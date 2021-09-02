
from botocore.client import Config
from datetime import datetime
import json
from typing import Dict
from urllib.parse import urlencode
from flask import send_file, Flask, jsonify
from flask_restful import Api, Resource, reqparse, request
from db import *
from flask_cors import CORS
import werkzeug
from werkzeug.utils import secure_filename
import boto3
from botocore.client import Config
import numpy
import base64
import os
from flask import render_template, url_for
from flask_weasyprint import HTML, render_pdf

# SETUP THE ENV


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# ## config
MSG_ALL_FIELDS = "Please enter all fields"


app = Flask(__name__)
# csrf = CSRFProtect()
# csrf.init_app(app)
CORS(app, origins="*", max_age="3600")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


api = Api(app, prefix='/api')


##
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


def uploadImage(file, name):
    ACCESS_ID = 'M5JE2VQZGQENQFXKIIGT'
    SECRET_KEY = 'RWJSd3ebdcgjhkxGurSJ2EsX0wpwQ81ENYf07NJy93w'

    # Initiate session
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='fra1',
                            endpoint_url='https://fra1.digitaloceanspaces.com',
                            aws_access_key_id=ACCESS_ID,
                            aws_secret_access_key=SECRET_KEY)

    # Upload a file to your Space
    res = client.upload_file(file, 'solmate', 'images/'+name)

    return res

# COMMONS 

# API REQUESTS
class Test(Resource):
    def get(self):
        return jsonify(message="OK", success=True)

# API REQUESTS
class AddKey(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('public_key', type=str, help='Missing param: public_key (str)', required="true")


        args = parser.parse_args()
        public_key = args['public_key']

        if(public_key == "" or public_key is None ):
            return jsonify(success=False, message=MSG_ALL_FIELDS)

        check_signup = db_user_add_key(public_key)
        if(check_signup == 1):
            return jsonify(success=True, message="Key Added Successfully!")
        else:
            return jsonify(success=False, message="Error Adding key!")


class WeddingInfo(Resource):
    def get(self):
        args = request.args
        public_key = args['public_key']

        if(public_key == "" or public_key is None):
            return jsonify(success=False, message=MSG_ALL_FIELDS)
        
        user_id = db_get_user_from_key(public_key)
        if(user_id == None):
            return jsonify(success=False, message="Invalid public key for user!")

        data = db_get_wedding_info(user_id)
        # print(data)
        if(data):
            data = json.loads(data)
            print(data)
            return jsonify(data)
        else:
            return None

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('public_key', type=str, help="Missig public_key", required="true")
        parser.add_argument('account_id', type=str, help="Missig account_id", required="true")
        parser.add_argument('trasaction_id', type=str, help="Missig trasaction_id", required="true")
        parser.add_argument('bride_firstname', type=str, help="Missig bride_firstname", required="true")
        parser.add_argument('bride_lastname', type=str, help="Missig bride_lastname", required="true")
        parser.add_argument('groom_firstname', type=str, help="Missig groom_firstname", required="true")
        parser.add_argument('groom_lastname', type=str, help="Missig groom_lastname", required="true")
        parser.add_argument('datetime', type=str, help="Missig datetime", required="true")
        parser.add_argument('location', type=str, help="Missig location", required="true")
        parser.add_argument('bestman_firstname', type=str, help="Missig bestman_firstname")
        parser.add_argument('bestman_lastname', type=str, help="Missig bestman_lastname")
        parser.add_argument('maidofhonor_firstname', type=str, help="Missig maidofhonor_firstname")
        parser.add_argument('maidofhonor_lastname', type=str, help="Missig maidofhonor_lastname")

        args = parser.parse_args()
        public_key = args['public_key']
        account_id = args['account_id']
        trasaction_id = args['trasaction_id']
        bride_firstname = args['bride_firstname'] 
        bride_lastname = args['bride_lastname']
        groom_firstname = args['groom_firstname']
        groom_lastname = args['groom_lastname']
        datetime = args['datetime']
        location = args['location']
        bestman_firstname = args['bestman_firstname']
        bestman_lastname = args['bestman_lastname']
        maidofhonor_firstname = args['maidofhonor_firstname']
        maidofhonor_lastname = args['maidofhonor_lastname']

        if(account_id == "" or account_id is None or trasaction_id == "" or trasaction_id is None or bride_firstname == "" or bride_firstname is None or bride_lastname == "" or bride_lastname is None or groom_firstname == "" or groom_firstname is None or groom_lastname == "" or groom_lastname is None or datetime == "" or datetime is None or location == "" or location is None):
            return jsonify(success=False, message=MSG_ALL_FIELDS)

        user_id = db_get_user_from_key(public_key)
        if(user_id == None):
            return jsonify(success=False, message="Invalid public key for user!")

        print(user_id)

        check = db_add_wedding_info(user_id, account_id, trasaction_id, bride_firstname, bride_lastname, groom_firstname, groom_lastname, datetime, location, bestman_firstname, bestman_lastname, maidofhonor_firstname, maidofhonor_lastname)
        if(check == 1):
            return jsonify(success=True, message="Wedding Details Added successful!")
        else:
            return jsonify(success=False, message="Oops...Error in adding wedding details")


class Nft(Resource):
    def get(self):
        args = request.args
        public_key = args['public_key']

        if(public_key == "" or public_key is None):
            return jsonify(success=False, message=MSG_ALL_FIELDS)

        user_id = db_get_user_from_key(public_key)
        if(user_id == None):
            return jsonify(success=False, message="Invalid public key for user!")

        data = db_get_nft(user_id)
        print(data)
        if(data):
            data = json.loads(data)
            print(data)
            return jsonify(data)
        else:
            return None
            
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('public_key', type=str, help="Missig public_key", required="true", location='form')
        parser.add_argument('datetime', type=str, help="Missig datetime", location='form')
        parser.add_argument('metadata_account_address', type=str, help="Missig metadata_account_address", required="true", location='form')
        parser.add_argument('minted_token_address', type=str,
                            help="Missig minted_token_address", required="true", location='form')
        parser.add_argument('nft_address', type=str, help="Missig nft_address", required="true",location='form')
        parser.add_argument(
            'image', type=werkzeug.datastructures.FileStorage, required="true", location='files')
        
        args = parser.parse_args()
        print(args['image'])
        print(type(args['image']))
        public_key = args['public_key']
        datetime = args['datetime']
        img = args['image'].read()
        metadata_account_address = args['metadata_account_address']
        minted_token_address = args['minted_token_address']
        nft_address = args['nft_address']

        # print(img.filename)
        # print(type(img))

        # if user does not select file, browser also
        # submit a empty part without filename
        # print(file.filename)
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # npimg = numpy.fromstring(img, numpy.uint8)
        # img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
        # print(type(img))

        # jpg_original = convertToBinaryData(img)
        # print(jpg_original)
        # print(type(jpg_original))


        # filename = secure_filename(img.filename)
        # img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # fname, file_extension = os.path.splitext(
        #     'uploads/'+filename)
    
        # # imgname = str(nft_address) + str(file_extension)
        # image = uploadImage('uploads/'+filename, imgname)
        # # print(image)

        # os.remove('uploads/'+filename)

        user_id = db_get_user_from_key(public_key)
        if(user_id == None):
            return jsonify(success=False, message="Invalid public key for user!")

        if(nft_address == "" or nft_address is None or metadata_account_address == "" or metadata_account_address is None or minted_token_address == "" or minted_token_address is None ):
            return jsonify(success=False, message=MSG_ALL_FIELDS)

        check = db_add_nft(user_id, img, metadata_account_address, minted_token_address, nft_address, datetime)
        if(check == 1):
            return jsonify(success=True, message="NFT Details Added successfully!")
        else:
            return jsonify(success=False, message="Oops...Error in adding NFT details")

class Social(Resource):
    def get(self):
        args = request.args
        public_key = args['public_key']

        if(public_key == "" or public_key is None):
            return jsonify(success=False, message=MSG_ALL_FIELDS)

        user_id = db_get_user_from_key(public_key)
        if(user_id == None):
            return jsonify(success=False, message="Invalid public key for user!")

        data = db_get_social_info(user_id)
        # print(data)
        if(data):
            data = json.loads(data)
            print(data)
            return jsonify(data)
        else:
            return None
            
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('public_key', type=str, help="Missig bride_firstname", required="true")
        parser.add_argument('url', type=str, help="Missig url", required="true")
        


        args = parser.parse_args()
        public_key = args['public_key']
        url = args['url']

        user_id = db_get_user_from_key(public_key)
        if(user_id == None):
            return jsonify(success=False, message="Invalid public key for user!")

        if(url == "" or url is None):
            return jsonify(success=False, message=MSG_ALL_FIELDS)

        check = db_add_to_social(user_id, url)
        if(check == 1):
            return jsonify(success=True, message="Social Details Added successfully!")
        else:
            return jsonify(success=False, message="Oops...Error in adding social details")

class Like(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('public_key', type=str, help="Missig bride_firstname", required="true")
        parser.add_argument('idsocial', type=str, help="Missig idsocial", required="true")

        args = parser.parse_args()
        public_key = args['public_key']
        idsocial = args['idsocial']
        
        user_id = db_get_user_from_key(public_key)
        if(user_id == None):
            return jsonify(success=False, message="Invalid public key for user!")
        
        likes = db_get_likes(user_id, idsocial)

        if(idsocial == None or idsocial == ""):
            return jsonify(success=False, message="No posts!")

        else:
            return jsonify(likes = str(likes),message = "liked",success = True)



class DisLike(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('public_key', type=str, help="Missig bride_firstname", required="true")
        parser.add_argument('idsocial', type=str, help="Missig idsocial", required="true")

        args = parser.parse_args()
        public_key = args['public_key']
        idsocial = args['idsocial']

        user_id = db_get_user_from_key(public_key)
        if(user_id == None):
            return jsonify(success=False, message="Invalid public key for user!")
        
        dislikes = db_get_dislikes(user_id, idsocial)

        if(idsocial == None or idsocial == ""):
            return jsonify(success=False, message="No posts!")

        else:
            return jsonify(likes = str(dislikes),message = "disliked",success = True)        


class Share(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('public_key', type=str, help="Missig bride_firstname", required="true")
        parser.add_argument('idsocial', type=str, help="Missig idsocial", required="true")

        args = parser.parse_args()
        public_key = args['public_key']
        idsocial = args['idsocial']

        user_id = db_get_user_from_key(public_key)
        if(user_id == None):
            return jsonify(success=False, message="Invalid public key for user!")

        shares = db_get_share(user_id, idsocial)

        if(idsocial == None or idsocial == ""):
            return jsonify(success=False, message="No posts!")

        else:
            return jsonify(shares = str(shares),message = "post shared", success = True)


class Certificate(Resource):
    def get(self):
        html = render_template('certificate.html')
        # html = render_template('doc2.html')
        return render_pdf(HTML(string=html))



# ENDPOINTS

api.add_resource(Test, '/test')
api.add_resource(AddKey, '/addKey')
api.add_resource(WeddingInfo, '/weddingInfo')
api.add_resource(Nft, '/nft')
api.add_resource(Social,'/social')
api.add_resource(Like,'/like')
api.add_resource(DisLike,'/dislike')
api.add_resource(Share,'/share')
api.add_resource(Certificate, '/certificate')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

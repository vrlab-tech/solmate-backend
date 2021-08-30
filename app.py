
from datetime import datetime
import json
from typing import Dict
from urllib.parse import urlencode
from flask import send_file, Flask, jsonify
from flask_restful import Api, Resource, reqparse, request
from db import *
from flask_cors import CORS


# SETUP THE ENV


# ## config
MSG_ALL_FIELDS = "Please enter all fields"


app = Flask(__name__)
# csrf = CSRFProtect()
# csrf.init_app(app)
CORS(app, origins="*", max_age="3600")


api = Api(app, prefix='/api')


##
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response



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
        parser.add_argument('bride_firstname', type=str, help="Missig bride_firstname", required="true")
        parser.add_argument('bride_lastname', type=str, help="Missig bride_lastname", required="true")
        parser.add_argument('groom_firstname', type=str, help="Missig groom_firstname", required="true")
        parser.add_argument('groom_lastname', type=str, help="Missig groom_lastname", required="true")
        parser.add_argument('datetime', type=str, help="Missig datetime", required="true")
        parser.add_argument('location', type=str, help="Missig location", required="true")
        parser.add_argument('bestman_firstname', type=str, help="Missig bestman_firstname", required="true")
        parser.add_argument('bestman_lastname', type=str, help="Missig bestman_lastname", required="true")
        parser.add_argument('maidofhonor_firstname', type=str, help="Missig maidofhonor_firstname", required="true")
        parser.add_argument('maidofhonor_lastname', type=str, help="Missig maidofhonor_lastname", required="true")

        args = parser.parse_args()
        public_key = args['public_key']
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

        if(bride_firstname == "" or bride_firstname is None or bride_lastname == "" or bride_lastname is None or groom_firstname == "" or groom_firstname is None or groom_lastname == "" or groom_lastname is None or datetime == "" or datetime is None or location == "" or location is None or bestman_firstname == "" or bestman_firstname is None or bestman_lastname == "" or bestman_lastname is None or maidofhonor_firstname == "" or maidofhonor_firstname is None or maidofhonor_lastname == "" or maidofhonor_lastname is None ):
            return jsonify(success=False, message=MSG_ALL_FIELDS)

        user_id = db_get_user_from_key(public_key)
        if(user_id == None):
            return jsonify(success=False, message="Invalid public key for user!")

        print(user_id)


        check = db_add_wedding_info(user_id, bride_firstname, bride_lastname, groom_firstname, groom_lastname, datetime, location, bestman_firstname, bestman_lastname, maidofhonor_firstname, maidofhonor_lastname)
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
        parser.add_argument('url', type=str, help="Missig bride_firstname", required="true")
        parser.add_argument('datetime', type=str, help="Missig datetime", required="true")

        args = parser.parse_args()
        public_key = args['public_key']
        datetime = args['datetime']
        url = args['url']

        user_id = db_get_user_from_key(public_key)
        if(user_id == None):
            return jsonify(success=False, message="Invalid public key for user!")

        if(datetime == "" or datetime is None or url == "" or url is None):
            return jsonify(success=False, message=MSG_ALL_FIELDS)

        check = db_add_nft(user_id, datetime, url)
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

class Likes(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('public_key', type=str, help="Missig bride_firstname", required="true")
        parser.add_argument('idsocial', type=str, help="Missig idsocial", required="true")

        args = parser.parse_args()
        public_key = args['public_key']
        idsocial = args['idsocial']
        likes = db_get_likes(public_key)

        if(idsocial == None or idsocial == ""):
            return jsonify(success=False, message="No posts!")

        else:
            return jsonify(likes = likes,message = "likes Added",success = True)



class DisLikes(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('public_key', type=str, help="Missig bride_firstname", required="true")
        parser.add_argument('idsocial', type=str, help="Missig idsocial", required="true")

        args = parser.parse_args()
        public_key = args['public_key']
        idsocial = args['idsocial']
        dislikes = db_get_dislikes(public_key)

        if(idsocial == None or idsocial == ""):
            return jsonify(success=False, message="No posts!")

        else:
            return jsonify(dislikes = dislikes,message = "likes removed",success = True)        


class Share(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('public_key', type=str, help="Missig bride_firstname", required="true")
        parser.add_argument('idsocial', type=str, help="Missig idsocial", required="true")

        args = parser.parse_args()
        public_key = args['public_key']
        idsocial = args['idsocial']
        shares = db_get_dislikes(public_key)

        if(idsocial == None or idsocial == ""):
            return jsonify(success=False, message="No posts!")

        else:
            return jsonify(shares = shares,message = "post shared",success = True)



# ENDPOINTS

api.add_resource(Test, '/test')
api.add_resource(AddKey, '/addKey')
api.add_resource(WeddingInfo, '/weddingInfo')
api.add_resource(Nft, '/nft')
api.add_resource(Likes,'/likes')
api.add_resource(DisLikes,'/dislikes')
api.add_resource(Share,'/shared')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

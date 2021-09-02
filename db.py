import time
from typing import ClassVar
import pandas as pd
from hmac import new
import re
from models import Social, Users, WeddingInfo, Nft, engine, session, OperationalError, StatementError, wraps
from passlib.hash import sha256_crypt
from datetime import datetime

def mk_session(fun):
    def wrapper(*args, **kwargs):
        s = session()
        kwargs['session'] = s
        try:
            res = fun(*args, **kwargs)
        except Exception as e:
            s.rollback()
            s.close()
            raise e

        s.close()
        return res
    wrapper.__name__ = fun.__name__
    return wrapper


def retry_db(exceptions, n_retries=3, ival=1):
    def decorator(fun):
        @wraps(fun)
        def wrapper(*args, **kwargs):
            exception_logged = False
            for r in range(n_retries):
                try:
                    return fun(*args, **kwargs)
                except exceptions as e:
                    if not exception_logged:
                        print(e)
                        exception_logged = True
                    else:
                        print("Retry #" + r + " after receiving exception.")

                    time.sleep(ival)
            return fun(*args, **kwargs)
        return wrapper
    return decorator


@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def db_user_add_key(key, session=None):
    try:
        check_key = session.query(Users).filter(Users.public_key == key).statement
        df = pd.read_sql(check_key, engine)
        if(df.empty):
            addkey = Users(public_key = key)
            session.add(addkey)
            session.commit()
        return 1
    except Exception as e:
        print(e)
        return 0

@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def db_get_user_from_key(key, session=None):
    check_key = session.query(Users).with_entities(Users.idusers).filter(Users.public_key == key).statement
    df = pd.read_sql(check_key, engine)
    if(df.empty):
        return None
    else:
        user_id = df.iloc[0]['idusers']
        return user_id 



@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def db_add_wedding_info(user_id, account_id, trasaction_id, bride_firstname, bride_lastname, groom_firstname, groom_lastname, datetime, location, bestman_firstname, bestman_lastname, maidofhonor_firstname, maidofhonor_lastname, session=None):
    try:
        check_info = session.query(WeddingInfo).filter(WeddingInfo.user_id == user_id).statement
        df = pd.read_sql(check_info, engine)
        if(df.empty):
            insert_key = WeddingInfo(user_id=user_id, account_id=account_id, trasaction_id=trasaction_id, bride_firstname=bride_firstname, bride_lastname=bride_lastname, groom_firstname=groom_firstname, groom_lastname=groom_lastname,
                                     datetime=datetime, location=location, bestman_firstname=bestman_firstname, bestman_lastname=bestman_lastname, maidofhonor_firstname=maidofhonor_firstname, maidofhonor_lastname=maidofhonor_lastname)
            session.add(insert_key)
        session.commit()
        return 1
    except Exception as e:
        print(e)
        return 0


@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def db_get_wedding_info(user_id, session=None):
    try:
        check_info= session.query(WeddingInfo).with_entities(WeddingInfo.account_id,WeddingInfo.transaction_id,WeddingInfo.bride_firstname, WeddingInfo.bride_lastname, WeddingInfo.groom_firstname, WeddingInfo.groom_firstname, WeddingInfo.datetime, WeddingInfo.location, WeddingInfo.bestman_firstname, WeddingInfo.bestman_lastname, WeddingInfo.maidofhonor_firstname, WeddingInfo.maidofhonor_lastname ).filter(
            WeddingInfo.user_id == user_id).statement
        df = pd.read_sql(check_info, engine)
        if(df.empty):
            return None
        else:
            return df.to_json(orient="records")
    except Exception as e:
        print(e)
        return None


@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def db_add_nft(user_id, img, metadata_account_address, minted_token_address, nft_address, datetime=None, session=None):
    try:
        check_nft = session.query(Nft).filter(Nft.user_id == user_id, Nft.nft_address ==nft_address).statement
        df = pd.read_sql(check_nft, engine)
        if(df.empty):
            insert_nft = Nft(user_id=user_id, datetime=datetime, image=img, metadata_account_address=metadata_account_address,minted_token_address=minted_token_address,nft_address=nft_address)
            session.add(insert_nft)
            session.commit()
            session.flush()
            return insert_nft.idnft
    except Exception as e:
        print(e)
        return 0


@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def db_get_nft(user_id, session=None):
    try:
        check_info = session.query(Nft).with_entities(Nft.idnft, Nft.image, Nft.metadata_account_address, Nft.minted_token_address, Nft.nft_address, Nft.datetime, Nft.created_at).filter(
            Nft.user_id == user_id).statement
        df = pd.read_sql(check_info, engine)
        if(df.empty):
            return None
        else:
            return df.to_json(orient="records")
    except Exception as e:
        print(e)
        return None

@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def db_get_social_info(user_id, session=None):
    try:
        check_info = session.query(Social, Nft).with_entities(Social.idsocial, Nft.image, Nft.nft_address, Social.likes, Social.shares, Social.created_at, Social.updated_at).filter(
            Social.user_id == user_id, Social.idnft == Nft.idnft).statement
        df = pd.read_sql(check_info, engine)
        if(df.empty):
            return None
        else:
            return df.to_json(orient="records")
    except Exception as e:
        print(e)
        return None


@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def db_add_to_social(user_id, idnft, session=None):
    try:
        insert_post = Social(user_id=user_id, idnft=idnft)
        session.add(insert_post)
        session.commit()
        return 1
    except Exception as e:
        print(e)
        return 0


@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def db_get_likes(user_id,idsocial,session=None):
   
    check_info = session.query(Social).with_entities(Social.likes).filter(Social.user_id == user_id, Social.idsocial == idsocial).statement
    df = pd.read_sql(check_info, engine)
    if(df.empty):
        return None
    else:
        likes = df.iloc[0]['likes']
        likes = likes + 1
        update_likes = {"likes": likes}
        session.query(Social).filter(Social.idsocial == idsocial).update(update_likes, synchronize_session=False)
        session.commit()
        return likes



@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def db_get_dislikes(user_id,idsocial,session=None):
   
    check_info = session.query(Social).with_entities(Social.likes).filter(Social.user_id == user_id, Social.idsocial == idsocial).statement
    df = pd.read_sql(check_info, engine)
    if(df.empty):
        return None
    else:
        dislikes = df.iloc[0]['likes']
        dislikes = dislikes - 1
        update_likes = {"likes": dislikes}
        session.query(Social).filter(Social.idsocial == idsocial).update(update_likes, synchronize_session=False)
        session.commit()
        return dislikes


@retry_db((OperationalError, StatementError), n_retries=3)
@mk_session
def db_get_share(user_id,idsocial,session=None):
   
    check_info = session.query(Social).with_entities(Social.shares).filter(Social.user_id == user_id, Social.idsocial == idsocial).statement
    df = pd.read_sql(check_info, engine)
    if(df.empty):
        return None
    else:
        shares = df.iloc[0]['shares']
        shares = shares + 1
        update_shares = {"shares": shares}
        session.query(Social).filter(Social.idsocial == idsocial).update(update_shares, synchronize_session=False)
        session.commit()
        return shares        

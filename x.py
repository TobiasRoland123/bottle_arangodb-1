from bottle import request, response
from icecream import ic
import re
import requests

##############################
def disable_cache():
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0)   


##############################

def db(query):
    try:
        url = "http://arangodb:8529/_api/cursor"
        res = requests.post( url, json = query )
        ic(res)
        ic(res.text)
        return res.json()
    except Exception as ex:
        print("#"*50)
        print(ex)
    finally:
        pass


##############################
USER_FIRST_NAME_MIN = 2
USER_FIRST_NAME_MAX = 20
USER_FIRST_NAME_REGEX = "^.{2,20}$"

def validate_user_first_name():
    error = f"user_first_name {USER_FIRST_NAME_MIN} to {USER_FIRST_NAME_MAX} characters"
    user_first_name = request.forms.get("user_first_name", "")
    user_first_name = user_first_name.strip()
    if not re.match(USER_FIRST_NAME_REGEX, user_first_name): raise Exception(400, error)
    return user_first_name


##############################
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
USER_LAST_NAME_REGEX = "^.{2,20}$"

def validate_user_last_name():
    error = f"user_last_name {USER_LAST_NAME_MIN} to {USER_LAST_NAME_MAX} characters"
    user_last_name = request.forms.get("user_last_name", "")
    user_last_name = user_last_name.strip()
    if not re.match(USER_LAST_NAME_REGEX, user_last_name): raise Exception(400, error)
    return user_last_name




##############################
USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20
USER_USERNAME_REGEX = "^.{2,20}$"

def validate_user_username():
    error = f"user_username {USER_USERNAME_MIN} to {USER_USERNAME_MAX} characters"
    user_username = request.forms.get("user_username", "")
    user_username = user_username.strip()
    if not re.match(USER_USERNAME_REGEX, user_username): raise Exception(400, error)
    return user_username





##############################

USER_KEY_REGEX = "^[1-9]\d*$"

def validate_user_key(user_key):
    error = f"user_key has a problem, does it start with zero?"
    
    user_key = user_key.strip()
    if not re.match(USER_KEY_REGEX, user_key): raise Exception(400, error)
    return user_key



##############################

USER_GENDER_REGEX = "^(male|female|no-gender)$"

def validate_user_gender():
    error = f"user_gender error"
    user_gender = request.forms.get("user_gender", "")

    print(f"########################   usergender: {user_gender} #####################################")
    user_gender = user_gender.strip()
    if not re.match(USER_GENDER_REGEX, user_gender): raise Exception(400, error)
    return user_gender



def return_gender(key,gender):
    print(50*".", gender, key)
    if gender == "male":
        return f"""
      🚹
        """
    elif gender == "female":
        return f"""
        🚺
        """
    elif gender == "no-gender":
        return f"""
       🚻
        """
        
    else:
        return "u have a gender that doesnt exist in real life"
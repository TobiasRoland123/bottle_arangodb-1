from bottle import delete, get, post, put, request, static_file, template
import x
from icecream import ic

##############################
@get("/favicon.ico")
def _():
    return static_file("favicon.ico", ".")

##############################
@get("/app.css")
def _():
    return static_file("app.css", ".")

##############################
@get("/mixhtml.js")
def _():
    return static_file("mixhtml.js", ".")

##############################
@get("/test")
def _():
    try:
        return template("test")
    except Exception as ex:
        pass
    finally:
        pass


##############################
@get("/")
def _():
    try:
        x.disable_cache()
        users = x.db({"query":"FOR user IN users RETURN user"})
        return template("index", users=users["result"])
    except Exception as ex:
        ic(ex)
        return "system under maintainance"         
    finally:
        pass

##############################
@post("/users")
def _():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_username = x.validate_user_username()
        user_gender = x.validate_user_gender()
        ic(user_gender)
        user = {"first_name":user_first_name, "last_name":user_last_name, "username": user_username, "gender": user_gender}
        res = x.db({"query":"INSERT @doc IN users RETURN NEW", "bindVars":{"doc":user}})
        html = template("_user.html", user=res["result"][0])
        form_create_user =  template("_form_create_user.html")
        return f"""
        <template mix-target="#users" mix-top>
            {html}
        </template>
        <template mix-target="#frm_user" mix-replace>
            {form_create_user}
        </template>
        """
    except Exception as ex:
        ic(ex)
        if "user_first_name" in str(ex):
            return f"""
            <template mix-target="#message">
                {ex.args[1]}
            </template>
            """            
    finally:
        pass


##############################
@delete("/users/<key>")
def _(key):
    try:
        ic(key)
        validated_key = x.validate_user_key(key)
        res = x.db({"query":"""
                    FOR user IN users
                    FILTER user._key == @key
                    REMOVE user IN users RETURN OLD""", 
                    "bindVars":{"key":validated_key}})
        print(res)
        return f"""
        <template mix-target="[id='{validated_key}']" mix-replace>
            <div class="mix-fade-out user_deleted" mix-ttl="2000">User deleted</div>
        </template>
        """
    except Exception as ex:
        ic(ex)
    finally:
        pass


##############################
@put("/users/<key>")
def _(key):
    try:
        first_name = x.validate_user_first_name()
        last_name = x.validate_user_last_name()
        username= x.validate_user_username()
        res = x.db({"query":"""
                        UPDATE { _key: @key,username: @username, first_name: @first_name, last_name:@last_name } 
                        IN users 
                        RETURN NEW""",
                    "bindVars":{
                        "key": f"{key}",
                        "username":f"{username}",
                        "first_name":f"{first_name}",
                        "last_name":f"{last_name}"
                    }})
        return f"""
        <template>            
        </template>
        """
    except Exception as ex:
        ic(ex)
        if "user_first_name" in str(ex):
            return f"""
            <template mix-target="#message">
                {ex.args[1]}
            </template>
            """            
    finally:
        pass
















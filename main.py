from flask import Flask,request,redirect, url_for, send_from_directory,Response,jsonify,make_response, render_template
import json
import base64 
import requests

def base64tofile(base64code):
    with open("tmp.png","wb") as f:
        f.write(base64.decodebytes(base64code))

app = Flask(__name__)

@app.route('/iSocialSignup', methods=['POST', 'GET'])
def iSocialSignup():
    f = open("iSocialAccount.json")
    account_data = json.load(f)
    list_id = list(account_data.keys())
    if request.method == "GET":
        return jsonify({
            "status":"1",
            "content":"ping success"
        })
    else:
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        for id in list_id:
            if (email in account_data[id]["email"]) or (username in account_data[id]["uname"]):
                return jsonify({
                    "status":"0",
                    "content": "account may exist"
                })

        account_data[str(len(list_id)+1)] = {

            "email":email,
            "uname":username,
            "password":password

        }

        json_object = json.dumps(account_data, indent=6)
        with open("iSocialAccount.json","w") as new_file:
            new_file.write(json_object)
        
        return jsonify({
            "status":"1",
            "content":"register success"
        })


@app.route("/iSocialLogin", methods = ["GET", "POST"])
def iSociallogin():
    f = open("iSocialAccount.json")
    account_data = json.load(f)

    if request.method == "GET":
        return jsonify({
            "status":"1",
            "content":"ping success"
        })
    else:
        username = request.form["username"]
        password = request.form["password"]
        
        list_id = list(account_data.keys())

        for id in list_id:
            if account_data[id]["uname"] == username:
                if account_data[id]["password"] == password:
                    return jsonify({
                        "status":"1",
                        "content":"login success",
                        "user_data":account_data[id]
                    })
                else:
                    return jsonify({
                        "status":"0",
                        "content":"wrong password"
                    })
        return jsonify({
            "status":"-1",
            "content":"No account found"
        })
@app.route("/iSocialChangePassword", methods = ["GET", "POST"])
def iSocialChangePassword():
    f = open("iSocialAccount.json")
    account_data = json.load(f)

    if request.method == "GET":
        return jsonify({
            "status":"1",
            "content":"ping success"
        })
    else:
        currentPassword = request.form["currentPassword"]
        newPassword = request.form["newPassword"]
        
        list_id = list(account_data.keys())

        for id in list_id:
            if account_data[id]["password"] == currentPassword:
                account_data[id]["password"] = newPassword
                json_object = json.dumps(account_data, indent=6)
                with open("iSocialAccount.json","w") as new_file:
                    new_file.write(json_object)
                return jsonify({
                    "status":"1",
                    "content":"change password success",
                    "user_data":account_data[id]
                })
        return jsonify({
            "status":"-1",
            "content":"Wrong password"
        })

@app.route("/login", methods = ["GET", "POST"])

def login():

    f = open("iSocialAccount.json")
    account_data = json.load(f)

    if request.method == "GET":
        return jsonify({
            "status":"1",
            "content":"ping success"
        })
    else:

        username = request.form["username"]
        password = request.form["password"]
        
        list_id = list(account_data.keys())

        for id in list_id:
            if account_data[id]["phone"] == username:
                if account_data[id]["password"] == password:
                    return jsonify({
                        "status":"1",
                        "content":"login success",
                        "usser_data":account_data[id]
                    })
                else:
                    return jsonify({
                        "status":"0",
                        "content":"wrong password"
                    })
        return jsonify({
            "status":"-1",
            "content":"No account found"
        })

        # except:
            # return jsonify({
                
            #     "status":"0",
            #     "content":"send Fail"
                
            # })


@app.route("/register", methods = ["GET", "POST"])
    
def register():

    f = open("iSocialAccount.json")
    account_data = json.load(f)
    list_id = list(account_data.keys())
    if request.method == "GET":
        return jsonify({
            "status":"1",
            "content":"ping success"
        })
    else:

        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        sex = request.form["sex"]
        username = request.form["username"]
        password = request.form["password"]

        for id in list_id:
            if (email in account_data[id]["email"]) or (username in account_data[id]["uname"]) or (phone in account_data[id]["phone"]):
                return jsonify({
                    "status":"0",
                    "content": "account may exist"
                })

        account_data[str(len(list_id)+1)] = {

            "fullname": fullname,
            "phone":phone,
            "email":email,
            "uname":username,
            "sex": sex,
            "password":password

        }

        json_object = json.dumps(account_data, indent=6)
        with open("account.json","w") as new_file:
            new_file.write(json_object)
        
        return jsonify({
            "status":"1",
            "content":"register success"
        })

@app.route("/get_posts", methods = ["GET", "POST"])
    
def get_post():
    
    f = open("posts.json")
    
    data = json.load(f)
    
    if request.method == "GET":
        return jsonify({
            "status":"1",
            "content":"ping success"
        })
    else:
        channelName = request.form["channelID"]
        res = dict()
        for i in range(len(data)):
            if (data[i]["channelID"] == channelName):
                res[str(i)] = data[i]
        return jsonify(res)

@app.route("/feed", methods = ["GET", "POST"])      

def get_feed():

    f = open("feed_data.json")

    data = json.load(f)
    res = []

    if request.method == "GET":
        return jsonify({
            "status":"1",
            "content":"ping success"
        })
    else:
        for i in range(len(data["feedData"])):
            res.append(data["feedData"][i])

        return jsonify({"status":"success",
                        "content":res})


@app.route("/comment", methods = ["GET", "POST"])      

def comment():

    f = open("comments.json")

    data = json.load(f)
    res = []

    if request.method == "GET":
        return jsonify({
            "status":"1",
            "content":"ping success"
        })
    else:
        
        userid = request.form["userID"]
        for i in range(len(data["comments"])):
            if userid == data["comments"][i]["username"]:
                res.append(data["comments"][i])
        return jsonify({

            "status":"success",
            "content": res

        })

@app.route("/create_post", methods = ["GET", "POST"])  

def create_post():
    
    if request.method == 'GET':
        return jsonify({
            "status":"1",
            "content":"ping success"
        })
    else:
        try:
            captions = request.form["caption"]
            media_file = request.files["media"]
            media_type = request.form["types"]
            media_file.save("./data/"+media_file.filename)
            
            return jsonify({
                
                "status":"1",
                "content":"success"
                
            })
            
        except:
            return jsonify({
                "status":"0",
                "content":"upload fail"
            })
    
@app.route("/profile", methods = ["GET", "POST"])  

def get_profile():
    f = open("users.json")
    data = json.load(f)
    res = dict()
    if request.method == "GET":
        return jsonify({
            
            "status": "1",
            "content":"ping success"
            
        })
    
    else:
        
        accountid = request.form["accountid"]
        list_id = list(data.keys())
        
        for id in list_id:
            
            if (data[str(id)]["accountid"] == str(accountid)):
                return jsonify({
                    
                    "status":"1",
                    "content":data[str(id)]
                    
                })
        return jsonify({
            
            "status":"0",
            "content":"user not found"
            
        })

@app.route('/updateComments',  methods = ["GET", "POST"])

def updateComment():

    f = open("feed_data.json")
    data = json.load(f)

    if request.method == "GET":
        return jsonify({
            "status":"1",
            "content":"ping success"
        })
    else:
        try:
            id = request.form["id"]
            avatarUri = request.form["avatarUri"]
            content = request.form["content"]

            username = request.form["username"]
            userID = request.form["userID"]

            for i in range(len(data["feedData"])):
                if data["feedData"][i]["id"] == str(id):
                    data["feedData"][i]["comments"].append({

                        "id": userID, 
                        "avatarUri": avatarUri,
                        "content": content,
                        "username": username

                    })
            
            json_object = json.dumps(data, indent=6)
            with open("feed_data.json","w") as new_file:
                new_file.write(json_object)
            return jsonify({
                "status":"1",
                "content": "success"
            })
        except:
            return jsonify({
                "status":"0",
                "content": "comments fail"
            })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

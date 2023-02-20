from time import timezone
import jwt, datetime, os, subprocess
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
server.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
server.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
server.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
server.config['MYSQL_PORT'] = os.environ.get("MYSQL_PORT")
print(server.config["MYSQL_HOST"])

def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz
        },
        secret,
        algorithm="HS256",
    )

@server.route("/login", methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentails", 401
    cur = mysql.connection.cursor()
    res = cur.execute(
        f"SELECT email, password FROM {auth.username}"
        )
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT"))
    else:
        return "Invalid credentials", 401
    # auth.username = 
    # auth.password = 

@server.route("/validate", methods=['POST'])
def validate():
    encoded_jwt = request.headers['Authorization']
    if not encoded_jwt:
        return "Missing credentials", 401
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "Not authorized", 403
    return decoded, 200
    
@server.route("/upload", methods=['POST'])
def upload():
    pass

@server.route("/download", methods=['GET'])
def download():
    pass

"""
wf_params = [{'a':"a"}, {'b':"d"}]
wf_params += [{'c': "s"}]   
for i in wf_params:
    for j in i:
        print(j.upper(), j, type(j), i[j])
        os.environ[j] = i[j]
"""

if __name__ == "__main__":
    print(__name__)
    server.run(host = '0.0.0.0', port = 5000)


# # +
# import os
# import subprocess

# wf_params=wf_params

# #execute bash script that sets the env vars
# subprocess.call([".", wf_params], shell=True)

# #try to get the variable set and print it
# print(os.getenv(wf_params))
# -

# !printenv



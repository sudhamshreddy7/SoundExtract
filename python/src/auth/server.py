import jwt, datetime, os
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="admin",
  password="admin"
)
print(mydb)
from flask import Flask, request
from flask_mysqldb import MySQL
server = Flask(__name__)
mysql = MySQL(server)
# configuration
server.config['MYSQL_USER']='admin'
server.config['MYSQL_PASSWORD']='admin'
server.config['MYSQL_DB'] = ''
# print(server.config)
server.config['MYSQL_USER']=os.environ.get('MYSQL_USER')
server.config['MYSQL_PASSWORD']=os.environ.get('MYSQL_PASSWORD')
server.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
server.config['MYSQL_PORT'] = os.environ.get('MYSQL_PORT')

@server.route("/login",methods = ['POST'])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    # db authorization
    cur = mysql.connection.cursor()
    res = cur.execute(
        'SELECT EMAIL,PASSWORD FROM USER WHERE EMAIL=%s',(auth.username,)
    )
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1] 
        if auth.username != email or auth.password != password:
            return "invalid credentials",401
        else :
            return createJWT(email,os.environ.get("JWT_SECRET"),True)
    else:
        return "invalid credentials",401
@server.route("/validate",method = ["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "missing credentials",401
    # Bearer token
    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
            encoded_jwt , os.environ.get("JWT_SECRET"), algorithm = ["HS256"]
        )
    except:
        return "invalid credentials",403
    return decoded,200
        



def createJWT(name,secret,authz):
    return jwt.encode(
        {
            "username":name,
            "exp":datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat":datetime.datetime.now(tz=datetime.timezone.utc),
            "admin":authz
        },
        secret,
        algorithm = "HS256",
    )

if __name__=="__main__":
    server.run(host="0.0.0.0",port=5000)

from flask import Flask,request
from flask_cors import CORS,cross_origin
import psycopg2,os,secrets,string
from flask import send_from_directory
from werkzeug.security import check_password_hash,generate_password_hash

# Database credentials
Host = "b87clogurgswprpe6rob-postgresql.services.clever-cloud.com"
Database = "b87clogurgswprpe6rob"
User = "ujinfmddr21fx2lz7awm"
Port= 5432
Password = "TilJ3xqMndLEsPBMCXxE"

app = Flask(__name__)
CORS(app)


'''cur.execute("CREATE TABLE IF NOT EXISTS doctors("
    "did VARCHAR(6) PRIMARY KEY,"
    "name VARCHAR(25) NOT NULL,"
    "email VARCHAR(25) UNIQUE NOT NULL,"
    "password VARCHAR(12) NOT NULL,"
    "pcount INT DEFAULT 0"
    ");")'''

'''cur.execute("CREATE TABLE IF NOT EXISTS patients("
    "pid INT PRIMARY KEY,"
    "did VARCHAR(6) NOT NULL,"
    "name VARCHAR(25) NOT NULL,"
    "age INT NOT NULL,"
    "phone VARCHAR(10) NOT NULL,"
    "bgroup VARCHAR(10) NOT NULL,"
    "weight INT NOT NULL,"
    "height INT NOT NULL,"
    "mhistory VARCHAR(200),"
    "FOREIGN KEY (did) REFERENCES Doctors(did)"
    ");")'''

'''cur.execute("INSERT INTO Doctors(did,name,email,password,pcount) VALUES('gddjnv','testName1','test456@gmail.com','hghdfjdjf124',0);")
conn.commit()
print("inserted")
cur.execute("SELECT * FROM Doctors")
print(cur.fetchall())
conn.close()'''

def connectDB():
    conn = psycopg2.connect(dbname = Database, user = User ,password = Password, host = Host)
    if(conn):
        print("got connected")
    else:
        print("not connected")
    return conn

def generateID(cur):
    id = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(6)) 
    cur.execute("SELECT * FROM doctors WHERE did=%s",(id,))
    if(cur.fetchone() != None):
        id = generateID(cur)
    return id

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/test",methods=['POST'])
def hello_world():
    content =  request.get_data()
    #response.json()
    print(content)
    return "Hello, World!",200

@app.route("/register",methods=['POST'])
@cross_origin()
def register():
    data = request.get_json()
    conn = connectDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors WHERE email=%s",(data['email'],))
    if(cur.fetchone() != None):
        return "User already exists!!",201
    hashedPass = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=12)
    print(hashedPass,len(hashedPass))
    values = (generateID(cur),data['name'],data['email'],hashedPass,0)
    cur.execute("INSERT INTO doctors(did,name,email,password,pcount) VALUES(%s,%s,%s,%s,%s);",values)
    conn.commit()
    conn.close()
    return "Success",200

@app.route("/login",methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()
    print(data)
    conn = connectDB()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors WHERE email=%s",(data['email'],))
    drData = cur.fetchone()
    if(drData != None and check_password_hash(drData[3],data["password"])):
        conn.close()
        return "User found!!",200
    conn.close()
    return "User not found",201
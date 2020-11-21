import mariadb
from flask import Flask, request, Response
import json
import dbcreds
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
@app.route('/blog_post', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def blog_post():
    if request.method == 'GET':
        conn = None
        cursor =None
        blog_post = None 
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM blog_post")
            blog_post = cursor.fetchall()
        except Exception as error:
            print("Something went wrong : ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(blog_post != None):
                return Response(json.dumps(blog_post, default=str), mimetype="application/json", status=200)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    
    elif request.method == 'POST':
        conn = None
        cursor = None
        username = request.json.get("username")
        content = request.json.get("content")
        created_at = request.json.get("created_at")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO blog_post(username, content, created_at) VALUES (?,?,?)", [username, content, created_at])
            conn.commit()
            rows = cursor.rowcount
        except Exception as error:
            print("Something went wrong (THIS IS LAZY): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("Content Posted", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
            
    
    elif request.method == "PATCH":
        conn = None
        cursor = None 
        username = request.json.get("username") 
        content = request.json.get("content")
        
        id =request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            if username != "" and username != None:
                cursor.execute("UPDATE blog_post SET username=? WHERE id=?", [username, id])
            if content != "" and content != None:
                cursor.execute("UPDATE blog_post SET content=? WHERE id=?", [content, id])
           
            conn.commit() 
            rows = cursor.rowcount    
        except Exception as error:
            print("Something went wrong (This is LAZY)")  
            print(error)  
        finally: 
            if cursor != None:
                cursor.close() 
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Updated Success", mimetype="text/html", status=204)
            else:
                return Response("Update Failed", mimetype="text/html", status=500)
            
        
    elif request.method == "DELETE":
        conn = None
        cursor = None 
        id =request.json.get("id")
        rows = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM blog_post WHERE id=?", [id])
            conn.commit() 
            rows = cursor.rowcount    
        except Exception as error:
            print("Something went wrong (This is LAZY)")  
            print(error)  
        finally: 
            if cursor != None:
                cursor.close() 
            if conn != None:
                conn.rollback()
                conn.close()
            if (rows == 1):
                return Response("Delete Success", mimetype="text/html", status=204)
            else:
                return Response("Delete Failed", mimetype="text/html", status=500)      
            
    

                
   
   
# cloud-computing
It's a progect which develpo in Python and Flask and build a prototype of a Cloud application.
I use cassandra as my database.
There is 4 REST-based service interface.

@app.route('/')
#Home page to introduce the project

@app.route('/student/')
#Show all student which I store in the cassandra

@app.route('/student/get/<id>',methods=["GET"])
#Show one student you choose by id(the private key)

@app.route('/student/post',methods=["POST"])
#you should send a request in terminal and it will add one student
The request just like
#curl -i -H "Content-Type: application/json" -X POST -d'{"stu_id":"4","stu_age":"21","stu_name":"bobo","stu_pwd":"zxx23"}' http://127.0.0.1:8080/student/post

@app.route('/student/delete/<id>',methods=['DELETE'])
#you should send a request in terminal and it will delete a student which you choose
The request just like
#curl -X "DELETE" http://127.0.0.1:8080/student/delete/<id>

@app.route('/crime',methods=['GET'])
#get some data(crime_id and month) from url, and store in my database

from flask import Flask,request,jsonify
from cassandra.cluster import Cluster
import requests

cluster = Cluster()
session = cluster.connect()
app = Flask(__name__)

@app.route('/')
def hello():
    return('<h1>This is my cloud computing mini-project!</h1>')


@app.route('/student/')
def profile():
    rows = session.execute( 'Select * From student.stu;')
    return('<h1> {} </h1>'.format(rows.current_rows))

@app.route('/student/get/<id>',methods=["GET"])
def get(id):
    rows = session.execute('Select * From student.stu where stu_id = {}'.format(id))
    if rows == None:
        return('There is no student id ={}'.format(id))
    else:
        return ('<h1>{}</h1>'.format(rows.current_rows))

@app.route('/student/post',methods=["POST"])
def post():
    if not request.json or not 'stu_id' in request.json or not 'stu_age' in request.json or not 'stu_name' in request.json:
        return jsonify({'error': 'this student is existed'}), 400
    new_record = {
        'stu_id': request.json['stu_id'],
        'stu_age': request.json['stu_age'],
        'stu_name': request.json['stu_name'],
        'stu_pwd': request.json['stu_pwd']
        }
    session.execute("""insert into student.stu(stu_id,stu_age,stu_name,stu_pwd) values ({},{},'{}','{}')""".format(new_record['stu_id'],new_record['stu_age'],new_record['stu_name'],new_record['stu_pwd']))
    return jsonify({'message':'record has created:{}'}.format(new_record['stu_name'])),201


@app.route('/student/delete/<id>',methods=['DELETE'])
def delete(id):
    session.execute('Delete from student.stu where stu_id={}'.format(id))
    rows = ( 'Select * From student.stu;')
    return ('<h1>{}</h1>'.format(rows))

@app.route('/crime',methods=['GET'])
def crime():
    crime_url_template ='https://data.police.uk/api/crimes-street/all-crime?lat={lat}&lng={lng}&date={data}'
    my_latitude = '51.52369'
    my_longitude = '-0.0395857'
    my_date = '2018-11'
    crime_url = crime_url_template.format(lat = my_latitude,
    lng = my_longitude,
    data = my_date)
    resp = requests.get(crime_url)
    crimes = resp.json()
    new = []
    for crime in crimes:
        new.append({
        'crime_id': crime['id'],
        'month': crime['month'],
    })
    print new
    for item in new:
        session.execute("insert into crimesdata.stats(crime_id,month) values ({},'{}')".format(item['crime_id'],item['month']))
    rows = session.execute('Select * From crimesdata.stats;')
    return ('<h1> {} </h1>'.format(rows.current_rows))


if __name__ == '__main__':
    app.run(port=8080, debug=True)


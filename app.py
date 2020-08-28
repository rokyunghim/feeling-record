from flask import Flask, render_template, jsonify, request,session

app = Flask(__name__)

from pymongo import MongoClient
from bson.objectid import ObjectId

# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@3.35.52.217', 27017)
db = client.feel
app.secret_key = "ABCDEFG"

@app.route('/')
def main():
    if "username" in session:
        return render_template('profil.html')
    else:
        return render_template('index.html')

@app.route('/signin')
def signIn():
    if "username" in session:
        return render_template('profil.html')
    else:
        return render_template('signin.html')

@app.route("/session", methods=['POST'])
def login():
    id = request.form['id']
    pw = request.form['password']
    members = list(db.members.find({},{'_id':False}))
    member_one = {}

    for member in members:
        if member['id'] == id and member['pw'] == pw:
            member_one['id'] = member['id']
            member_one['pw'] = member['pw']

    if 'id' in member_one.keys():
        session["username"] = member_one['id']
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'error'})

@app.route('/signup')
def signUp():
    return render_template('signup.html')

@app.route('/signup_db', methods=['POST'])
def signup_db():
    id = request.form['id']
    pw = request.form['password']
    doc = {
        'id': id,
        'pw': pw
    }
    db.members.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다.'})

@app.route('/home')
def home():
    if "username" in session:
        return render_template('profilprofil.html')
    else:
        return render_template('signin.html')


@app.route('/profil')
def profil():
    if "username" in session:
        return render_template('profil.html')
    else:
        return render_template('signin.html')


@app.route('/record')
def record():
    if "username" in session:
        return render_template('record.html')
    else:
        return render_template('signin.html')

def objectIdDecoder(list):
  results=[]
  for document in list:
    document['_id'] = str(document['_id'])
    results.append(document)
  return results

@app.route('/record-get', methods=['GET'])
def recordGet():
    username = session['username']
    data = objectIdDecoder(list(db.contents.find({'username': username}).sort('number',-1)))
    return jsonify(data)

@app.route('/all-get', methods=['GET'])
def allGet():
    data = objectIdDecoder(list(db.contents.find({}).sort('number',-1)))
    return jsonify(data)

@app.route('/random', methods=['GET'])
def random():
    if "username" in session:
        return render_template('random.html')
    else:
        return render_template('signin.html')


@app.route('/record-post', methods=['POST'])
def recordPost():
    why = request.form['why']
    stat = request.form['stat']
    time = request.form['time']
    number = request.form['number']
    username = session['username']

    print(why, stat, time)
    doc = {'stat': stat, 'why': why, 'time': time, 'username' : username,'number':number}
    print(doc)
    db.contents.insert_one(doc)
    return jsonify({'hi': 'hi'})

@app.route('/delete', methods=['POST'])
def deleteDb():
    ID = request.form['id']
    print(ID)
    db.contents.delete_one({'_id': ObjectId(ID)})
    return jsonify({'result':'success'})

@app.route('/update', methods=['POST'])
def updateDb():
    ID = request.form['id']
    new_content = request.form['content']
    print(ID,new_content)
    db.contents.update({'_id': ObjectId(ID)},{'$set': {'why': new_content}})
    return jsonify({'result':'success'})

@app.route("/out")
def session_out():
    session.pop("username", None)
    return 'bye member!'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template, jsonify, request,session

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.feel
app.secret_key = "ABCDEFG"

@app.route('/')
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


@app.route('/record-get', methods=['GET'])
def recordGet():
    username = session['username']
    data = list(db.contents.find({'username': username}, {'_id': False}))
    return jsonify(data)


@app.route('/record-post', methods=['POST'])
def recordPost():
    why = request.form['why']
    stat = request.form['stat']
    time = request.form['time']
    username = session['username']
    print(why, stat, time)
    doc = {'stat': stat, 'why': why, 'time': time, 'username' : username}
    db.contents.insert_one(doc)
    return jsonify({'hi': 'hi'})

@app.route("/out")
def session_out():
    session.clear()
    return 'bye member!'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

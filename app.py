from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import bcrypt
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.qef1qmv.mongodb.net/?retryWrites=true&w=majority')
db = client.miniproject

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/join/user', methods=["post"])
def join_post():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']
    phone_receive = request.form['phone_give']

    # 비밀번호를 해싱하여 저장
    hashed_pw = bcrypt.hashpw(pw_receive.encode('utf-8'), bcrypt.gensalt())

    doc = {
        'id':id_receive,  
        'pw' : hashed_pw.decode('utf-8'),
        'name' : name_receive,
        'phone' : phone_receive   
    }
    db.user.insert_one(doc)
    
    return jsonify({'msg': '회원가입 완료!'})

@app.route("/login/user", methods=["POST"])
def login_post():
    id_receive = request.json['id']
    pw_receive = request.json['pw']
    
    user = db.user.find_one({'id': id_receive}, {'_id': False})
    
    if user and bcrypt.checkpw(pw_receive.encode('utf-8'), user['pw'].encode('utf-8')):
        session['user_id'] = id_receive
        session['user_name'] = user['name']  # 사용자 닉네임 세션에 저장
        return jsonify({'success': True, 'message': '로그인 성공'})

    else:
        return jsonify({'success': False, 'message': '로그인 실패'})
    
@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user_name' in session:
        # user_id = session['user_id']
        user_name = session['user_name']
        # 여기에서 해당 사용자 정보를 데이터베이스 등에서 가져와 사용할 수 있음
        return f'안녕하세요, {user_name}님! 프로필 페이지입니다.'
    else:
        return '로그인이 필요합니다.'

@app.route('/get_all_users')
def all_users():
    all_users = list(db.user.find({},{'_id':False}))
    return jsonify({'result': all_users})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
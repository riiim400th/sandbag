import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask import render_template, request, redirect, url_for ,session, abort
import jwt
import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"



@app.route("/")
def index_root():
    return render_template("root.html")

@app.route("/hoge")
def index():
    param = request.args.get("q")
    return render_template("index.html",param=param,text="text")

@app.route("/post/<text>", methods=['POST'])
def post_index(text):
    param = request.form["q"]
    return render_template("index.html",param=param,text=text)

@app.route("/post")
def get_post():
    return render_template("post.html")

@app.route("/post", methods=['POST'])
def post_post():
    username = request.form['username']
    password = request.form['password']
    return render_template('post.html', username=username, password=password)


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename:str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/uploaded_image/' + filename)  # 画像がアップロードされた後、その画像を表示するページにリダイレクト
        else:
            return 'Invalid file type'
    return render_template('upload.html')

@app.route('/uploaded_image/<filename>')
def uploaded_image(filename):
    return render_template('uploaded_image.html', filename=filename)

def is_logged_in():
    return True if session.get('logged_in') else False

def is_admin():
    return True if session.get('role') == 'admin' else False

@app.route('/login' ,methods=['POST'])
def logincheck():
    role = 0
    username = request.form['username']
    password = request.form['password']
    if username == 'hoge':
        if password == 'hoge':
            role = 1
    if username == 'admin':
        if password == 'admin':
            role = 2
    match role:
        case 0:
            return redirect(url_for('login_form'))
        case 1:
            session['logged_in'] = True
            session['role'] = 'user'
            return redirect(url_for('get_home'))
        case 2:
            session['logged_in'] = True
            session['role'] = 'admin'
            return redirect(url_for('get_admin_home'))
    # return render_template('home.html')

@app.route("/home")
def get_home():
    if is_logged_in():
        return render_template("home.html")
    else:
        abort(401)
        
@app.route("/admin_home")
def get_admin_home():
    # if is_logged_in() and is_admin():
    return render_template("admin.html")
    # else:
    #     abort(401)

# @app.route('/admin')
# def admin():
#     if is_logged_in() and is_admin():
#         return render_template('admin.html')
#     else:
#         abort(401)


@app.route('/login')
def login_form():
    return render_template('login.html')
    # session['logged_in'] = True
    # session['role'] = 'admin'  # ここを'user'に変更すれば一般ユーザーになります
    # return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('role', None)
    return redirect(url_for('login_form'))



##############################################################JWT

# 秘密鍵（実際の運用では環境変数などに保存）
SECRET_KEY = 'your_secret_key'
REFRESH_SECRET_KEY = 'your_refresh_secret_key'

# ユーザー情報の仮のデータベース
users = {
    "hoge": "hoge"
}

# ログインページ
@app.route('/jwt')
def home():
    return render_template('login_jwt.html')

# JWTを発行するエンドポイント
@app.route('/jwt/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 仮の認証処理
    if username in users and users[username] == password:
        access_token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=15)
        }, SECRET_KEY, algorithm='HS256')
        
        refresh_token = jwt.encode({
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, REFRESH_SECRET_KEY, algorithm='HS256')
        
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token})

    return jsonify({'message': 'Invalid credentials'}), 401

# リフレッシュトークンを使用して新しいアクセストークンを発行するエンドポイント
@app.route('/jwt/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing!'}), 403

    try:
        decoded = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=['HS256'])
        new_access_token = jwt.encode({
            'username': decoded['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=15)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'access_token': new_access_token})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token has expired!'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token!'}), 403

# JWT認証が必要なエンドポイント
@app.route('/jwt/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'message': 'Token is missing!'}), 403

    try:
        decoded_token = jwt.decode(token.split()[1], SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')  # トークンからユーザーIDを取得
        # ここで必要ならデータベースからユーザー情報を取得
        user_info = {
            'user_id': user_id,
            'username': 'example_user',  # これはデモ用。実際にはデータベースから取得
            'email': 'user@example.com'  # これはデモ用。実際にはデータベースから取得
        }
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 403
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 403

    # 成功時のレスポンスに重要な情報を含める
    return jsonify({
        'message': 'Access granted',
        'user_info': user_info,
        'resource_data': {
            'data_id': 123,
            'data_content': 'This is some protected data'
        }
    })


if __name__ == "__main__":
    print(' PEM pass phrase is "hoge"')
    app.run(host='localhost',debug=True, port=443, ssl_context=('.\certs\server.crt', '.\certs\server.key'))
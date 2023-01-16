from flask import Flask, render_template, url_for, redirect
from DataStore.MySQL import MySQL
import os
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
load_dotenv()


dns = {
    'host': os.getenv("HOST"),
    'user': os.getenv("USERNAME"),
    'passwd': os.getenv("PASSWORD"),
    'db': os.getenv("DATABASE"), 
}
# dns = {
#     'user': 'mysql',
#     'host': 'localhost',
#     'password': '123abc',
#     'database': 'kaggle'
# }

db = MySQL(**dns)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) #セッション情報を暗号化するための設定
csrf = CSRFProtect(app)


@app.route('/')
def main():
    props = {
        'title': 'Index.html',
        'msg': 'This page is index.html',
    }
    html = render_template('index.html', props=props)
    return html

@app.route('/hello')
def hello():
    props = {
        'title': 'Hello.html',
        'msg': 'This page is Hello.html',
    }
    html = render_template('hello.html', props=props)
    return html

@app.route('/users')
def users():
    props = {
        'title': 'User List',
        'msg': 'User List',
    }
    stmt = 'SELECT * FROM users'
    users =db.query(stmt)
    html = render_template('users.html', props=props, users=users)
    return html

@app.route('/users/<int:id>')
def user(id):
    props = {
        'title': 'User Information',
        'msg': 'User information',
    }
    stmt = 'SELECT * FROM users WHERE id = {}'.format(id)
    user = db.query(stmt)
    html = render_template('users-id.html', props=props, user=user[0:4])
    return html


#存在しないページへのアクセスのridirectの方法
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('main'))




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
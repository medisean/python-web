from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'abc'  # 设置用于 Flash 消息的密钥

# 用户信息存储（示例中使用全局变量，实际应使用数据库）
users = [{
        'username': 'admin',
        'password': generate_password_hash('123')
    }]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 在用户列表中查找匹配的用户名
        user = next((user for user in users if user['username'] == username), None)
        if user and check_password_hash(user['password'], password):
            flash('登录成功', 'success')
            return render_template('index.html')
        else:
            flash('用户名或密码错误', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # 表单验证
        if not username or not password or not confirm_password:
            flash('请填写所有字段', 'error')
        elif password != confirm_password:
            flash('密码与确认密码不匹配', 'error')
        elif any(user['username'] == username for user in users):
            flash('用户名已存在', 'error')
        else:
            # 将用户信息添加到列表中（实际应使用数据库存储）
            hashed_password = generate_password_hash(password)
            users.append({'username': username, 'password': hashed_password})
            flash('注册成功，请登录', 'success')
            return redirect('/login')

    return render_template('register.html')

@app.route('/')
def home():
    return render_template('login.html')
    # return 'Home page'

if __name__ == '__main__':
    app.run()
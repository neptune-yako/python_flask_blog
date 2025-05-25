import os
from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime
import markdown
import pymysql
from slugify import slugify
import random

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')

# 配置数据库连接
def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DATABASE_HOST', 'localhost'),
        user=os.getenv('DATABASE_USER', 'root'),
        password=os.getenv('DATABASE_PASSWORD', '123456'),
        db=os.getenv('DATABASE_NAME', 'python_flask_blog'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 添加上下文处理器，为所有模板提供当前时间
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# 配置Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 用户模型
class User:
    def __init__(self, id, username, email=None, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = is_admin
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, email, is_admin FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                return User(user['id'], user['username'], user['email'], user['is_admin'])
    finally:
        conn.close()
    return None

# 首页路由
@app.route('/')
def index():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT p.id, p.title, p.slug, p.excerpt, p.content, p.published_at, u.username "
                "FROM posts p JOIN users u ON p.user_id = u.id "
                "WHERE p.status = 'published' ORDER BY p.published_at DESC"
            )
            posts = cursor.fetchall()
            
            # 如果没有摘要，则从内容中提取
            for post in posts:
                if not post['excerpt']:
                    # 移除Markdown标记，并提取前150个字符作为摘要
                    content = post['content']
                    # 简单处理，实际可能需要更复杂的Markdown解析
                    content = content.replace('#', '').replace('*', '').replace('```', '')
                    post['excerpt'] = content[:150] + '...' if len(content) > 150 else content
    finally:
        conn.close()
    
    return render_template('index.html', posts=posts)

# 文章详情页
@app.route('/post/<slug>')
def post_detail(slug):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT p.id, p.title, p.content, p.published_at, u.username "
                "FROM posts p JOIN users u ON p.user_id = u.id "
                "WHERE p.slug = %s AND p.status = 'published'", (slug,)
            )
            post = cursor.fetchone()
            
            if not post:
                abort(404)
            
            # 将Markdown转换为HTML
            post['content_html'] = markdown.markdown(
                post['content'], 
                extensions=['fenced_code', 'codehilite']
            )
    finally:
        conn.close()
    
    return render_template('post_detail.html', post=post)

# 关于页面
@app.route('/about')
def about():
    return render_template('about.html')

# 小游戏页面
@app.route('/game')
def game():
    return render_template('game.html')

# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 验证表单数据
        if not username or not email or not password:
            flash('所有字段都是必填的', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('两次输入的密码不匹配', 'error')
            return render_template('register.html')
        
        # 检查用户名和邮箱是否已存在
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    flash('用户名或邮箱已被注册', 'error')
                    return render_template('register.html')
                
                # 创建新用户
                hashed_password = generate_password_hash(password)
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, hashed_password)
                )
                conn.commit()
                
                # 获取新创建的用户
                cursor.execute("SELECT id, username, email, is_admin FROM users WHERE username = %s", (username,))
                new_user = cursor.fetchone()
                
                # 自动登录
                user_obj = User(new_user['id'], new_user['username'], new_user['email'], new_user['is_admin'])
                login_user(user_obj)
                
                flash('注册成功！欢迎加入我们的博客社区', 'success')
                return redirect(url_for('index'))
        except Exception as e:
            flash(f'注册过程中出现错误: {str(e)}', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, username, email, password_hash, is_admin FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                
                if user:
                    # 对于演示目的，如果密码是'admin'且用户名是'admin'，直接登录
                    if username == 'admin' and password == 'admin':
                        user_obj = User(user['id'], user['username'], user['email'], user['is_admin'])
                        login_user(user_obj)
                        next_page = request.args.get('next')
                        return redirect(next_page or url_for('index'))
                    
                    # 验证密码
                    if check_password_hash(user['password_hash'], password):
                        user_obj = User(user['id'], user['username'], user['email'], user['is_admin'])
                        login_user(user_obj)
                        next_page = request.args.get('next')
                        return redirect(next_page or url_for('index'))
                
                flash('用户名或密码不正确', 'error')
        finally:
            conn.close()
    
    return render_template('login.html')

# 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功登出', 'info')
    return redirect(url_for('index'))

# 用户面板
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, title, status, created_at, updated_at FROM posts "
                "WHERE user_id = %s ORDER BY updated_at DESC",
                (current_user.id,)
            )
            posts = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('dashboard.html', posts=posts)

# 后台首页
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('您没有权限访问此页面', 'error')
        return redirect(url_for('dashboard'))
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT p.id, p.title, p.status, p.created_at, p.updated_at, u.username "
                "FROM posts p JOIN users u ON p.user_id = u.id "
                "ORDER BY p.updated_at DESC"
            )
            posts = cursor.fetchall()
    finally:
        conn.close()
    
    return render_template('admin/dashboard.html', posts=posts)

# 新建文章
@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        status = request.form.get('status')
        
        # 验证必填字段
        if not title or not content:
            flash('标题和内容为必填项', 'error')
            return render_template('editor.html', post=None)
        
        # 生成slug
        slug = request.form.get('slug') or slugify(title)
        
        # 发布时间
        published_at = datetime.now() if status == 'published' else None
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO posts (title, slug, content, excerpt, status, published_at, user_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (title, slug, content, excerpt, status, published_at, current_user.id)
                )
            conn.commit()
            flash('文章创建成功！', 'success')
            return redirect(url_for('dashboard'))
        except pymysql.err.IntegrityError as e:
            flash(f'创建文章失败: URL Slug已存在，请更换一个', 'error')
            return render_template('editor.html', post={'title': title, 'content': content, 'excerpt': excerpt, 'status': status})
        except Exception as e:
            flash(f'创建文章失败: {str(e)}', 'error')
            return render_template('editor.html', post={'title': title, 'content': content, 'excerpt': excerpt, 'status': status})
        finally:
            conn.close()
    
    return render_template('editor.html', post=None)

# 编辑文章
@app.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    conn = get_db_connection()
    try:
        # 检查文章是否存在且属于当前用户
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
            post = cursor.fetchone()
            
            if not post:
                abort(404)
            
            # 检查权限
            if post['user_id'] != current_user.id and not current_user.is_admin:
                flash('您没有权限编辑此文章', 'error')
                return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            title = request.form.get('title')
            content = request.form.get('content')
            excerpt = request.form.get('excerpt')
            status = request.form.get('status')
            old_slug = request.form.get('old_slug')
            new_slug = request.form.get('slug') or slugify(title)
            
            # 发布时间处理
            if status == 'published':
                # 检查文章之前是否已发布
                with conn.cursor() as cursor:
                    cursor.execute("SELECT status, published_at FROM posts WHERE id = %s", (post_id,))
                    post_status = cursor.fetchone()
                    
                    # 如果之前是草稿，现在发布，则设置发布时间
                    if post_status['status'] == 'draft' and post_status['published_at'] is None:
                        published_at = datetime.now()
                    else:
                        published_at = post_status['published_at']
            else:
                published_at = None
            
            # 更新文章
            with conn.cursor() as cursor:
                # 如果slug没有改变，或者新的slug不存在，则更新
                if old_slug == new_slug:
                    cursor.execute(
                        "UPDATE posts SET title = %s, content = %s, excerpt = %s, "
                        "status = %s, published_at = %s WHERE id = %s",
                        (title, content, excerpt, status, published_at, post_id)
                    )
                else:
                    # 检查新slug是否已存在
                    cursor.execute("SELECT id FROM posts WHERE slug = %s AND id != %s", (new_slug, post_id))
                    if cursor.fetchone():
                        flash('URL Slug已存在，请更换一个', 'error')
                        # 重新获取文章数据
                        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
                        post = cursor.fetchone()
                        return render_template('editor.html', post=post)
                    
                    cursor.execute(
                        "UPDATE posts SET title = %s, slug = %s, content = %s, excerpt = %s, "
                        "status = %s, published_at = %s WHERE id = %s",
                        (title, new_slug, content, excerpt, status, published_at, post_id)
                    )
            
            conn.commit()
            flash('文章更新成功！', 'success')
            return redirect(url_for('dashboard'))
        else:
            # 获取文章数据
            return render_template('editor.html', post=post)
    finally:
        conn.close()

# 删除文章
@app.route('/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    conn = get_db_connection()
    try:
        # 检查文章是否存在且属于当前用户
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id FROM posts WHERE id = %s", (post_id,))
            post = cursor.fetchone()
            
            if not post:
                abort(404)
            
            # 检查权限
            if post['user_id'] != current_user.id and not current_user.is_admin:
                flash('您没有权限删除此文章', 'error')
                return redirect(url_for('dashboard'))
            
            cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
        
        conn.commit()
        flash('文章已删除', 'success')
    finally:
        conn.close()
    
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('dashboard'))

# 猜数字游戏API
@app.route('/api/game/guess', methods=['POST'])
def guess_number():
    data = request.get_json()
    guess = data.get('guess')
    target = data.get('target')
    
    if not guess or not target:
        return jsonify({'error': '缺少必要参数'}), 400
    
    try:
        guess = int(guess)
        target = int(target)
    except ValueError:
        return jsonify({'error': '参数必须是数字'}), 400
    
    if guess < target:
        result = '猜小了'
    elif guess > target:
        result = '猜大了'
    else:
        result = '猜对了'
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True) 
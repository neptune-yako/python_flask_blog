# 简洁风个人博客

一个界面简洁、现代、具有扁平化设计风格的个人博客平台。

## 功能特点

- 简洁美观的前台界面，专注于内容阅读
- 卡片式文章展示，视觉效果更佳
- 支持用户注册和登录，每个用户都可以发布自己的文章
- 支持Markdown格式的文章编写
- 后台管理系统，方便管理文章
- 内置趣味小游戏（猜数字）
- 响应式设计，适配各种设备

## 技术栈

- 后端：Flask (Python 3.8+)
- 前端：HTML5, TailwindCSS, Vanilla JavaScript
- 数据库：MySQL
- 数据库连接：PyMySQL
- Markdown编辑器：EasyMDE
- 代码高亮：Prism.js

## 安装与运行

### 1. 克隆仓库

```bash
git clone https://github.com/neptune-yako/python_flask_blog.git
cd python_flask_blog
```

### 2. 创建虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

确保 `.env` 文件存在并包含正确的配置：

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=your_password_here
DATABASE_NAME=python_flask_blog
```

### 5. 初始化数据库

使用我们提供的脚本初始化数据库：

```bash
python run.py --init-db
```

或者手动在MySQL中执行 `schema.sql` 文件中的SQL语句。

### 6. 运行应用

```bash
python run.py
```

或者：

```bash
flask run
```

### 7. 访问博客

- 前台：http://localhost:5000
- 登录/注册：http://localhost:5000/login 或 http://localhost:5000/register
- 小游戏：http://localhost:5000/game
- 管理员账号：
  - 用户名：admin
  - 密码：admin

## 用户功能

### 注册与登录

- 用户可以注册新账号
- 登录后可以发布和管理自己的文章
- 管理员用户拥有额外的管理权限

### 文章管理

- 登录用户可以创建、编辑和删除自己的文章
- 支持草稿和发布两种状态
- 使用Markdown编辑器编写文章内容

### 小游戏

- 内置猜数字游戏，为博客增添趣味性
- 系统随机生成1-100之间的数字，用户通过多次猜测找出正确答案

## 项目结构

```
python_flask_blog/
├── app.py                 # Flask应用主文件
├── run.py                 # 启动脚本
├── requirements.txt       # Python依赖
├── schema.sql             # 数据库初始化脚本
├── .env                   # 环境变量配置
├── README.md              # 项目说明
└── templates/             # HTML模板
    ├── layout.html        # 基础布局
    ├── index.html         # 首页
    ├── login.html         # 登录页面
    ├── register.html      # 注册页面
    ├── dashboard.html     # 用户仪表盘
    ├── editor.html        # 文章编辑器
    ├── post_detail.html   # 文章详情页
    ├── about.html         # 关于页面
    ├── game.html          # 小游戏页面
    └── admin/             # 管理员模板
        ├── dashboard.html # 管理面板
```

## 设计特点

- 扁平化设计风格，视觉简洁现代
- 卡片式文章展示，增强用户体验
- 响应式布局，适配各种设备尺寸
- 微交互动效，提升用户体验

## 后续开发计划

- 添加文章分类和标签功能
- 实现评论系统
- 增加文章搜索功能
- 添加更多小游戏
- 集成图片上传和管理功能

## 许可证

MIT 

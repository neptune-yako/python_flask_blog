# 简洁风个人博客

一个界面简洁、现代、具有苹果官网设计风格的个人博客平台。

## 功能特点

- 简洁美观的前台界面，专注于内容阅读
- 支持Markdown格式的文章编写
- 后台管理系统，方便管理文章
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
git clone <repository-url>
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
- 后台管理：http://localhost:5000/admin/login
  - 用户名：admin
  - 密码：admin

## 常见问题解决

### 数据库连接错误

如果遇到数据库连接错误，请检查：

1. MySQL服务是否正在运行
2. `.env` 文件中的数据库配置是否正确
3. 数据库用户是否有权限访问指定的数据库

### 登录问题

默认管理员账号：
- 用户名：admin
- 密码：admin

如果无法登录，可能是数据库中的用户表未正确初始化，请重新运行初始化脚本。

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
    ├── post_detail.html   # 文章详情页
    ├── about.html         # 关于页面
    └── admin/             # 后台模板
        ├── login.html     # 登录页
        ├── dashboard.html # 管理面板
        └── editor.html    # 文章编辑器
```

## 使用说明

### 后台管理

1. 访问 `/admin/login` 登录后台（用户名：admin，密码：admin）
2. 在管理面板可以查看所有文章
3. 点击"新建文章"创建新的博客文章
4. 使用Markdown编辑器编写文章内容
5. 设置文章状态（草稿/发布）
6. 保存文章

### 前台浏览

1. 首页显示所有已发布的文章
2. 点击文章标题或"阅读全文"查看完整文章
3. "关于"页面展示博主信息

## 后续开发计划

- 添加文章分类和标签功能
- 实现评论系统
- 增加文章搜索功能
- 添加用户管理功能，支持多用户
- 集成图片上传和管理功能

## 许可证

MIT 
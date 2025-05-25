-- 创建数据库
CREATE DATABASE IF NOT EXISTS python_flask_blog DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE python_flask_blog;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建文章表
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    excerpt VARCHAR(500),
    status ENUM('draft', 'published') NOT NULL DEFAULT 'draft',
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 创建初始管理员用户 (密码为 'admin')
INSERT INTO users (username, password_hash) VALUES ('admin', '$2b$12$1xxxxxxxxxxxxxxxxxxxxuZLbwxnpY0o58unSvIPxddLxGystU2');

-- 创建一些示例文章
INSERT INTO posts (title, slug, content, excerpt, status, published_at, user_id)
VALUES 
('欢迎来到我的博客', 'welcome-to-my-blog', 
'# 欢迎来到我的博客\n\n这是我的第一篇博客文章。在这里，我将分享我的想法、经验和知识。\n\n## 为什么要写博客？\n\n写博客可以帮助我整理思路，分享知识，与他人交流。\n\n```python\nprint("Hello, World!")\n```', 
'这是我的第一篇博客文章，介绍了为什么我要开始写博客。', 
'published', NOW(), 1),

('如何使用Python进行数据分析', 'how-to-use-python-for-data-analysis', 
'# 如何使用Python进行数据分析\n\n在这篇文章中，我将介绍如何使用Python的pandas和matplotlib库进行数据分析和可视化。\n\n## 安装必要的库\n\n```bash\npip install pandas matplotlib\n```\n\n## 读取数据\n\n```python\nimport pandas as pd\n\ndf = pd.read_csv("data.csv")\nprint(df.head())\n```', 
'本文介绍了如何使用Python的pandas和matplotlib库进行数据分析和可视化。', 
'published', NOW(), 1); 
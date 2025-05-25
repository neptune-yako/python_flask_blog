个人博客项目开发需求文档 (DRD)
版本: 1.0
日期: 2025年5月26日
制定者: (您的 AI 助手)

1. 项目概述 (Project Overview) 📝
项目名称: 简洁风个人博客 (Minimalist Personal Blog)

项目目标: 开发一个界面简洁、现代、具有苹果官网设计风格的个人博客平台。用户（博主）可以通过后台管理文章，访问者可以流畅地浏览文章。

核心价值:

简洁美学: 提供干净、专注阅读的体验。

易于管理: 博主可以轻松发布和管理内容。

高性能: 快速加载，响应迅速。

目标用户:

博主 (Admin): 拥有博客，希望通过一个简洁的平台发布和管理自己的文章。

访问者 (Visitor): 对博主内容感兴趣，希望获得舒适阅读体验的用户。

2. 技术栈确认 (Technology Stack) 💻
后端框架: Flask (Python 3.8)

前端框架/库: HTML5, TailwindCSS, Vanilla JavaScript (或根据需要引入轻量级库), CSS3

数据库: MySQL

数据库连接库: PyMySQL

运行环境: Python 3.8+

服务器 (建议):本地

3. 功能需求 (Functional Requirements) ⚙️
3.1 前台功能 (Frontend Features)
首页 (Home Page):

以列表形式展示已发布的文章，按发布时间倒序排列。

每篇文章显示标题、摘要（或正文前 N 个字符）、发布日期。

提供分页功能（如果文章数量较多）。

简洁的页头 (Header)，包含博客名称/Logo 和导航（如：首页、关于）。

简洁的页脚 (Footer)，包含版权信息等。

文章详情页 (Post Detail Page):

显示完整的文章标题和内容。

显示文章发布日期。

支持代码块高亮显示。

（可选）支持评论区（初期可不做）。

关于页面 (About Page):

静态页面，展示博主的个人介绍。

3.2 后台管理功能 (Backend/Admin Features)
登录 (Login):

提供一个安全的登录页面供博主登录。

进行用户名和密码验证。

使用 Session 或 Token 进行会话管理。

文章管理 (Post Management):

列表: 显示所有文章（包括草稿和已发布），包含标题、状态、创建/修改日期。

新建: 提供一个富文本编辑器（或 Markdown 编辑器）用于撰写新文章，可以设置标题、正文、URL Slug（自动生成或手动指定）、状态（草稿/发布）。

编辑: 修改现有文章的内容和属性。

删除: 删除文章（可加入回收站或二次确认机制）。

（可选）分类/标签管理 (Category/Tag Management):

（初期可简化，暂不实现）未来可添加对文章进行分类或打标签的功能。

4. 非功能需求 (Non-Functional Requirements) ✨
设计与风格 (Design & Style):

核心: 模仿 Apple 官网风格。

布局: 大量留白，网格系统布局，视觉焦点突出。

色彩: 以黑、白、灰为主色调，搭配少量点缀色（如蓝色链接）。

字体: 使用优雅、清晰的无衬线字体 (San Francisco-like or system fonts)。字号对比明显，易于阅读。

动效: 少量、平滑、有意义的过渡效果和微交互 (e.g., hover effects, page transitions)。

图片: 如果使用图片，需要高质量且与整体风格协调。

性能 (Performance):

页面加载速度快，API 响应时间短。

优化数据库查询。

前端资源（CSS, JS）进行压缩。

响应式设计 (Responsive Design):

界面能自适应不同尺寸的设备（桌面、平板、手机）。

安全性 (Security):

后台登录防止暴力破解。

防止 SQL 注入和 XSS 攻击。

密码存储使用哈希加盐。

易用性 (Usability):

前台导航清晰，阅读流畅。

后台管理操作直观，易于上手。

5. 数据库设计 (Database Schema - MySQL) 🗄️
数据库名: personal_blog_db

users 表 (存储管理员信息):

id (INT, PRIMARY KEY, AUTO_INCREMENT)

username (VARCHAR(50), UNIQUE, NOT NULL)

password_hash (VARCHAR(255), NOT NULL)

created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

posts 表 (存储文章信息):

id (INT, PRIMARY KEY, AUTO_INCREMENT)

title (VARCHAR(255), NOT NULL)

slug (VARCHAR(255), UNIQUE, NOT NULL) - 用于 URL，方便 SEO 和访问

content (TEXT, NOT NULL) - 文章正文

excerpt (VARCHAR(500), NULL) - 文章摘要

status (ENUM('draft', 'published'), NOT NULL, DEFAULT 'draft') - 文章状态

published_at (TIMESTAMP, NULL) - 发布时间

created_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

updated_at (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

user_id (INT, NOT NULL, FOREIGN KEY REFERENCES users(id)) - 作者 ID

(注: 初期可简化，user_id 可暂时不做，假设只有一个管理员。如果只有一个管理员，users 表和 posts 表中的 user_id 字段可以暂时移除，待后续扩展时再加入。)

6. 系统架构与 API 设计 (Architecture & API Design) 🏗️
6.1 架构
前端 (Client): 使用 HTML 模板（由 Flask 渲染）、TailwindCSS 进行样式设计，JavaScript 实现交互。

后端 (Server - Flask): 处理业务逻辑，直接渲染 HTML 模板。通过 PyMySQL 与 MySQL 数据库交互。

(注: 考虑到“简洁”和初期开发效率，我们优先采用 Flask 后端渲染模板的方式，而非前后端分离。如果后续有明确需求，可以再调整为 RESTful API + 前端 JS 框架的模式。)

6.2 路由设计 (Flask Routes)
前台路由:

GET / - 首页，展示文章列表。

GET /post/<slug> - 文章详情页。

GET /about - 关于页面。

后台路由 (需要登录保护):

GET /admin/login - 显示登录页面。

POST /admin/login - 处理登录请求。

GET /admin/logout - 处理登出请求。

GET /admin/dashboard - 后台管理主页，展示文章列表。

GET /admin/post/new - 显示新建文章页面。

POST /admin/post/new - 处理新建文章请求。

GET /admin/post/edit/<int:post_id> - 显示编辑文章页面。

POST /admin/post/edit/<int:post_id> - 处理编辑文章请求。

POST /admin/post/delete/<int:post_id> - 处理删除文章请求。

7. 前端设计与实现 (Frontend Design & Implementation) 🎨
模板引擎: Flask 自带的 Jinja2。

CSS 框架: TailwindCSS。需要配置 tailwind.config.js 以定制颜色、字体、间距，使其更贴近 Apple 风格。

颜色: 定义主色（如 #FFFFFF 白, #000000 黑, #F5F5F7 浅灰, #1D1D1F 深灰）、强调色（如 #007AFF 苹果蓝）。

字体: 设置 font-family 优先使用系统 UI 字体，如 ['system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif']。

间距: 参考 Apple HIG (Human Interface Guidelines) 定义符合其设计感的间距单位。

HTML 结构:

templates/layout.html: 定义基础布局（Header, Footer, 主要内容区域，引入 TailwindCSS 和 JS）。

templates/index.html: 首页，继承 layout.html。

templates/post_detail.html: 文章详情页，继承 layout.html。

templates/about.html: 关于页面，继承 layout.html。

templates/admin/login.html: 登录页。

templates/admin/dashboard.html: 后台管理主页，继承 layout.html (或有独立的 admin layout)。

templates/admin/editor.html: 文章编辑器页 (新建/编辑)，继承 layout.html (或 admin layout)。

JavaScript:

用于微交互，如导航栏的响应式处理、按钮的点击效果。

如果使用富文本编辑器，需要集成相应的 JS 库 (例如 TinyMCE, CKEditor 的轻量版，或纯 Markdown 编辑器如 SimpleMDE/EasyMDE 并配合后端 Markdown 解析)。

如果需要代码高亮，需要集成如 highlight.js 或 Prism.js，并在文章渲染时应用。

8. 开发环境与部署 (Dev & Deployment) 🚀
环境管理: 使用 venv 或 conda 创建独立的 Python 3.8 环境。

依赖管理: 使用 requirements.txt 文件列出所有 Python 依赖 (Flask, PyMySQL, Flask-Login (用于认证), python-dotenv (用于配置), Markdown (如果使用 Markdown 编辑器) 等)。

配置管理: 数据库连接信息、SECRET_KEY 等敏感信息通过 .env 文件和 python-dotenv 库加载，不要硬编码。.env 文件应加入 .gitignore。

数据库初始化: 提供 SQL 脚本或 Flask-Migrate (如果模型较复杂或需要演进) 来创建和迁移数据库表。初期可手动创建。

运行:

开发环境: flask run (开启 Debug 模式)。

生产环境: 使用 Gunicorn 或 uWSGI 运行 Flask 应用，并使用 Nginx 作为反向代理和静态文件服务器。

TailwindCSS:

安装 TailwindCSS CLI。

配置 tailwind.config.js。

创建 input.css 文件引入 Tailwind 指令。

运行构建命令 (e.g., npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch) 将 TailwindCSS 的指令转换为最终的 output.css 文件，并在 HTML 中链接此文件。

9. 下一步与确认 (Next Steps & Confirmation) ✅
请您仔细审阅以上文档。

设计风格细节: 对于 "Apple 官网风格"，我们理解为：极简、大量留白、高质量排版（清晰的字体层级和对比）、中性色调（黑白灰为主，辅以品牌蓝等点缀色）、平滑且有意义的微动效。这个理解是否准确？是否有特定的 Apple 页面或元素作为主要参考？

后台文章编辑器: 您倾向于使用 Markdown 编辑器 (更轻量，适合技术写作) 还是 所见即所得 (WYSIWYG) 富文本编辑器 (操作更直观，类似 Word)？

简化与迭代: 我们已将分类/标签管理、评论功能、多用户等列为可选或后期迭代内容，以确保初期版本的核心功能和简洁性。这是否符合您的预期？

数据库用户表: 初期如果仅为单博主使用，users 表可以简化，甚至可以先将管理员账户信息硬编码或通过简单配置文件管理，待有实际需求再完善用户系统和 user_id 关联。您对此有何看法？

您的确认将帮助我们确保 AI 工具能够准确、高效地进行后续的代码开发工作。期待您的反馈！
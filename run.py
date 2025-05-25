import os
import pymysql
from dotenv import load_dotenv
import subprocess
import sys

# 加载环境变量
load_dotenv()

def init_db():
    """初始化数据库"""
    print("正在初始化数据库...")
    
    # 检查是否已经存在数据库
    try:
        # 先连接到MySQL服务器（不指定数据库）
        conn = pymysql.connect(
            host=os.getenv('DATABASE_HOST', 'localhost'),
            user=os.getenv('DATABASE_USER', 'root'),
            password=os.getenv('DATABASE_PASSWORD', '123456'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with conn.cursor() as cursor:
            # 创建数据库（如果不存在）
            cursor.execute("CREATE DATABASE IF NOT EXISTS python_flask_blog DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            
            # 使用该数据库
            cursor.execute("USE python_flask_blog")
            
            # 检查users表是否存在
            cursor.execute("SHOW TABLES LIKE 'users'")
            if not cursor.fetchone():
                # 如果不存在，创建表并插入初始数据
                with open('schema.sql', 'r', encoding='utf-8') as f:
                    # 按分号分割SQL语句
                    sql_commands = f.read().split(';')
                    for command in sql_commands:
                        if command.strip():
                            cursor.execute(command)
                            conn.commit()
                print("数据库表已创建并初始化。")
            else:
                print("数据库表已存在，跳过初始化。")
        
        conn.close()
        print("数据库初始化完成！")
        return True
    
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        return False

def run_app():
    """运行Flask应用"""
    print("正在启动博客应用...")
    from app import app
    app.run(debug=True)

if __name__ == "__main__":
    # 如果命令行参数包含--init-db，则初始化数据库
    if len(sys.argv) > 1 and sys.argv[1] == '--init-db':
        if init_db():
            print("数据库初始化成功！")
        else:
            print("数据库初始化失败，请检查数据库连接配置。")
    else:
        # 尝试连接数据库，如果失败则提示初始化
        try:
            conn = pymysql.connect(
                host=os.getenv('DATABASE_HOST', 'localhost'),
                user=os.getenv('DATABASE_USER', 'root'),
                password=os.getenv('DATABASE_PASSWORD', '123456'),
                db=os.getenv('DATABASE_NAME', 'python_flask_blog'),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            conn.close()
            # 数据库连接成功，运行应用
            run_app()
        except Exception as e:
            print(f"无法连接到数据库: {e}")
            print("请先运行 'python run.py --init-db' 初始化数据库，或检查数据库连接配置。") 
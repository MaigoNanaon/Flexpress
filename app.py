from flask import Flask, render_template

# 创建 Flask 应用
app = Flask(__name__, template_folder='.')

# 定义路由，渲染 templates/index.html 文件
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # 运行 Flask 应用
    app.run(host='0.0.0.0', port=8500, debug=True)
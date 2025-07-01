from flask import Flask, render_template, request, jsonify, session, redirect
from werkzeug.utils import secure_filename
from datetime import timedelta
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from pathlib import Path
import m_dlib.face_marks as fmarks
from u_2_net import my_u2net_test
from to_background import to_background
from to_background import to_standard_trimap
from m_dlib import ai_crop
import os

app = Flask(__name__)
app.secret_key = "s3cr3t_k3y_9817231"

# 设置允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 设置静态文件缓存过期时间
app.send_file_max_age_default = timedelta(seconds=1)

# 确保静态图片目录存在
static_images_dir = Path(__file__).parent / 'static' / 'images'
static_images_dir.mkdir(parents=True, exist_ok=True)


@app.route('/check_login')
def check_login():
    if 'user_id' in session:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],))
        user = cursor.fetchone()
        return jsonify({"logged_in": True, "username": user["username"]})
    return jsonify({"logged_in": False})

@app.route('/')
@login_required
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
@login_required  # 新增登录保护
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"error": True, "msg": "没有选择文件"}), 400

        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": True, "msg": "图片类型：png、PNG、jpg、JPG、bmp"}), 400

        # 参数获取
        size_type = request.form.get('size', '1inch')
        bg_color = request.form.get('bgColor', 'blue')

        # 安全保存上传图片
        original_filename = secure_filename(f.filename)
        base_filename = Path(original_filename).stem
        original_path = static_images_dir / original_filename
        f.save(original_path)

        # 中间图像处理路径
        alpha_img = static_images_dir / f"{base_filename}_alpha.png"
        alpha_resize_img = static_images_dir / f"{base_filename}_alpha_resize.png"
        trimap = static_images_dir / f"{base_filename}_trimap.png"
        id_image = static_images_dir / f"{base_filename}_id.png"
        processed_filename = f"processed_{original_filename}"
        deal_img = static_images_dir / processed_filename

        # 处理流程
        my_u2net_test.seg_trimap(str(original_path), str(alpha_img), str(alpha_resize_img))
        to_standard_trimap.to_standard_trimap(str(alpha_resize_img), str(trimap))
        to_background.to_background(str(original_path), str(trimap), str(id_image), bg_color)

        # 尺寸映射表
        SIZE_MAP = {
            '1inch': (295, 413, 'blue', (5, 7)),
            '2inch': (413, 626, 'blue', (5, 7)),
            'passport': (413, 531, 'white', (11, 46)),
            'visa_us': (600, 600, 'red', (1, 1)),
            'visa_uk': (826, 1063, 'red', (35, 45)),
        }

        if size_type not in SIZE_MAP:
            return jsonify({'error': True, 'msg': f'未知的尺寸类型: {size_type}'}), 400

        size_width, size_height, cl, size_tuple = SIZE_MAP[size_type]
        size3 = size_tuple[1]

        # 使用 Dlib 检测人脸框
        shape, d = fmarks.predictor_face(str(original_path))

        # 获取人脸框的宽度和高度
        face_width = d.right() - d.left()
        face_height = d.bottom() - d.top()

        
       
        # 计算裁剪区域的宽高
        scale_ratio = 2.8  
        

        # 计算新的裁剪区域尺寸
        half_width = int(face_width * scale_ratio )
        half_height = int(face_height * scale_ratio )

        # 计算图像中心点
        X_CENTRE = d.left() + (d.right() - d.left()) / 2
        Y_CENTER = d.top() + (d.bottom() - d.top()) / 2
        print(f"检测到的人脸宽度: {face_width}, 高度: {face_height}")
        print(f"裁剪区域: 中心点 ({X_CENTRE}, {Y_CENTER}), 宽高 ({half_width}, {half_height})")
        print(f"size_tuple:{size_tuple}")
        print(f"size3:{size3}")
        print(f"传入 ai_crop 的尺寸: {size_width}x{size_height}")  # 输出正确的尺寸

        # ✅ 替换原调用
        ai_crop.crop_photo(
            str(id_image),
            str(deal_img),
            size_width,
            size_height,
            cl,
            size3,
            scale_ratio
        )

        return jsonify({
            "error": False,
            "original_img": f"/static/images/{original_filename}",
            "processed_img": f"/static/images/{processed_filename}"
        })

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

def apology(message, code=400):
    return f"{code}: {message}", code

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("必须提供用户名", 403)
        elif not password:
            return apology("必须提供密码", 403)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = cursor.fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("无效的用户名或密码", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not all([username, password, confirmation]):
            return apology("请填写所有字段", 400)
        if password != confirmation:
            return apology("两次密码不一致", 400)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return apology("用户名已存在", 400)

        cursor.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        conn.commit()
        return redirect("/login")

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    init_db()  # 确保数据库初始化
    app.run(debug=True)

# from flask import Flask, render_template, request, jsonify, session, redirect
# from werkzeug.utils import secure_filename
# from datetime import timedelta
# import sqlite3
# from werkzeug.security import check_password_hash, generate_password_hash
# from helpers import login_required

# from u_2_net import my_u2net_test
# from to_background import to_background
# from to_background import to_standard_trimap
# from m_dlib import ai_crop
# import os
# app = Flask(__name__)
# app.secret_key = "s3cr3t_k3y_9817231"  # 示例


# # 输出
# @app.route('/')
# @login_required
# def index():
#     return render_template("index.html")


# # 设置允许的文件格式
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# # 设置静态文件缓存过期时间
# app.send_file_max_age_default = timedelta(seconds=1)

# # 添加路由
# @app.route('/upload', methods=['POST', 'GET'])
# def upload():
#     # 通过file标签获取上传的文件
#     f = request.files['file']
#     if not (f and allowed_file(f.filename)):
#         return jsonify({"error": 1001, "msg": "图片类型：png、PNG、jpg、JPG、bmp"})
#     # 当前文件所在路径
#     basepath = os.path.dirname(__file__)


#     # 一定要先创建该文件夹，不然会提示没有该路径
#     upload_path = os.path.join(basepath, 'static\images', original_filename)
#     print(upload_path)
#     # 保存文件
#     f.save(upload_path)

#     org_img = upload_path
#     alpha_img =os.path.join(basepath, 'static\images\meinv_alpha.png')

#     #alpha_resize_img = "img\meinv_alpha_resize.png"
#     alpha_resize_img = os.path.join(basepath, 'static\images\size_re.png')
#     # #
#     # 通过u_2_net 获取 alpha
#     my_u2net_test.seg_trimap(org_img, alpha_img, alpha_resize_img)
#     #
#     print("-----------------------------")
#     # # 通过alpha 获取 trimap
#     trimap =os.path.join(basepath, 'static\images\meinv_trimap_resize.png')
#     to_standard_trimap.to_standard_trimap(alpha_resize_img, trimap)
#     #
#     # 证件照添加蓝底纯色背景
#     id_image=os.path.join(basepath, 'static\images\meinv_id.png')
#     to_background.to_background(org_img, trimap, id_image, "blue")
#     # id_image = "..\\aiphoto\\img\\meinv_id_grid.png"
#     # to_background.to_background_grid(org_img, trimap, id_image)
#     # image = Image.open(id_image)
#     # data = image.getdata()
#     # np.savetxt("data6.txt", data,fmt='%d',delimiter=',')

#     # 20200719
#     # 通过识别人脸关键点，裁剪图像
#     processed_filename = 'processed_' + secure_filename(f.filename)
#     deal_img_path = os.path.join(basepath, 'static', 'images', processed_filename)
#     ai_crop.crop_photo(id_image, deal_img_path)


#     # 返回上传成功界面
#     return render_template("index.html",
#                          original_img=f"/static/images/{secure_filename(f.filename)}",
#                          processed_img=f"/static/images/{processed_filename}")

#     print("处理后图片路径：", processed_filename)


# # 重新返回上传界面

# def apology(message, code=400):
#     return f"{code}: {message}", code

# def get_db():
#     conn = sqlite3.connect("users.db")  # 使用你刚创建的数据库文件
#     conn.row_factory = sqlite3.Row  # 让查询结果像字典一样使用
#     return conn

# # 创建数据库（文件名：users.db）
# conn = sqlite3.connect("users.db")
# cursor = conn.cursor()

# # 创建 users 表（如果不存在）
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT NOT NULL UNIQUE,
#     hash TEXT NOT NULL
# )
# """)

# # 保存更改并关闭连接
# conn.commit()
# conn.close()


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     # Forget any user_id
#     session.clear()

#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")

#         # Ensure username was submitted
#         if not username:
#             return apology("must provide username", 403)

#         # Ensure password was submitted
#         elif not password:
#             return apology("must provide password", 403)

#         # Connect to database and query for user
#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
#         rows = cursor.fetchall()

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
#             return apology("invalid username and/or password", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
#         return redirect("/")

#     else:
#         return render_template("login.html")
    
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     """Register user"""
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         confirmation = request.form.get("confirmation")

#         if not username or not password or not confirmation:
#             return apology("everything must be full", 400)

#         if password != confirmation:
#             return apology("password and confirmation are not the same", 400)

#         conn = get_db()
#         cursor = conn.cursor()

#         # 检查用户名是否已存在
#         cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
#         rows = cursor.fetchall()

#         if len(rows) > 0:
#             conn.close()
#             return apology("this username has been used", 400)

#         # 插入新用户
#         hash_password = generate_password_hash(password)
#         cursor.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash_password))
#         conn.commit()
#         conn.close()

#         return redirect("/login")

#     else:
#         return render_template("register.html")

# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")


# @app.route('/help')
# def help_page():
#     return render_template('help.html')


# @app.route('/about')
# def about_page():
#     return render_template('about.html')



# if __name__ == '__main__':
#     app.run(debug=True)

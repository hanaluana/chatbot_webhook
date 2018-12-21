from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route('/signup', methods=['GET','POST'])
def signup():
    email=request.form.get('email')
    password=request.form.get('password')
    
    adminEmail="qwer@qwer.com"
    adminPassword = "12341234"
    
    if adminEmail==email and password==adminPassword:
        msg='관리자님 환영합니다!'
    else:
        if adminEmail==email:
            msg='관리자님 비번 틀림 빨리 뇌 청소 하셈'
        else:
            msg='넌 그냥 꺼져'
        
    return render_template("signup.html", msg=msg)
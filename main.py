
from flask import make_response,Flask, request, render_template, redirect, url_for, flash,Blueprint,Markup,send_from_directory
from sqlalchemy_searchable import search
from flask_login import UserMixin, LoginManager, login_required, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from password_strength import PasswordPolicy,PasswordStats
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from module import update1 ,update2

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql:///Admission"
app.config['SQLALCHEMY_POOL_RECYCLE'] = 90
db = SQLAlchemy(app)


# DB # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class UserScoreModel(db.Model):
    __tablename__ = 'UserScore'
    pid = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30),nullable=False,unique=True)
    score = db.Column(db.JSON, nullable=True)
    def __init__(self,user,score):
        self.user = user
        self.score = score

    @classmethod    
    def find_by_user(cls, user):
        return cls.query.filter_by(user = user).first()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()     
class ScoreLevelModel(db.Model):
    __tablename__ = 'ScoreLevel'
    pid = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(30),nullable=False,unique=True)
    Level = db.Column(db.JSON, nullable=False)
    def __init__(self,year,Level):
        self.year = year
        self.Level = Level

    @classmethod    
    def find_by_year(cls, year):
        return cls.query.filter_by(year = year).first()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()   

class FavModel(db.Model):
    __tablename__ = 'Favorite'
    pid = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30),nullable=False)
    favid = db.Column(db.String(30),nullable=True )
    def __init__(self,user,favid):
        self.user = user
        self.favid = favid

    @classmethod    
    def find_by_user(cls, user):
        return cls.query.filter_by(user = user)
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()     

class FavModelstar(db.Model):
    __tablename__ = 'StarFavorite'
    pid = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(30),nullable=False)
    favid = db.Column(db.String(30),nullable=True )
    def __init__(self,user,favid):
        self.user = user
        self.favid = favid

    @classmethod    
    def find_by_user(cls, user):
        return cls.query.filter_by(user = user)
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()


class NewsModel(db.Model):
    __tablename__ = 'news'
    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30),nullable=False)
    content = db.Column(db.String(4294967295),nullable=True )
    date = db.Column(db.String(100), nullable=False)
    tag= db.Column(db.String(30), nullable=False)
    tag_type=db.Column(db.String(30), nullable=False, default="info")
    def __init__(self,title,content, date, tag,tag_type):
        self.title = title
        self.content = content
        self.date = date
        self.tag = tag
        self.tag_type = tag_type
    @classmethod
    def find_by_id(cls, pid):
        return cls.query.filter_by(pid = pid).first()
    @classmethod
    def find_by_tag(cls, tag):
        return cls.query.filter_by(tag = tag)
    @classmethod
    def get_all_new(cls):
        return cls.query.all()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()


class DepartmentModel(db.Model):
    __tablename__ = 'Department'
    pid = db.Column(db.Integer, primary_key=True)
    schoolid = db.Column(db.String(30),nullable=False )
    code = db.Column(db.String(30),nullable=False )
    name = db.Column(db.String(30),nullable=False )
    url = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(30),nullable=False )
    detail= db.Column(db.JSON, nullable=True)


    def __init__(self,year,code,name,url,detail,schoolid):
        self.code = code
        self.year = year
        self.name = name
        self.url = url
        self.detail = detail
        self.schoolid = schoolid
        self.id = id
    @classmethod
    def find_by_schoolid(cls, schoolid):
        return cls.query.filter_by(schoolid = schoolid) 
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name.contains(str(name)))
    @classmethod    
    def find_by_year(cls, year):
        return cls.query.filter_by(year = year)
    @classmethod    
    def find_by_id(cls, code):
        return cls.query.filter_by(code = code).first()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()     

class Department2Model(db.Model):
    __tablename__ = 'Department2'
    pid = db.Column(db.Integer, primary_key=True)
    schoolid = db.Column(db.String(30),nullable=False )
    code = db.Column(db.String(30),nullable=False )
    name = db.Column(db.String(30),nullable=False )
    url = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(30),nullable=False )
    detail= db.Column(db.JSON, nullable=True)
    group_= db.Column(db.String(30),nullable=False )


    def __init__(self,year,code,name,url,detail,schoolid,group_):
        self.code = code
        self.year = year
        self.name = name
        self.url = url
        self.detail = detail
        self.schoolid = schoolid
        self.id = id
        self.group_=group_
    @classmethod
    def find_by_schoolid(cls, schoolid):
        return cls.query.filter_by(schoolid = schoolid) 
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()
    @classmethod    
    def find_by_year(cls, year):
        return cls.query.filter_by(year = year)
    @classmethod    
    def find_by_id(cls, code):
        return cls.query.filter_by(code = code).first()
    @classmethod    
    def get_all(cls):
        return cls.query.all()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()     


class SchoolsModel(db.Model):
    __tablename__ = 'schools'
    pid = db.Column(db.Integer, primary_key=True)
    schoolid = db.Column(db.String(30),unique=True,nullable=False)
    name = db.Column(db.String(30),unique=True,nullable=False )
    zone = db.Column(db.String(30), nullable=False)
    isNational= db.Column(db.String(30), nullable=False)
    official_website = db.Column(db.String(255), nullable=True)
    def __init__(self,schoolid,name, zone, isNational,official_website):
        self.schoolid = schoolid
        self.name = name
        self.zone = zone
        self.isNational = isNational
        self.official_website = official_website

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()
    @classmethod    
    def find_by_id(cls, schoolid):
        return cls.query.filter_by(schoolid = schoolid).first()
    @classmethod    
    def get_all_school(cls):
        return cls.query.all()        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()     


class Schools2Model(db.Model):
    __tablename__ = 'Schools2'
    pid = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(30),nullable=False)
    schoolid = db.Column(db.String(30),nullable=False)
    group1 = db.Column(db.String(30),nullable=True)
    group2 = db.Column(db.String(30),nullable=True)
    group3 = db.Column(db.String(30),nullable=True)
    starpercentage = db.Column(db.String(30),nullable=True )
    name = db.Column(db.String(30),nullable=False )
    zone = db.Column(db.String(30), nullable=True)
    isNational= db.Column(db.String(30), nullable=False)
    official_website = db.Column(db.String(255), nullable=True)
    def __init__(self,year,group1,group2,group3,schoolid,name,starpercentage, zone, isNational,official_website):
        self.year = year
        self.group1 = group1
        self.group2 = group2
        self.group3 = group3
        self.schoolid = schoolid
        self.starpercentage = starpercentage
        self.name = name
        self.zone = zone
        self.isNational = isNational
        self.official_website = official_website

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name)
    @classmethod    
    def find_by_id(cls, schoolid):
        return cls.query.filter_by(schoolid = schoolid).first()
    @classmethod    
    def find_by_year(cls, year):
        return cls.query.filter_by(year = year)
    @classmethod    
    def get_school_by_group1(cls,group1):
        return cls.query.filter_by(group1 = group1)        
    @classmethod    
    def get_school_by_group2(cls,group2):
        return cls.query.filter_by(group2 = group2)        
    @classmethod    
    def get_school_by_group3(cls,group3):
        return cls.query.filter_by(group3 = group3)        
    @classmethod    
    def get_all_school(cls):
        return cls.query.all()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()     


class UserModel(db.Model):
    __tablename__ = 'users'
    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(255),unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False)
    school=db.Column(db.String(30), nullable=True)
    def __init__(self, name, email, password,role,school):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.school = school
    @classmethod    
    def get_all_user(cls):
        return cls.query.all()
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first()
    @classmethod    
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()        

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def get_star_school(type=""):
    if type=="??????????????????":
        query =Schools2Model.get_all_school()
    elif type=="?????????????????????":
        query =Schools2Model.get_school_by_group1("True")
    elif type=="?????????????????????":
        query =Schools2Model.get_school_by_group2("True")
    elif type=="?????????????????????":
        query =Schools2Model.get_school_by_group3("True")
    if query:
        allschool=[]
        for school in query:
            a={"id":school.schoolid,"SchoolName":school.name,"zone":school.zone,"star":school.starpercentage,"isNational":school.isNational,"official_website":school.official_website}
            allschool.append(a)
        return allschool
    return ""
def get_star_department(id="",group=""):
    if id!="":
        query =Department2Model.find_by_schoolid(id)
    else:
        query =Department2Model.get_all()
    if query:
        if group=="???????????????" or group=="???????????????" or group=="???????????????":
            alldepartment=[]
            for department in query:
                if group==department.group_:       
                    a={"schoolid":department.schoolid,"name":department.name,"url":department.url,"detail":department.detail}
                    alldepartment.append(a)
        elif group=="????????????":
            alldepartment=[]
            for department in query:
                a={"schoolid":department.schoolid,"name":department.name,"url":department.url,"detail":department.detail}
                alldepartment.append(a)            
        return alldepartment
    return ""

# fuc
def get_school(tag=""):
    if tag=="":
        query =SchoolsModel.get_all_school()
    if query:
        allschool=[]
        for school in query:
            a={"id":school.schoolid,"SchoolName":school.name,"zone":school.zone,"isNational":school.isNational,"official_website":school.official_website}
            allschool.append(a)
        return allschool
    return ""
def get_department(id=""):
    if id!="":
        query =DepartmentModel.find_by_schoolid(id)
    if query:
        alldepartment=[]
        for department in query:
            a={"schoolid":department.schoolid,"name":department.name,"url":department.url,"detail":department.detail}
            alldepartment.append(a)
        return alldepartment
    return ""
def get_alldepartment(year="110"):
    query =DepartmentModel.find_by_year(year)
    if query:
        alldepartment=[]
        for department in query:
            SchoolsName=SchoolsModel.find_by_id(department.schoolid).name
            a={"schoolid":department.schoolid,"SchoolsName":SchoolsName,"name":department.name,"url":department.url,"detail":department.detail}
            print(department.name)
            alldepartment.append(a)
        return alldepartment
    return ""
def search_department_apply(name):
    query =DepartmentModel.find_by_name(name)
    if query:
        alldepartment=[]
        for department in query:
            SchoolsName=SchoolsModel.find_by_id(department.schoolid).name
            a={"schoolid":department.schoolid,"SchoolsName":SchoolsName,"name":department.name,"url":department.url,"detail":department.detail}
            alldepartment.append(a)
        return alldepartment
    return ""
def get_news(tag=""):
    if tag=="":
        query =NewsModel.get_all_new()
    else:
        query =NewsModel.find_by_tag(tag)    
    if query:
        allnews=[]
        for new in query:
            a={"id":new.pid,"title":new.title,"content":new.content,"tag":new.tag,"date":new.date,"tag_type":new.tag_type}
            allnews.append(a)
        list.reverse(allnews)
        return allnews
    return ""

def get_users():
    query =UserModel.get_all_user()
    if query:
        allusers=[]
        for user in query:
            a={"pid":user.pid,"name":user.name,"email":user.email,"password":user.password,"role":user.role,"school":user.school}
            allusers.append(a)
        list.reverse(allusers)
        return allusers
    return ""    
def user_find(arg,type="username"):
    if type=="username":
        query =UserModel.find_by_name(arg)
    elif type=="email":
        query =UserModel.find_by_email(arg)
    if query:
        user={"name":query.name,"email":query.email,"password":query.password,"role":query.role,"school":query.school}
        return user
    return False
def login_check(username, password):
    """????????????????????????"""
    finduser=user_find(username)
    
    if (finduser) and check_password_hash(finduser['password'],password):
        return True
    else:
        return False
def admin_reauired():
    """admin_reauired"""
    if current_user.role=="admin":
        return True
    else:
        return False
# flask login settings

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = '???????????????'
# # # # # # # # # # # # # # # # # # # # # # # 

# flask login class User
class User(UserMixin):
    pass
@login_manager.user_loader
def user_loader(username):
    u=user_find(username)
    if  not u:
        return

    user = User()
    user.id = username
    user.role=u["role"]
    user.email=u["email"]
    user.school=u["school"]
    return user
@login_manager.request_loader
def request_loader(request):
    username = request.form.get('user_id')
    u=user_find(username)
    if  not u:
        return
    user = User()
    user.id = username
    user.role=u["role"]
    user.email=u["email"]
    user.school=u["school"]
    user.is_authenticated = login_check(username, request.form['password'])
    return user

# # # # # # # # # # # # # # # # # # # # # # # 

#route
@app.errorhandler(404)
def handle_404(err):
    return render_template('404.html')
@app.route("/run")
def run():
    db.create_all()
    return "OK"

@app.route("/add_to_favorite/star" ,methods=['GET','POST'])
def addToFavoriteStar():
    try:
        if request.method == 'POST':      
            alllist=[]
            query=FavModelstar.find_by_user(current_user.id)
            for a in query:
                alllist.append(a.favid)
            if request.form['postid'] not in alllist:
                newFav=FavModelstar(current_user.id,request.form['postid'])
                newFav.save_to_db()
                return F"add_succ_{request.form['postid']}"
            else:
                query=FavModelstar.find_by_user(current_user.id)
                for a in query:
                    if a.favid == request.form['postid']:
                        a.delete()          
                return F"rm_succ_{request.form['postid']}"
        return render_template('404.html')
    except:
        return "????????????"

@app.route("/add_to_favorite/caac" ,methods=['GET','POST'])
def addToFavorite():
    try:
        if request.method == 'POST':      
            alllist=[]
            query=FavModel.find_by_user(current_user.id)
            for a in query:
                alllist.append(a.favid)
            if request.form['postid'] not in alllist:
                newFav=FavModel(current_user.id,request.form['postid'])
                newFav.save_to_db()
                return F"add_succ_{request.form['postid']}"
            else:
                query=FavModel.find_by_user(current_user.id)
                for a in query:
                    if a.favid == request.form['postid']:
                        a.delete()          
                return F"rm_succ_{request.form['postid']}"
        return render_template('404.html')
    except:
        return "????????????"



@app.route("/????????????????????????")
def ????????????????????????():
    return render_template('??????????????????.html')

@app.route("/????????????????????????/<type>")
def ????????????????????????(type):
    if type=="?????????????????????" or type=="?????????????????????" or type=="?????????????????????" or type=="??????????????????":

        
        return render_template('?????????????????? group.html',type=type,schools=get_star_school(type))
    return render_template('404.html')

@app.route("/????????????????????????/<type>/<pid>")
def ????????????????????????school(type,pid):
    departmentlist=get_star_department(pid,type[:-2])
    school=Schools2Model.find_by_id(pid)
    favlist=[]
    try:
        q=FavModelstar.find_by_user(current_user.id)
        for a in q:
            favlist.append(a.favid)
    except:
        pass
    return render_template("??????????????????????????????.html",type=type,school=school.name,departmentlist=departmentlist,favlist=favlist)
@app.route("/????????????????????????/<type>/????????????")
def ????????????all(type):
    favlist=[]
    try:
        q=FavModelstar.find_by_user(current_user.id)
        for a in q:
            favlist.append(a.favid)
    except:
        pass
    return render_template('??????????????????-all.html',type=type,departmentlist=get_star_department("",type[:-2]),favlist=favlist)
@app.route("/????????????????????????/????????????" ,methods=['GET','POST'])
@login_required
def ????????????fav():

    favlist=[]
    try:
        q=FavModelstar.find_by_user(current_user.id)
        for a in q:
            favlist.append(a.favid)
    except:
        pass

    departmentlist=[]
    # try:
    q=FavModelstar.find_by_user(current_user.id)
    for a in q:
        department=Department2Model.find_by_id(a.favid)

        SchoolsName=Schools2Model.find_by_id(department.schoolid).name
        
        departmentlist.append({"schoolid":department.schoolid,"name":department.name,"url":department.url,"detail":department.detail})
    # except:
    #     pass    
    return render_template('??????????????????-fav.html',departmentlist=departmentlist,favlist=favlist)















@app.route("/??????????????????????????????")
def ????????????????????????():
    return render_template('????????????????????????.html',schools=get_school())

@app.route("/??????????????????????????????/????????????")
def ????????????????????????all():
    favlist=[]
    try:
        q=FavModel.find_by_user(current_user.id)
        for a in q:
            favlist.append(a.favid)
    except:
        pass
    if request.args.get('search'):
        departmentlist= search_department_apply(request.args.get('search'))
    else:
        departmentlist= get_alldepartment()
    return render_template('????????????????????????-all.html',departmentlist=departmentlist,favlist=favlist)
@app.route("/??????????????????????????????/????????????" ,methods=['GET','POST'])
@login_required
def ????????????????????????fav():
    departlist=[]
    try:
        f=FavModel.find_by_user(current_user.id)
        for a in f:
            q=DepartmentModel.find_by_id(a.favid)
            SchoolsName=SchoolsModel.find_by_id(q.schoolid).name
            departlist.append({"schoolid":q.schoolid,"SchoolsName":SchoolsName,"name":q.name,"url":q.url,"detail":q.detail})
            
    except:
        pass    
    return render_template('????????????????????????-fav.html',departlist=departlist)

@app.route("/??????????????????????????????/<pid>")
def ????????????????????????school(pid):
    departmentlist=get_department(pid)
    school=SchoolsModel.find_by_id(pid)
    favlist=[]
    try:
        q=FavModel.find_by_user(current_user.id)
        for a in q:
            favlist.append(a.favid)
    except:
        pass
    return render_template("????????????????????????????????????.html",school=school.name,departmentlist=departmentlist,favlist=favlist)

@app.route("/robots.txt")
@app.route("/sitemap.xml")
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/")
def home():
    return render_template("index.html",news=get_news())
@app.route("/new/<pid>")
def new(pid):
    new=NewsModel.find_by_id(pid)
    try:
        a={"id":new.pid,"title":new.title,"content":Markup(new.content),"tag":new.tag,"date":new.date,"tag_type":new.tag_type}
        return render_template("new.html",new=a)
    except:
        return render_template('404.html')




@app.route("/about")
def about():
    return render_template("about.html")






@app.route('/profile/')
@login_required
def account():
    tab=request.form.get('tab')

    scoredata =UserScoreModel.find_by_user  (current_user.id)
    if scoredata:
        scoredata=scoredata.score
    else:
        scoredata={}    

    if tab is not None:
        return render_template("profile.html",tab=tab,score=scoredata)
    return render_template("profile.html",score=scoredata)

@app.route('/auth/account/update', methods=['GET','POST'])
@login_required
def account_update():
    if request.method == 'POST':  
        user = UserModel.find_by_name(current_user.id)
        if request.form['email'] is not None:
            user.email=request.form['email']
            if request.form['school']:
                 user.school=request.form['school']
            if request.form['nowpassword']  and (not request.form['newpassword'] or not request.form['Cnewpassword']):
                return "??????????????????????????????????????????????????????"
            if request.form['newpassword'] :
                if request.form['nowpassword']:
                    if request.form['newpassword'] ==  request.form['Cnewpassword']:
                        stats = PasswordStats(request.form['newpassword'])
                        if policy.test(request.form['newpassword'])==[]:
                            if stats.strength()>=0.33:                        
                                user.password=generate_password_hash(request.form['newpassword'])
                            else:
                                return "??????????????????"
                        else:
                            return "???????????????????????????1??????????????????1??????????????????????????????8?????????"
                    else:
                        return "????????????????????????????????????" 
                else:
                    return "???????????????????????????????????????"
            user.update()
            return "save_succ"
        return "?????????E-mail"
    return render_template('404.html')
@app.route('/auth/account/score', methods=['GET','POST'])
@login_required
def score_update():
    if request.method == 'POST':  
        chinese=english=math=society=naturally=""
        chinese_Level=english_Level=math_Level=society_Level=naturally_Level="--"
        english_hearing="???"
        if request.form['chinese']:
            if int(request.form['chinese'])<=15 and int(request.form['chinese']) >=0:
                chinese=int(request.form['chinese'])
            else:
                OutOfRange()
        if request.form['english']:
            if int(request.form['english'])<=15 and int(request.form['english']) >=0:
                english=int(request.form['english'])
            else:
                OutOfRange()                
        if request.form['math']:
            if int(request.form['math'])<=15 and int(request.form['math']) >=0:
                math=int(request.form['math'])
            else:
                OutOfRange()                
        if request.form['society']:
            if int(request.form['society'])<=15 and int(request.form['society']) >=0:
                society=int(request.form['society'])
            else:
                OutOfRange()                
        if request.form['naturally']:
            if int(request.form['naturally'])<=15 and int(request.form['naturally']) >=0:
                naturally=int(request.form['naturally'])
            else:
                OutOfRange()                
        if request.form['english_hearing']: 
            english_hearing=request.form['english_hearing']

        leveldata=ScoreLevelModel.find_by_year("110")
        
        if chinese:
            if int(chinese)>=int(leveldata.Level["???"]["??????"]):
                chinese_Level="??????"
            elif int(chinese)>=int(leveldata.Level["???"]["??????"]):
                chinese_Level="??????"
            elif int(chinese)>=int(leveldata.Level["???"]["??????"]):
                chinese_Level="??????"                
            elif int(chinese)>=int(leveldata.Level["???"]["??????"]):
                chinese_Level="??????"    
            elif int(chinese)>=int(leveldata.Level["???"]["??????"]):
                chinese_Level="??????"    
            else:
                chinese_Level="--"
        if english:
            if int(english)>=int(leveldata.Level["???"]["??????"]):
                english_Level="??????"
            elif int(english)>=int(leveldata.Level["???"]["??????"]):
                english_Level="??????"
            elif int(english)>=int(leveldata.Level["???"]["??????"]):
                english_Level="??????"                
            elif int(english)>=int(leveldata.Level["???"]["??????"]):
                english_Level="??????"    
            elif int(english)>=int(leveldata.Level["???"]["??????"]):
                english_Level="??????"   
            else:
                english_Level="--"

        if math:
            if int(math)>=int(leveldata.Level["???"]["??????"]):
                math_Level="??????"
            elif int(math)>=int(leveldata.Level["???"]["??????"]):
                math_Level="??????"
            elif int(math)>=int(leveldata.Level["???"]["??????"]):
                math_Level="??????"                
            elif int(math)>=int(leveldata.Level["???"]["??????"]):
                math_Level="??????"    
            elif int(math)>=int(leveldata.Level["???"]["??????"]):
                math_Level="??????"  
            else:
                math_Level="--"

        if naturally:
            if int(naturally)>=int(leveldata.Level["???"]["??????"]):
                naturally_Level="??????"
            elif int(naturally)>=int(leveldata.Level["???"]["??????"]):
                naturally_Level="??????"
            elif int(naturally)>=int(leveldata.Level["???"]["??????"]):
                naturally_Level="??????"                
            elif int(naturally)>=int(leveldata.Level["???"]["??????"]):
                naturally_Level="??????"    
            elif int(naturally)>=int(leveldata.Level["???"]["??????"]):
                naturally_Level="??????" 
            else:
                naturally_Level="--"
            

        if society:
            if int(society)>=int(leveldata.Level["???"]["??????"]):
                society_Level="??????"
            elif int(society)>=int(leveldata.Level["???"]["??????"]):
                society_Level="??????"
            elif int(society)>=int(leveldata.Level["???"]["??????"]):
                society_Level="??????"                
            elif int(society)>=int(leveldata.Level["???"]["??????"]):
                society_Level="??????"    
            elif int(society)>=int(leveldata.Level["???"]["??????"]):
                society_Level="??????"   
            else:
                society_Level="--"
        score={
            "???":{"score":chinese,"???":chinese_Level},
            "???":{"score":english,"???":english_Level},
            "???":{"score":math,"???":math_Level},
            "???":{"score":naturally,"???":naturally_Level},
            "???":{"score":society,"???":society_Level},
            "??????":{"score":english_hearing}
        }
        
        if UserScoreModel.find_by_user(current_user.id):
            save = UserScoreModel.find_by_user(current_user.id)
            save.score=score
            save.update()
        else:
            save = UserScoreModel(current_user.id,score)
            save.save_to_db()
        return str(score)
    return render_template('404.html')
def OutOfRange():
    return "OutOfRange"










@app.route("/auth/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  
        if request.form['password'] and request.form['confirm_password'] and request.form['email'] and request.form['username']:
            stats = PasswordStats(request.form['password'])
            if request.form['password'] !=request.form['confirm_password']:
                return "?????????????????????"
            elif policy.test(request.form['password'])==[]:
                if stats.strength()>=0.35:
                    if not user_find(request.form['username']):
                        if not user_find(request.form['email'],"email"):
                            hash_pw=generate_password_hash(request.form['password'])
                            create_user(request.form['username'],request.form['email'],hash_pw)
                            return  "reg_succ"
                        return "???E-mail?????????"
                    return "???????????????????????????"
                else:
                    return  "pw_not_strong"
            else:
                return "pw_not_UpToStandard" 
        return "??????"
    return render_template("auth/register.html")   
def create_user(username,email,password):
    new_user = UserModel(username,email,password,"normal","")
    new_user.save_to_db()

@app.route('/auth/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/auth/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if login_check(request.form['username'], request.form['password']):
            username=request.form['username']
            user = User()
            user.id = username
            login_user(user)
            flash(f'{username}??????????????????')
            return('login_succ')
        flash('????????????...')
        return('pw_err')

    a=request.args.get('next')
    if a is None:
        a="../"
    return render_template("auth/login.html",next=a)








@app.route("/panel", methods=['GET', 'POST'])
@login_required
def panel():
    if admin_reauired():
        allusers=get_users()
        return render_template("admin/index.html",allusers=allusers,news=get_news())
    return render_template('404.html')
@app.route('/update/<type>', methods=['GET','POST'])
@login_required
def update(type):
    if type =="level":
        year=request.form['year']
        data={
            "???":{"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????']},
            "???":{"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????']},
            "???":{"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????']},
            "???":{"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????']},
            "???":{"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????'],"??????":request.form['??????']}
        }
        if ScoreLevelModel.find_by_year(year):
            ScoreLevel=ScoreLevelModel.find_by_year(year)
            ScoreLevel.year=year
            ScoreLevel.Level=data
            ScoreLevel.update()
        else:
            ScoreLevel=ScoreLevelModel(year,data)
            ScoreLevel.save_to_db()
    return "OK"


@app.route("/remove/<rm_type>/<pid>", methods=['GET'])
@login_required
def rm(rm_type,pid):
    if admin_reauired():
        try:
            if rm_type=="news":
                new=NewsModel.find_by_id(pid)
                new.delete()
                go="pill=3&tab=news"
            elif rm_type=="users":
                User=UserModel.find_by_name(pid)
                User.delete()
                go="pill=2"
            else:
                return render_template('404.html')
        except:
            return render_template('404.html')
        return redirect(url_for('panel')+F"?&{go}")
    else:
        return render_template('404.html')

@app.route("/getdata", methods=['GET', 'POST'])
@login_required
def getdata():
    if admin_reauired():
        if request.method == 'POST':
            try:
                year=request.values.get('year')   
                url=request.values.get('url')  
                datalist=update1(year,url)

                isDepartmentExist=DepartmentModel.find_by_year(year)
                if isDepartmentExist:
                    isDepartmentExist.delete()     

                for school in datalist:
                    schoolname=school["SchoolName"]
                    SchoolId=school["SchoolId"]
                    SchoolUrl=school["SchoolUrl"]
                    if "??????" in schoolname or "??????" in schoolname:
                        isNational="True"
                    else:
                        isNational="False"
                    isExist=SchoolsModel.find_by_id(SchoolId)
                    if isExist:
                        isExist.delete()
                    newSchool=SchoolsModel(SchoolId,schoolname,"Undefine",isNational,SchoolUrl)
                    newSchool.save_to_db() 
                    for department in school["????????????"]:
                        departmentcode=department["??????"]
                        departmentname=department["??????"]
                        departmenturl=department["url"]
                        departmentdetail=department
                        newdepartment=DepartmentModel(year,departmentcode,departmentname,departmenturl,(departmentdetail),SchoolId) #(year,code,name,url,detail):
                        newdepartment.save_to_db()
                return "????????????"
            except:
                return "????????????"
        else:
            return redirect(url_for('panel'))
    return render_template('404.html')

@app.route("/getdata2", methods=['GET', 'POST'])
@login_required
def getdata2():
    if admin_reauired():
        if request.method == 'POST':
            # try:
                year=request.values.get('year')   
                url=request.values.get('url')  
                datalist=update2(year,url)
                isSchoolExist=Schools2Model.find_by_year(year)
                if isSchoolExist:
                    isSchoolExist.delete()     
                isDepartmentExist=Department2Model.find_by_year(year)
                if isDepartmentExist:
                    isDepartmentExist.delete()     
                for datalist2 in datalist:
                    for school in datalist2:
                        schoolname=school["SchoolName"]
                        SchoolId=school["SchoolId"]
                        SchoolUrl=school["SchoolUrl"]
                        star=school["??????????????????"]
                        group=school["???"]
                        if "??????" in schoolname or "??????" in schoolname:
                            isNational="True"
                        else:
                            isNational="False"

                        isExist=Schools2Model.find_by_name(schoolname).first()
                        if isExist:
                            if group=="???????????????":
                                a=isExist
                                a.group1="True"
                            elif group=="???????????????":
                                a=isExist
                                a.group2="True"
                            elif group=="???????????????":
                                a=isExist
                                a.group3="True"     
                            a.update()                           
                        else:
                            try:
                                tt=SchoolsModel.find_by_name(schoolname)
                                SchoolUrl=tt.official_website
                            except:
                                pass

                            group1=""
                            group2=""
                            group3=""
                            if group=="???????????????":
                                group1="True"
                            elif group=="???????????????":
                                group2="True"
                            elif group=="???????????????":
                                group3="True"     
    
                            newSchool=Schools2Model(year,group1,group2,group3,SchoolId,schoolname,star,"Undefine",isNational,SchoolUrl)
                            newSchool.save_to_db() 
                        for department in school["????????????"]:
                            departmentcode=department["??????"]
                            departmentgroup=department["group"]
                            departmentname=department["??????"]
                            departmenturl=department["url"]
                            departmentdetail=department
                            newdepartment=Department2Model(year,departmentcode,departmentname,departmenturl,(departmentdetail),SchoolId,departmentgroup) #(year,code,name,url,detail):
                            newdepartment.save_to_db()
                return "????????????"
            # except:
            #     return "????????????"
        else:
            return redirect(url_for('panel'))
    return render_template('404.html')

@app.route("/news_release", methods=['GET', 'POST'])
@login_required
def news_release():
    if admin_reauired():    
        if request.method == 'POST':
            news_tag_type=request.values.get('news_tag_type') 
            news_tag=request.values.get('news_tag') 
            news_title=request.values.get('news_title')   
            news_content=request.values.get('news_content')
            newNew = NewsModel(news_title,news_content,str(datetime.date.today()),news_tag,news_tag_type)
            newNew.save_to_db()
            return "???????????????"
        else:
            return redirect(url_for('panel'))
    return render_template('404.html')










if __name__ == "__main__":
    app.secret_key = "VKO72yJ9ek1raiqjXTw1dxGNnp3MjmjkjmAcUg2DeBedXquW8nbnqaXAfL6SY7MQ"
    app.run(host="0.0.0.0",port=80,debug=True,processes=True)

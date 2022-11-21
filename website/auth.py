from flask import (
                    Flask , Blueprint, flash ,
                    render_template, url_for, abort,
                    request ,redirect ,session ,g # g object. g object is global to the request. Meaning g is specific to one user.
                  )
#from website import userclass
from .userclass import User
from .wazuhconn import Conn
from .util import iterate_dict
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth',__name__)

# templ_folder = '/home/user/Desktop/web_applic/website/templates'
# stat_folder = '/home/user/Desktop/web_applic/website/static'
# app = Flask(__name__ ,template_folder= templ_folder, static_folder = stat_folder)

_name = 'API_AUTH'
hash_password = generate_password_hash('API_PASS',method='sha256',salt_length=8)
auth_user = User(id=1 , usrname=_name, password =hash_password)

print ("A USER " , auth_user)
title ="WEB_APPLICATION"


@auth.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
      #Make a user obj
      user = User(id='user_id' , usrname=_name, password =hash_password)  
      conn =Conn()
      g.user = user
      g.conn =conn

@auth.route("/")
def index():
    return render_template('index.html', title=title)


@auth.route("/login" , methods = ['GET' ,'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else: #'POST'
        session.pop('user_id', None)
        user_name =  request.form['username']#generate_password_hash(request.form['username'] ,method='sha256',salt_length=8 )  
        pass_word =  request.form['password']#generate_password_hash(request.form['password'] ,method='sha256',salt_length=8 ) 
       
       
       
        if (_name == user_name) and (check_password_hash(hash_password, pass_word)):
            session['user_id'] = auth_user.id
            return redirect(url_for('auth.displayrules'))
        else:
            flash('Invalid Credentials', category='error')
            return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth.route("/displayrules",methods = ['GET' ,'POST'])
def displayrules():
    if  g.user and g.conn.connect_to_wazuh() : 
        if request.method == 'GET':
            return render_template('displayrules.html' )
        else: #'POST'
            rule_id = request.form['rule_id']
            if not rule_id:
                    return render_template('displayrules.html' )
            wazuh_data = g.conn.get_rule(rule_id)
           
            return render_template('displayrules.html' , data= iterate_dict(wazuh_data['data']['affected_items'][0])) 
    else:
        abort(403)
        return render_template('displayrules.html')

@auth.route("/listagents",methods = ['GET'])
def listagents():
    if  g.user and g.conn.connect_to_wazuh() : 
        if request.method == 'GET':
            dict_agents = g.conn.get_agents()
            if not dict_agents:
                    return render_template('displayrules.html' )          
            dict_agents = iterate_dict(dict_agents['data']['affected_items'][0]) # nested dictionary with lists. we pass the 1st dictionary .
        
            return render_template('displayrules.html' , agentsdata= iterate_dict(dict_agents[0]))
    else:
        abort(403)
        return render_template('displayrules.html')


@auth.route("/addagent",methods = ['POST'])
def add_agent ():
    if  g.user and g.conn.connect_to_wazuh() :
         if request.method == 'POST':
            form_name = request.form['name']
            form_agent_name = request.form['agent_name']
            print("NAME AGENT NAME " , form_name , form_agent_name)
            add_agent_data = g.conn.add_agen(form_name , form_agent_name)
    return render_template('displayrules.html' , add_agent_data )



@auth.route("/logout")
def logout():
    session.pop('user_id', None)
    return render_template('index.html')

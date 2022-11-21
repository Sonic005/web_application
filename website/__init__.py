from flask import Flask

templ_folder = '/home/user/Desktop/web_applic/website/templates'
stat_folder = '/home/user/Desktop/web_applic/website/static'



def init_app():
    app = Flask(__name__ ,template_folder= templ_folder, static_folder = stat_folder)
    app.config['SECRET_KEY']='dsfsdnl khsdk'

    from .auth import auth

    app.register_blueprint(auth , url_prefix='/')

    return app







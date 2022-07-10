from flask import Flask, redirect, render_template, request
import requests
import os
from toml import load
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, current_user, login_user, UserMixin, logout_user
import bcrypt
from markupsafe import Markup
import difflib
from werkzeug.serving import run_simple
from werkzeug.utils import secure_filename
import sys
import importlib

sys.path.append("wk-contents")

pl = importlib.import_module("pluginloader")

def get_hashed_password(plain_text_password):
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password, hashed_password)



to_reload = False
def get_app():
    app = Flask("WebsiteKit", template_folder="wk-include", static_url_path="/wk-static")
    app.config["SQLALCHEMY_DATABASE_URI"] = config["WkitConf"]["sqlalchemy_database_uri"]
    app.config["SECRET_KEY"] = config["WkitConf"]["secret_key"]
    
    @app.route('/wk-admin/reload')
    @login_required
    def reload():
        global to_reload
        to_reload = True
        return "<script>history.back()</script>"

    def get_hashed_password(plain_text_password):
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

    def check_password(plain_text_password, hashed_password):
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        return bcrypt.checkpw(plain_text_password, hashed_password)

    db = SQLAlchemy(app)
    login_mgr = LoginManager(app)
    app.login_required = login_required
    class HTML(db.Model):
        id = db.Column(db.Integer, primary_key = True, autoincrement = True)
        rule = db.Column(db.String(50), unique = True, default="/")
        html = db.Column(db.String(10240), nullable=False)
        render_type = db.Column(db.String(5), nullable=False)
        

    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key = True, autoincrement = True)
        username = db.Column(db.String(50), unique = True, default="Wk-Admin")
        password = db.Column(db.String(1024))
        

    @login_mgr.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


    @app.route("/wk-login")
    def login():
        return render_template("wk-login.html")


    @app.errorhandler(401)
    def unauthorized(e):
        return redirect("/wk-login"), 401

    @app.route("/wk-logout")
    @login_required
    def logoff():
        logout_user()
        return redirect("/")

    @app.route("/wk-postlogin", methods=["POST"])
    def postlogin():
        user = User.query.filter_by(username = request.form["username"]).first()
        if user:
            if check_password(request.form["password"].encode(), user.password.encode()):
                login_user(user)
                return redirect("/wk-admin")
            else:
                print("sed")
        else:
            print(request.form["username"])
            print("uh?")
            for x in User.query.all():
                print(x.username)
                a = x.username
                b = request.form["username"]
                print('{} => {}'.format(a,b))  
                for i,s in enumerate(difflib.ndiff(a, b)):
                    if s[0]==' ': continue
                    elif s[0]=='-':
                        print(u'Delete "{}" from position {}'.format(s[-1],i))
                    elif s[0]=='+':
                        print(u'Add "{}" to position {}'.format(s[-1],i))    
                print() 

        return redirect("/wk-login")

    @app.route("/wk-admin")
    @login_required
    def admin():
        return render_template("wk-backend.html")

    @app.route("/wk-admin/routes")
    @login_required
    def routes():
        rules = []
        for rule in app.url_map.iter_rules():
            if not rule.rule.startswith("/wk-"):
                rules.append(rule)
        return render_template("wk-manage-routes.html", rules=rules)


    @app.route("/wk-admin/edit/styles")
    @login_required
    def edit_css():
        samole = Markup(requests.get("https://www.w3schools.com/howto/tryhow_css_example_website.htm").text)
        th = []
        for x in os.listdir("wk-themes"):
            if x.endswith(".theme"):
                th.append("wk-themes/"+x+"/style.css")
        return render_template("wk-edit-styles.html", themes=th, stylesheet_name=request.args.get("stylesheet_name","style.css"), sample_text=samole)


    @app.route("/wk-admin/edit/styles", methods=["POST"])
    @login_required
    def edit_css_P():
        stylesheet_name=request.args.get("stylesheet_name","style.css")
        markup = request.form["markup"]
        if request.form["theme"] != "null":
            markup = open(request.form["theme"]).read()
        with open(f"wk-contents/{secure_filename(stylesheet_name)}","w") as f:
            f.write(markup)
        return redirect("/wk-admin/reload")

    @app.route("/wk-admin/edit/response")
    @login_required
    def edit_response():
        return render_template("wk-edit-rule.html", rule=request.args.get("u"))

    @app.route("/wk-admin/edit/response", methods=["POST"])
    @login_required
    def edit_response_P():
        HTML.query.filter_by(rule=request.args.get("u")).update({'html':request.form['markup'], 'render_type':request.form['render-type']})
        db.session.commit()
        return redirect("/wk-admin/reload")

        return render_template("wk-edit-rule.html", rule=request.args.get("u"))

    @app.route("/wk-admin/edit/add-route")
    @login_required
    def add_route():
        return render_template("wk-add-route.html", rule=request.args.get("u"))

    @app.route("/wk-admin/edit/add-route", methods=["POST"])
    @login_required
    def add_route_P():
        print(request.form["rule"])
        ht = HTML(rule=request.form["rule"], html=request.form["markup"], render_type=request.form['render-type'])
        db.session.add(ht)
        db.session.commit()
        return redirect("/wk-admin/reload")
        return redirect("/wk-admin/edit/add-route")


    for ht in HTML.query.all():
        app.add_url_rule(
            ht.rule,
            "_"+ht.rule.strip("/"),
            lambda: ht.html,
        )

    @app.route("/wk-admin/<e>")
    def notfound(e):
        return '<script>history.back()</script>'
    
    app.db = db
    for l in os.listdir("wk-contents/uploads"):
        pl.load_pl(app, l)

    return app

class AppReloader(object):
    def __init__(self, create_app):
        self.create_app = create_app
        self.app = create_app()

    def get_application(self):
        global to_reload
        if to_reload:
            self.app = self.create_app()
            to_reload = False

        return self.app

    def __call__(self, environ, start_response):
        app = self.get_application()
        return app(environ, start_response)
config = load(open(".wkaccess"))



if __name__ == "__main__":
    application = AppReloader(get_app)
    run_simple(config["WkitConf"]["ws_host"], config["WkitConf"]["ws_port"], application,
               use_reloader=True, use_debugger=True, use_evalex=True)

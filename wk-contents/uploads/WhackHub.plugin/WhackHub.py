import toml
import sqlite3
import os

def setup(app):
    @app.route("/wk-admin/whackhub/create")
    @app.login_required
    def create_backup():
        wkaccess = toml.load(open(".wkaccess"))
        section = wkaccess.get("WkPlugin")
        if not section:
            section = {"WHACKHUB_NEW_DATABASE_URI":"wkh.db"}
            #return "<script>history.back()</script>"
        to = section.get("WHACKHUB_NEW_DATABASE_URI")#app.request.args.get("t", "wkh.db")
        
        d1 = sqlite3.connect(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///",""))
        if os.path.exists(to):os.remove(to)
        d2 = sqlite3.connect(to)
        for l in d1.iterdump():
            print(l)
            cur = d2.cursor()
            cur.execute(l)
            cur.close()
        d2.commit()

        return f"""
Backup created as {to}.<br><button onclick="history.back()">Back!</button>
        """

    @app.route("/wk-admin/whackhub/load")
    @app.login_required
    def load_backup():
        return open(os.path.dirname(os.path.abspath(__file__))+"/confirm.html").read()

    @app.route("/wk-admin/whackhub/load", methods=["POST"])
    @app.login_required
    def FLoad():
        wkaccess = toml.load(open(".wkaccess"))
        section = wkaccess.get("WkPlugin")
        if not section:
            section = {"WHACKHUB_NEW_DATABASE_URI":"wkh.db"}
            #return "<script>history.back()</script>"
        to = section.get("WHACKHUB_NEW_DATABASE_URI")#app.request.args.get("t", "wkh.db")
        if not os.path.exists(to):
            return "<script>history.back()</script>"
        d1 = sqlite3.connect(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///",""))
        if os.path.exists(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///","")):os.remove(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///",""))
        d2 = sqlite3.connect(to)
        for l in d2.iterdump():
            print(l)
            cur = d1.cursor()
            cur.execute(l)
            cur.close()
        d1.commit()

        return f"""
Backup created as {to}.<br><button onclick="history.back()">Back!</button>
        """


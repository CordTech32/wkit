# WKit
Simple, Minimalistic Website Development Kit  
Written in Python using Flask, SQLAlchemy and Werkzeug.

WKit allows you to manage your Website with Routes, HTML, Styles and everything else![](https://python.makes-me-horny.wtf/674760.png)

## Installation
WKit comes with the `install.py` Program, that quickly  
sets up WKit and readies it for deployment.

## The Backend 
The Backend is WKit's Core. It provides a Graphical User Interface that allows:

* Managing the Routes  
* Managing Plugins (But Plugins aren't ready yet, they will most likely be added in V2)  
* Managing the Styles
### Logging in
To Log in to the Backend, you open `http://your-website/wk-login`.  
Upon Prompt, you enter your username and password that you specified in the Installation.  

You will then be redirected to the Backend, available at `/wk-admin`

## Routes, Rules and HTML
A *Route* is the Combination of a *Rule* and a HTML Response.

The Rule is equivalent to the Endpoint (/1234). Upon calling a *Rule*, the corresponding HTML *Response* will be rendered. Note that the MIMEType is always :mimetype: text/html

## Reinstalling the Backend
To wipe off your current Website and start over, delete `users.db` and run the install-file again.


## .wkaccess
The .wkaccess-File tells WKit, where to run your App. It also contains the SECRET_KEY and the Database Path.

It is written in [TOML](https://toml.io/)

### A Sample .wkaccess

The most minimalistic wkaccess looks like this:

```toml
[WkitConf]
ws_host="127.0.0.1"
ws_port=4000
secret_key="bzergeu"
sqlalchemy_database_uri="sqlite:///users.db"
```

### Running the App
Just run `python3 WSS.py`
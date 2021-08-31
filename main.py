import os
from flask import Flask,render_template,redirect,url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized


deploy=False

app=Flask(__name__,static_url_path='')



@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/login')
def login():
    return app.send_static_file('login.html')

@app.route('/login/oauth2')
def login():
    pass



if __name__ == "__main__":
    if deploy==False:
        app.run(host='127.0.0.1',port=443,debug=True,ssl_context=('./server.crt', './server.key'))
    elif deploy==True:
        app.run(host='0.0.0.0',port=443,debug=True)

    
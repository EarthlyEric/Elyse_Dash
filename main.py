from gevent import monkey
monkey.patch_all()

import os
from flask import Flask,render_template,redirect,url_for,send_from_directory
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from gevent.pywsgi import WSGIServer
from configobj import ConfigObj
from flask_compress import Compress


config = ConfigObj('config.ini')

raw_deploy_config=config['deploy']
if raw_deploy_config=='1':
    deploy_config=True
elif raw_deploy_config=='0':
    deploy_config=False

DISCORD_CLIENT_ID_config=int(config['DISCORD_CLIENT_ID'])
DISCORD_CLIENT_SECRET_config=config['DISCORD_CLIENT_SECRET']
DISCORD_BOT_TOKEN_config=config['DISCORD_BOT_TOKEN']



deploy=deploy_config

app = Flask(__name__,
            static_url_path='', 
            static_folder='web',
            template_folder='web')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      

app.secret_key=b"random bytes representing flask secret key"
app.config["DISCORD_CLIENT_ID"]=DISCORD_CLIENT_ID_config   
app.config["DISCORD_CLIENT_SECRET"]=DISCORD_CLIENT_SECRET_config
if deploy==False:
    app.config["DISCORD_REDIRECT_URI"]="https://127.0.0.1/callback"
elif deploy==True:
    app.config["DISCORD_REDIRECT_URI"]="https://elyse.reload-dev.ml/callback"              
                 
app.config["DISCORD_BOT_TOKEN"]="DISCORD_BOT_TOKEN_config"                    

discord=DiscordOAuth2Session(app)

compress = Compress()
compress.init_app(app)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/team')
def team():

    return render_template('team.html')

@app.route('/thanks')
def thanks():

    return render_template('thanks.html')

@app.route('/login')
def login():

    return render_template('login.html')

@app.route('/oauth2')
def oauth2():

    return discord.create_session()

@app.route('/callback')
def callback():
    discord.callback()
    user=discord.fetch_user()
    print(user)

    return redirect(url_for(".dashboard"))

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):

    return redirect(url_for("login"))

@app.route('/dashboard')
@requires_authorization
def dashboard():
    user=discord.fetch_user()
    user_name=user.name

    return render_template('dashboard.html',user=user)

@app.route('/logout')
@requires_authorization
def logout():
    discord.revoke()

    return redirect(url_for("index"))

if __name__ == "__main__":
    if deploy==False:
        app.run(host='127.0.0.1',port=443,debug=True,ssl_context=('./server.crt', './server.key'))
    elif deploy==True:
        http_server = WSGIServer(('0.0.0.0', 8080), app)
        http_server.serve_forever()

    
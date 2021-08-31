import os
from flask import Flask,render_template,redirect,url_for,send_from_directory
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

deploy=False

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      

app.config["DISCORD_CLIENT_ID"] = 870136029582098452    
app.config["DISCORD_CLIENT_SECRET"] = "Yy5Cg9isk0xQsLej1fWAJ80v8wefXDeh"               
app.config["DISCORD_REDIRECT_URI"] = "https://127.0.0.1/callback"                 
app.config["DISCORD_BOT_TOKEN"] = "ODcwMTM2MDI5NTgyMDk4NDUy.YQIXUw.860tn47xIqW0SqgHRoxZW3H5BwE"                    

discord = DiscordOAuth2Session(app)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/oauth2')
def oauth2():

    return discord.create_session()

@app.route('/callback')
def callback():
    discord.callback()
    user = discord.fetch_user()

    return redirect(url_for(".dashboard"))

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):

    return redirect(url_for("login"))

@app.route('/dashboard')
@requires_authorization
def dashboard():
    user = discord.fetch_user()

    return render_template('dashboard.html')



if __name__ == "__main__":
    if deploy==False:
        app.run(host='127.0.0.1',port=443,debug=True,ssl_context=('./server.crt', './server.key'))
    elif deploy==True:
        app.run(host='0.0.0.0',port=443,debug=True)

    
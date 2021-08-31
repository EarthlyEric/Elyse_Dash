import os
from flask import Flask,render_template,redirect,url_for
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized


deploy=False

app=Flask(__name__,static_url_path='')

app.secret_key = b"random bytes representing flask secret key"
# OAuth2 must make use of HTTPS in production environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = 870136029582098452    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "Yy5Cg9isk0xQsLej1fWAJ80v8wefXDeh"                # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "https://alice-app.osc-fr1.scalingo.io/dash"                 # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = "ODcwMTM2MDI5NTgyMDk4NDUy.YQIXUw.860tn47xIqW0SqgHRoxZW3H5BwE"                    # Required to access BOT resources.

discord = DiscordOAuth2Session(app)

def welcome_user(user):
    dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return discord.bot_request(
        f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
    )

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/login')
def login():
    return app.send_static_file('login.html')

@app.route('/login/oauth2')
def oauth2():
    return discord.create_session()

@app.route("/callback/")
def callback():
    discord.callback()
    user = discord.fetch_user()
    welcome_user(user)
    return redirect(url_for(".me"))

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/dash")
@requires_authorization
def me():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src='{user.avatar_url}' />
        </body>
    </html>"""



if __name__ == "__main__":
    if deploy==False:
        app.run(host='127.0.0.1',port=443,debug=True,ssl_context=('./server.crt', './server.key'))
    elif deploy==True:
        app.run(host='0.0.0.0',port=443,debug=True)

    
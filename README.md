# Discord bot Naomi - discord.ext.commands & cogs


For launch on HerokuApp you need to:
* Add BuildPacks:
    * heroku/python
    * https://github.com/xrisk/heroku-opus.git
    * https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git
* Add Config Vars:
    * TALK_SERVICE_SESSION_ID - Your Google Dialogflow session ID
    * TALK_SERVICE_TOKEN - Your Google Dialogflow token
    * TOKEN - Your bot token

(You can create bot-application and get token on https://discordapp.com/developers/applications/me)


Bot written with Python 3.6.6 and Discord-Rewrite 1.0.0a

Thanks [F4stZ4p](https://github.com/F4stZ4p) for music cog. 
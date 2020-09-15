# Discord Stock News Bot

A Discord bot that monitors and reports stock news from Robinhood to a specific discord channel every 10min.

Requirements

- Python 3.8.5

# Setup/Installation

1. Fork/Clone the repository `git clone git@github.com:Dkirk25/news_bot.git`
2. Setup Firebase Project

- Need to generate a private key in Firebase project.
- Set the variable to the path of the private_key.json

3. Create a `.env`

```
# Discord
TOKEN=
CHANNEL_ID=

# Firebase
FIREBASE_KEY=

# Robinhook
USERNAME=
PASSWORD=
MFA=

# Poll data every 10 minutes
POLL_INTERVAL=600
```

4. Run `python main.py`

# Bot Commands

1. `.add` - Add stock to list of "Watched Stocks"
2. `.remove` - Remove stock to list of "Watched Stocks"
3. `.list` - View all stocks being watched
4. `.help` - Shows list of bot commands
5. `.purge` - Remove all messages that are not from the bot

# Integrations

- Discord
- Firebase
- Robinhood Unofficial API (pyrh)
  · https://github.com/robinhood-unofficial/pyrh

# PIP Modules

View the [requirements.txt](https://github.com/Dkirk25/news_bot/blob/master/requirements.txt)

# Deployment Options

- [Heroku](httpS://www.heroku.com)
- [Google Cloud](https://cloud.google.com)

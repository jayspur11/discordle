# discordle
...is a Discord bot that manages a text channel where people can freely discuss Wordle spoilers. It does so by creating a new role in the server, then a "private" channel that only the new role can access, granting access to people as they send their Wordle results from the day, and finally revoking access at midnight (Eastern time) when the new puzzle becomes available.

# Getting Started
Before anything else, you'll need to set up your environment. Whether you plan to help develop this bot or just want to run it, here are the basics:

1. Install Python.
    - Discordle was developed using [Python 3.9](https://www.python.org/downloads/release/python-3910/). Later versions of Python 3 will work, too, but I make no guarantees about earlier versions.
2. Grab the code.
    - ```git clone https://github.com/jayspur11/discordle.git``` \
      If you just want to run the bot, not contribute to it, you can download & unzip the latest [release](https://github.com/jayspur11/discordle/releases) instead.
    - ```cd discordle```
3. (optional) Create a virtual environment.\
   This is entirely up to you. I find it useful to keep all my projects' dependencies separated.
    - ```python3 -m venv .venv```
    - (Bash) ```source .venv/bin/activate```
    - (PowerShell) ```.\.venv\Scripts\Activate.ps1```
4. Install dependencies.
    - ```python3 -m pip install -r requirements.txt```
5. Set up your environment file.
    - ```cp .env.example .env```
    - Use your favorite editor to fill out the info.

Now you're ready to roll!

## Running the Bot
Once you've got everything set up, you can run the bot with ```python3 app.py```.

If you're going to work on the bot, and have set up `.env` with a test bot account, great!

If you're hosting the bot to for-realsies manage a server, I recommend taking it a step further and [setting it up as a service](https://www.google.com/search?q=how+to+run+a+python+script+as+a+service) <!-- hah gottem --> so it can (mostly) manage itself.
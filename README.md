# <p align="center">Telegram Reminder Bot Template
This is a simple template for a Telegram reminder bot built using the [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) implementation of the [Telegram Bot API](https://core.telegram.org/bots/api). 

* [Functionality](#functionality)
* [Installation](#installation)
* [Bot Setup](#bot-setup)
* [Running The Bot](#running-the-bot)
  * [Full Command List](#full-command-list)
  * [Extending The Template](#extending-the-template)
* [License](#license)
* [Contact](#contact)

## Functionality
This bot template is built with the following features:
* Handle user registration with the bot
* Handle blocking of users
* Automatically send reminder messages to registered users at scheduled times
* Basic administration and troubleshooting

If additional functionality is required, see [Extending The Template](#extending-the-template).

## Installation
This bot template is mostly tested on Python 3.7.4.

1. Clone this repository
   ```
   git clone https://github.com/ryankn/telegram-reminder-bot.git
   ```

2. Follow the installation instructions for the [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI#getting-started) library. 

3. Install the following dependencies (instructions below for using the package manager [pip](https://pip.pypa.io/en/stable/)). 
   ```
   $ pip install timeloop
   $ pip install python-dotenv
   ```

## Bot Setup
To use this template, [obtain an API token from @BotFather](https://core.telegram.org/bots#6-botfather). Then modify `.env`, replacing the placeholder TOKEN variable with your API token. Note that this API token is what allows you to control your bot, so keep it secret!

Other commonly desired configuration changes can be done by modifying variables within the `.env` file. 

### Administrative 
* `ADMIN`: chat id of the admin user (presumably you). You can get your chat id by sending the `/chatid` command to the bot. Only the user with the registered admin chatid
* `UD_FILE`: the userdict file to use. Set to `userdict.tsv` by default.
* `TMP_UD_FILE`: the temporary userdict file to use when overwriting files. Set to `tmp_userdict.tsv` by default.
* `BD_FILE`: the blockdict file to use. Set to `blockdict.tsv` by default.

### Bot Controls
* `BOT_NAME`: what name the bot will refer to itself as.
* `ONBOARDING`: the text sent to users when onboarding is completed.
* `REMINDER`: the text sent to users when a reminder is prompted.
* `TIMES`: the times to send reminders to users, in the timezone of the bot's server. By default, set to 8 AM and 5:30 PM.

## Running The Bot
To run the bot, run `run.py`, which will automatically restart the bot whenever the bot crashes. 

To initiate bot onboarding, the `/start` command can be sent to the bot by the user. After the user inputs their name, this is written to `userdict.tsv` and the user will begin receiving reminders. That's it!

### Full Command List
* `/start`: initiates onboarding; if user has already onboarded, greets user.
* `/chatid`: sends back the requesting user's chat id.
* `/name`: sends back the requesting user's name.

* `/forceremind`: Forces a reminder to be sent out to users immediately. Admin only.
* `/block 12345678`: Blocks the user with the specified chat id. Admin only. 
* `/userdict`: Sends back all users. Admin only.
* `/blockdict`: Sends back all blocked users. Admin only.
* `/exception`: Throws a ZeroDivisionError, crashing the bot. Admin only.

### Extending The Template
For information on how to extend the template and add additional functionality as required, check out the full documentation for [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI).

## License
Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License.

## Contact
Ryan Nah - ryanknah@gmail.com

Project Link: https://github.com/ryankn/telegram-reminder-bot
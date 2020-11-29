import telebot
import re
import time
from timeloop import Timeloop
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# put token from BotFather here
TOKEN = os.getenv('TOKEN')

# text for output
BOT_NAME = os.getenv('BOT_NAME')
ONBOARDING = os.getenv('ONBOARDING')
REMINDER = os.getenv('REMINDER')

# your chat id for debugging
ADMIN = int(os.getenv('ADMIN'))

# file names
UD_FILE = os.getenv('UD_FILE')
TMP_UD_FILE = os.getenv('TMP_UD_FILE')
BD_FILE = os.getenv('BD_FILE')

# times of day to send reminders, as a list of lists
TIMES = [i.split(":") for i in os.getenv('TIMES').split(",")]

#create a new Telegram Bot object
bot = telebot.TeleBot(TOKEN)

class User:
    def __init__(self, name):
        self.name = name

user_dict = {}
block_dict = {}

f= open(UD_FILE, "r")

f1 = f.readlines()
for x in f1:
    spam = re.split(r'\t+', x)
    user = User(spam[1])
    user_dict[int(spam[0])] = user

f.close()

f= open(BD_FILE, "r")

f1 = f.readlines()
for x in f1:
    spam = re.split(r'\t+', x)
    user = User(spam[1])
    block_dict[int(spam[0])] = user

f.close()

# Handle '/start'
# initialization, takes initial information and writes it to UD_FILE
# it also loads the new info into in the various user_dicts
# rank, name, appointment, division, then generates name abbreviation and 4d

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        chat_id = message.chat.id
        if chat_id in block_dict:
            bot.send_message(chat_id, "You are blocked.")
        else:
            if chat_id in user_dict:
                user = user_dict[chat_id]
                bot.reply_to(message, 'Nice to see you again, ' + user.name + ".")
                t = time.localtime()
                print("[{:0>2}:{:0>2}]: replied to {}".format(t.tm_hour, t.tm_min, user.name)) 
            else:
                msg = bot.reply_to(message, "Hello, I am {}. What is your name?".format(BOT_NAME))
                bot.register_next_step_handler(msg, process_name_step)
    except Exception as e:
        t = time.localtime()
        print("[{:0>2}:{:0>2}]: error {}".format(t.tm_hour, t.tm_min, e))

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        user.name = name
        f = open(UD_FILE, "a+")
        f.write(str(chat_id) + "\t" + user.name + "\n")
        f.close()
        bot.reply_to(message, ONBOARDING)
        bot.send_message(ADMIN, user.name + " has registered with {}!".format(BOT_NAME))
    except Exception as e:
        bot.reply_to(message, 'Please input your name.')
        bot.register_next_step_handler(message, process_name_step)

# send message reminders
def send_reminder(hour,minute):
    confirmation = "%d:%s %s reminder sent!"
    if minute < 10:
        minute_str = "0" + str(minute)
    else:
        minute_str = str(minute)
    if hour < 12:
        hour_str = "am"
    else:
        hour_str = "pm"
        hour = hour - 12
    for key in user_dict:
        try:
            bot.send_message(key, REMINDER % (hour, minute_str, hour_str))
            print("message to " + user_dict[key].name + " sent")
        except telebot.apihelper.ApiException as e:
            bot.send_message(ADMIN, "message to " + user_dict[key].name + " failed")
            print("message to " + user_dict[key].name + " failed")
            print("error: " + re.split('false,', e.args[0])[1])
            bot.send_message(ADMIN, "error: " + re.split('false,', e.args[0])[1])
            print("function: " + e.function_name)
    print(confirmation % (hour, minute_str, hour_str))
    bot.send_message(ADMIN, confirmation % (hour, minute_str, hour_str))
#    bot.stop_polling() #oddly, to achieve reliability, bot shuts down after each message

# force a reminder to send at this time
@bot.message_handler(commands=['forceremind'])
def force_reminder(message):
    try:
        chat_id = message.chat.id
        if chat_id == ADMIN:
            t = time.localtime()
            send_reminder(t.tm_hour, t.tm_min)
        else:
            bot.send_message(chat_id, "nice try buddy")
            print(str(chat_id) + " tried to force a reminder")
            bot.send_message(ADMIN, "some guy tried to force a reminder")
    except telebot.apihelper.ApiException as e:
        print("error in force reminder")
        print(e)
    except ZeroDivisionError:
        print("divzero error")
        1/0
    except Exception as e:
        print("error in force reminder but its not telegram")
        print(e)
        bot.send_message(ADMIN, "error in force reminder but its not telegram")

tl = Timeloop()

# check whether its the right time. if it is, sends a message
# allows for duplicate times if cohort A and B both need a message at the same time
@tl.job(interval=timedelta(seconds=60))
def checktime():
    t = time.localtime()
    if [str(t.tm_hour), str(t.tm_min)] in TIMES:
        send_reminder(t.tm_hour, t.tm_min)

##@tl.job(interval=timedelta(seconds=10))
##def testing():
##    t = time.localtime()
##    print("{}:{}:{:0>2}".format(t.tm_hour, t.tm_min, t.tm_sec))

@tl.job(interval=timedelta(hours=1))
def checkup():
    bot.send_message(ADMIN, "bot still running", disable_notification=True)
    t = time.localtime()
    print("bot still running at {:0>2}:{:0>2}".format(t.tm_hour, t.tm_min))

# upon program shutdown, do cleanup
def shutdown():
    tl.stop()
    t = time.localtime()
    print('{} crashed at {:0>2}:{:0>2}'.format(BOT_NAME,t.tm_hour, t.tm_min))
    bot.send_message(ADMIN, "{} crashed at {:0>2}:{:0>2}.".format(BOT_NAME,t.tm_hour, t.tm_min))

# the following commands are all for bug-testing

# sends chat id to the user

@bot.message_handler(commands=['chatid'])
def send_chatid(message):
	bot.reply_to(message, message.chat.id)

# sends name to the user

@bot.message_handler(commands=['name'])
def send_name(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    bot.reply_to(message, user.name)

# sends the current userdict to the user

@bot.message_handler(commands=['userdict'])
def send_userdict(message):
    chat_id = message.chat.id
    if chat_id == ADMIN:
        l1 = []
        for key in user_dict:
            user = user_dict[key]
            l1.append(str(key) + "\t" + user.name + "\n")
        eggs = ''.join(l1)
        if eggs == "":
            bot.reply_to(message, "Userdict empty.")
        else:
            bot.reply_to(message, eggs)
    else:
        bot.reply_to(message, "Nice try.")
        bot.send_message(ADMIN, "{} tried to access the userdict.".format(chat_id))

# sends the current blockdict to the user

@bot.message_handler(commands=['blockdict'])
def send_blockdict(message):
    chat_id = message.chat.id
    if chat_id == ADMIN:
        l1 = []
        for key in block_dict:
            user = block_dict[key]
            l1.append(str(key) + "\t" + user.name + "\n")
        eggs = ''.join(l1)
        if eggs == "":
            bot.reply_to(message, "Blockdict empty.")
        else:
            bot.reply_to(message, eggs)
    else:
        bot.reply_to(message, "Nice try.")
        bot.send_message(ADMIN, "{} tried to access the blockdict.".format(chat_id))

# adds a user with the specified chatid to the block list
# checks first if their chatid is part of the userdict
# removes them from the userdict

@bot.message_handler(commands=['block'])
def block(message):
    try:
        chat_id = message.chat.id
        if chat_id == ADMIN:
            msg = message.text
            if msg == "/block":
                bot.send_message(chat_id, "No user specified.")
            else:
                to_block = int(msg[7:])
                if to_block == ADMIN:
                    bot.send_message(chat_id, "Cannot block the admin!")
                else:
                    if to_block in block_dict:
                        bot.send_message(chat_id, "User already blocked!")
                    elif to_block in user_dict:
                        val = user_dict.pop(to_block)
                        block_dict[to_block] = val
                        bot.send_message(chat_id, "Specified chatid {} for {} has been removed.".format(to_block, val.name))
                        # add to blockdict file
                        f = open(BD_FILE, "a+")
                        f.write(str(to_block) + "\t" + val.name + "\n")
                        f.close()
                        # rewrite userdict file
                        f = open(UD_FILE, "r")
                        lines = f.readlines()
                        f.close()
                        for line in lines:
                            if re.split("\t+", line, maxsplit=1)[0] == str(to_block):
                                lines.remove(line)
                                break
                        else:
                            print("Error: chatid unable to be found in udfile")
                            bot.send_message(chat_id, "Unable to find chatid in udfile.")
                            raise Exception("Unable to find chatid in udfile.")
                        f = open(TMP_UD_FILE, "w+")
                        for line in lines:
                            f.write(line)
                        f.close()
                        print("Temporary user file written!")
                        os.remove(UD_FILE)
                        print("Userdict file removed!")
                        os.rename(TMP_UD_FILE, UD_FILE)
                        print("Userdict file replaced!")
                        bot.send_message(chat_id, "All files successfully overwritten!")
                    else:
                        bot.send_message(chat_id, "Specified chatid not in userdict!")
        else:
            bot.send_message(chat_id, "Nice try.")
            bot.send_message(ADMIN, "{} tried to use the block function.".format(chat_id))
    except Exception as e:
        bot.send_message(ADMIN, "Error in block function.")
        print(e)

# throws a ZeroDivisionError forcing a program crash

@bot.message_handler(commands=['exception'])
def div_zero(message):
    if ADMIN == message.chat.id:
        1/0
    else:
        bot.send_message(message.chat.id, "Nice try.")
        bot.send_message(ADMIN, "{} tried to crash {}.".format(message.chat.id, BOT_NAME))

# main function to initiate polling and timeloop
# upon termination of polling, run shutdown script

def main():
    try:
        tl.start()
        bot.polling()
    except Exception as e:
        bot.stop_polling()
        t = time.localtime()
        print("[{:0>2}:{:0>2}]: error caught by main/except {}".format(t.tm_hour, t.tm_min, e))
        shutdown()
    else:
        bot.stop_polling()
        t = time.localtime()
        print("error caught by main/else at {:0>2}:{:0>2}".format(t.tm_hour, t.tm_min))
        shutdown()

if __name__=='__main__':
    main()

import os 
import telebot
from dotenv import load_dotenv
import requests

# Load environment variables from the .env file
load_dotenv()

# Fetch the token from an environment variable
TOKEN = os.getenv('BOT_TOKEN')

if TOKEN is None:
    raise Exception("Bot token is not defined")




BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start','hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message,message.text)

def get_daliy_horoscope(sign:str,day:str)->dict:
    """Get daliy horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Data in format YYYY-MM-DD TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data"""

    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign":sign,"day":day}
    response = requests.get(url,params)

    return response.json()
@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces"
    sent_msg = bot.send_message(message.chat.id,text,parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg,day_handler)

def day_handler(message):
    sign = message.text
    text = "What day do you what to know?\nChoose one:*TODAY*, *TOMORROW*, *YESTERDAY*"
    sent_msg = bot.send_message(message.chat.id,text,parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg,fetch_horoscope,sign.capitalize()
    )
def fetch_horoscope(message,sign):
    day = message.text
    horoscope= get_daliy_horoscope(sign,day)
    print(horoscope)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id,"Here is your horoscope!")
    bot.send_message(message.chat.id,horoscope_message,parse_mode="Markdown")


bot.infinity_polling()
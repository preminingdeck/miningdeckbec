from bot.bot import Bot
from bot.handler import MessageHandler

TOKEN = '001.1655158285.1169112168:1003045046'
nickname = 'jahs_boy'
bot = Bot(token=TOKEN)
m = 'heyheyeheye'
def message_cb(bot, event):
    bot.send_text(chat_id=event.from_chat, text=event.text)

def send_msg(bot, cid, msg):
    bot.send_text(chat_id=cid,text=msg)

while 1:
    send_msg(bot, nickname,m )


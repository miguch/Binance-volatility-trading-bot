from telegram.ext import Updater
from threading import Thread
import time
updater = Updater(token='', use_context=True)

dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(update, context):
    logging.info('received: ' + update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola!")

targetsLines = {}
def sendLoop(update, context):
    chatId = update.effective_chat.id
    while True:
        time.sleep(60 * 7)
        logging.info('send Log data to ' + str(chatId))
        (content, lines) = readLogFile(targetsLines[chatId])
        if lines > targetsLines[chatId]:
            targetsLines[chatId] = lines
            context.bot.send_message(chat_id=chatId, text=content)
            time.sleep(1)
            context.bot.send_message(chat_id=chatId, text='record number: '+str(lines))

def executor(update, context):
    try:
        logging.info('received: ' + update.message.text)
        startLine = float(update.message.text)
        (content, lines) = readLogFile(startLine)
        context.bot.send_message(chat_id=update.effective_chat.id, text=content)
        time.sleep(1)
        context.bot.send_message(chat_id=update.effective_chat.id, text='record number: '+str(lines))
        if targetsLines.get(update.effective_chat.id) == None:
            sendThread = Thread(target=sendLoop, args=(update, context))
            sendThread.start()
        targetsLines[update.effective_chat.id] = lines
    except Exception as e:
        logging.error(e)

def readLogFile(startLine):
    with open("./trades.txt", 'r') as tradeFile:
        Lines = tradeFile.readlines()
        count = 0
        result = []
        for line in Lines:
            count += 1
            if count >= startLine:
                result.append(line)
    return (''.join(result), max(count + 1, 0))
    

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
from telegram.ext import MessageHandler, Filters
general_handler = MessageHandler(Filters.text & (~Filters.command), executor)
dispatcher.add_handler(general_handler)

updater.start_polling()

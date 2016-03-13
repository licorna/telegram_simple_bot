from TelegramBotAPI.types import sendMessage
from TelegramBot.plugin import BotPlugin
import asyncio
import os

def hola(text):
    return 'Hola ' + text

def wolfram(text):
    pass

actions = {
    'hola': hola,
    'wolf': wolfram
}

class Ping(BotPlugin):

    @asyncio.coroutine
    def startPlugin(self):
        pass

    @asyncio.coroutine
    def stopPlugin(self):
        pass

    @asyncio.coroutine
    def on_message(self, msg):
        return False

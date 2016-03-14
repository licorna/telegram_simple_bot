from TelegramBotAPI.types import sendMessage
from TelegramBot.plugin import BotPlugin
import asyncio
import wolframalpha
from config import WOLFRAM_APPID

APPNAME='Malo Bot'

TITLE_TEMPLATE = '*{title}*\n'
CODE_TEMPLATE = '```{text}```'
TEXT_TEMPLATE = '{text}'

class Wolfram(BotPlugin):

    @asyncio.coroutine
    def startPlugin(self):
        self.client = wolframalpha.Client(WOLFRAM_APPID)

    @asyncio.coroutine
    def stopPlugin(self):
        pass

    @asyncio.coroutine
    def on_message(self, msg):
        if hasattr(msg, 'text'):
            m = sendMessage()
            m.chat_id = msg.chat.id
            m.parse_mode = 'Markdown'
            if msg.text[:5] == '!wolf':
                response = self.wolf_query(wolf_params(msg.text))
                if len(response) > 0:
                    m.text = '\n'.join(filter(None, response))
                else:
                    m.text = "I don't have a response to that"
                yield from self.send_method(m)

        # if True is returned, other plugins will process the
        # same message. If False is returned, execution will not continue.
        return False

    def wolf_query(self, query):
        'Executes a query in wolfram alpha'
        if query == 'ping':
            return ['pong'] # request by mavega
        res = self.client.query(query)
        parts = []
        for pod in res.pods:
            parts.append(pod_repr(pod))
        return parts

def wolf_params(query):
    'Gets parameters of !wolf query'
    return query[6:]

def pod_repr(pod):
    'Returns a "line" from the pod, it will be title and text...'
    if not pod.text:
        return
    text = (CODE_TEMPLATE if is_no_format(pod.title) else TEXT_TEMPLATE).format(
        text=pod.text)

    return TITLE_TEMPLATE.format(title=pod.title) + text

def is_no_format(title):
    words = (
        'Derivative',
        'Indefinite integral',
        'Identities',
        'Global maxima',
        'Global minima',
        'Alternative representations',
        'Series representations',
        'Integral representations',
        'Definite integral over a half-period',
        'Definite integral mean square',
        'Alternate form',
        'Roots',
        'Properties as a real function',
        'Series expansion at x=0')
    return title in words

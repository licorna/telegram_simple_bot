from TelegramBotAPI.types import sendMessage
from TelegramBot.plugin import BotPlugin
import asyncio
import wolframalpha

APPNAME='Malo Bot'
WOLFRAM_APPID='<your wolfram appid>'

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
                    m.text = 'No entiendo la pregunta'
                yield from self.send_method(m)

        # if True is returned, other plugins will process the
        # same message. If False is returned, execution will not continue.
        return False

    def wolf_query(self, query):
        'Executes a query in wolfram alpha'
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
    return template.format(title=pod.title, text=pod.text)

template = '''*{title}*
{text}
'''

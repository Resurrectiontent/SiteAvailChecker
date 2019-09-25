import vk_api
import time

from logging import error
from BD import DB
from threading import Thread
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class VkBot(Thread):

    _GROUP_ID = '185661251'
    _VK_BOT_TOKEN = '66672c7ca1271149c73e7cd779a5068485829383e34b4e09dd166560e9a5c10103625b0eae8e8a8049a02'

    def __init__(self, welcome_msg: str):
        Thread.__init__(self, daemon=True)

        self.bd = DB()

        self._welcome_msg = welcome_msg

        self.vk_session = vk_api.VkApi(token=self._VK_BOT_TOKEN)
        self.vk = self.vk_session.get_api()
        self._longpoll = VkBotLongPoll(self.vk_session, self._GROUP_ID)

    def welcome(self, text: str):
        self._welcome_msg = text

    def send_messages(self, message: str):
        users = self.bd.get_user_ids()
        for user in users:
            self._send_msg(message,
                           user)

    def disconnect_db(self):
        self.bd.disconnect()

    def _send_msg(self, msg: str, usr):
        sent = False
        while not sent:
            try:
                self.vk.messages.send(user_id=usr,
                                      random_id=get_random_id(),
                                      message=msg)
                sent = True
            except:
                error('Message sending failed.')
                time.sleep(30)

    def poll(self):
        for event in self._longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.text.lower() == '/start':
                    if event.from_user:
                        answer = self.bd.add_user(event.obj.from_id)

                        if answer['type'] == 'Success':
                            self._send_msg('Вы будете оповещены о падениях и поъёмах сервера.',
                                           event.obj.from_id)
                            self._send_msg(self._welcome_msg,
                                           event.obj.from_id)
                        else:
                            self._send_msg(answer['value'],
                                           event.obj.from_id)

                elif event.obj.text.lower() == '/stop':
                    if event.from_user:
                        answer = self.bd.remove_user(event.obj.from_id)

                        if answer['type'] == 'Success':
                            self._send_msg('Вас больше не будут оповещать о состоянии сервера.',
                                           event.obj.from_id)
                        else:
                            self._send_msg(answer['value'],
                                           event.obj.from_id)

                elif event.obj.text == '?':
                    if event.from_user:
                        self._send_msg(self._welcome_msg,
                                       event.obj.from_id)

    def run(self):
        while True:
            try:
                self.poll()
            except:
                error('Polling failed.')
                time.sleep(30)

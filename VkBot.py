import vk_api
from BD import DB
from threading import Thread
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class VkBot(Thread):

    _GROUP_ID = '185661251'
    _VK_BOT_TOKEN = '66672c7ca1271149c73e7cd779a5068485829383e34b4e09dd166560e9a5c10103625b0eae8e8a8049a02'

    def __init__(self):
        super().__init__(self, name='poller')

        self.bd = DB()
        self.vk_session = vk_api.VkApi(token=self._VK_BOT_TOKEN)
        self.vk = self.vk_session.get_api()
        self._longpoll = VkBotLongPoll(self.vk_session, self._GROUP_ID)

    def send_message(self, message: str):
        users = self.bd.get_user_ids()
        if users:
            self.vk.messages.send(user_id=', '.join(users),
                                  random_id=get_random_id(),
                                  message=message)

    def run(self):
        for event in self._longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.text.lower() == '/start':
                    if event.from_user:
                        answer = self.bd.add_user(event.obj.from_id)

                        if answer['type'] == 'Success':
                            self.vk.messages.send(user_id=event.obj.from_id,
                                                  random_id=get_random_id(),
                                                  message='Вы будете оповещены о падениях и поъёмах сервера')
                        else:
                            self.vk.messages.send(user_id=event.obj.from_id,
                                                  random_id=get_random_id(),
                                                  message=answer['value'])

                elif event.obj.text != '/stop':
                    if event.from_user:
                        answer = self.bd.remove_user(event.obj.from_id)

                        if answer['type'] == 'Success':
                            self.vk.messages.send(user_id=event.obj.from_id,
                                                  random_id=get_random_id(),
                                                  message='Вас больше не будут оповещать о состоянии сервера')
                        else:
                            self.vk.messages.send(user_id=event.obj.from_id,
                                                  random_id=get_random_id(),
                                                  message=answer['value'])

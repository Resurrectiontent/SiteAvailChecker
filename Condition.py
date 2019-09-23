from VkBot import VkBot


class Condition:

    def __init__(self):
        self._condition = False
        self._bot = VkBot()
        self._bot.start()

    def crashed(self):
        # if condition was True
        if self._condition:
            self._condition = False
            self._bot.send_message('Сервер упал!')

    def risen(self):
        # if condition was False
        if not self._condition:
            self._condition = True
            self._bot.send_message('Сервер заработал!')

    def interrupt(self):
        self._bot.disconnect_db()

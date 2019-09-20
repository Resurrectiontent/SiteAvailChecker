import os
import requests
import random
import vk_api
import json

from vk_api import VkUpload
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

GROUP_ID = '185661251'
VK_BOT_TOKEN = '66672c7ca1271149c73e7cd779a5068485829383e34b4e09dd166560e9a5c10103625b0eae8e8a8049a02'

MINIAPP_ID = '7121215'
PROTECTED_KEY = 'FW01JGNSGvFewFfnHsYc'
MINIAPP_TOKEN ='529f842a0d06b38d6ff1fc9e67010c0848c284e37f6c0964bbcd65f2d1b80f60bc9d3338601ea3fc4a86b'

#Messaging
vk_session = vk_api.VkApi(token=VK_BOT_TOKEN)
vk = vk_session.get_api()
#Wall posting
vk_session1 = vk_api.VkApi(token=MINIAPP_TOKEN, app_id=MINIAPP_ID)
vk1 = vk_session1.get_api()

upload = VkUpload(vk_session)
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

print('polling')
for event in longpoll.listen():
    print(event)
    if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.text.lower() == 'картинка':
                if event.from_user:
                    #Chose a random image
                    image_url = '{0}\\images\\{1}'.format(os.getcwd(), random.choice(os.listdir('images')))
                    #Get server
                    data = vk.photos.getMessagesUploadServer(user_id=event.obj.from_id)

                    upload_url = data["upload_url"]
                    files = {'photo': open(image_url, 'rb')}
                    #Post an image to the server
                    response = requests.post(upload_url, files=files)
                    result = json.loads(response.text)
                    #Receive uploaded image information
                    uploadResult = vk.photos.saveMessagesPhoto(server=result["server"],
                                                   photo=result["photo"],
                                                   hash=result["hash"])

                    vk.messages.send(user_id=event.obj.from_id, 
                                     random_id = get_random_id(),
                                     attachment='{0}-{1}_{2}'.format('photo', GROUP_ID, uploadResult[0]["id"]),
                                     message = random.choice(['Пуньк', 'Бу!', 'Плюшка', 'Репа', 'Спасибо Кириллу за кириллицу!']))

            elif event.obj.text[:9] == 'На стену:':
                if event.from_user:

                    vk1.wall.post(owner_id=int('-{}'.format(GROUP_ID)),
                                 from_group=1,
                                 message=event.obj.text[10 if event.obj.text[9] in ' \t\n' else 9 :],
                                 attachments=event.obj.attachments,
                                 signed=0)

            elif event.obj.text != '':
                if event.from_user:

                    vk.messages.send(user_id=event.obj.from_id, 
                                     random_id = get_random_id(),
                                     message = "Обнаружено нарушение!"\
                                     "На территории участковой избирательной комиссии №17 (ТИК Бокситогорского муниципального района) по адресу деревня Косые Харчевни, 5 зарегистрировано нарушение."
                              )
                    vk.messages.send(user_id=event.obj.from_id, 
                                     random_id = get_random_id(),
                                     message = "Председатель УИК №17 Степанов А.В выехал на место нарушения по адресу Бокситогорский район, Ефимовское городское поселение, деревня Косые Харчевни, 5")

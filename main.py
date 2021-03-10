import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint
from vk_api.utils import get_random_id
import re
import requests
from time import sleep
from vk_api import VkApi
from vk_api.upload import VkUpload
vk_session = vk_api.VkApi(token='token')
longpoll = VkBotLongPoll(vk_session, id)
vk = vk_session.get_api()   # Выполняем авторизацию от имени сообщества
upload = VkUpload(vk)

#отправляет сообщение
def mes(vk, chat_id, message=None, attachment=None, wait=25):
    vk.messages.send(random_id=get_random_id(), chat_id=chat_id, message=message, attachment=attachment)

#загружает фото
def say_photo():
    ph = event.object.attachments[0]['photo']['sizes'][4]['url']
    p = requests.get(ph)
    out = open("file.png", "wb")
    out.write(p.content)
    out.close()
    res = upload.photo_messages('file.png')[0]
    owner_id = res['owner_id']
    photo_id = res['id']
    access_key = res['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'

    return attachment

user_id_test = []
 
restart = True
while restart == True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                    response = event.obj.text.lower()
                    object1 = event.object.attachments
                    if "1" in response:
                        info = vk.users.get(user_ids=event.obj.from_id, random_id=randint(1, 9999999))
                        fname = info[0]["first_name"]
                        mes(vk, "7", str(f" @id{event.obj.from_id} ({fname}), пожалуйста, давай не будем употреблять эти слова."))
                        if response == object1:
                            if event.object.attachments[0]['type'] == 'photo':
                                mes(vk, "8", str(f" Этот не хороший человек по имени @id{event.obj.from_id} ({fname}) материться и присылает: "), attachment=say_photo())
                        else: 
                            mes(vk, "8", str(f" Этот не хороший человек по имени @id{event.obj.from_id} ({fname}) материться"))
                            
                    if "@bot" in response:
                        info = vk.users.get(user_ids=event.obj.from_id,  random_id=randint(1, 9999999))
                        fname = info[0]["first_name"]
                        a = re.sub(r'@bot', ' ', event.obj.text)
                        user_id_test.append(event.obj.from_id)
                        mes(vk, "1", str(f" @id{event.obj.from_id} ({fname}) спрашивает: " + a))
                        
                    if response:

                        fwd_messages = event.obj.fwd_messages
                        if not fwd_messages:
                            continue
                        info = vk.users.get(user_ids=user_id_test,  random_id=randint(1, 9999999))
                        fname = info[0]["first_name"]
                        lname = info[0]["last_name"]

                        if response == object1:
                            if object1[0]['type'] == 'photo':
                                mes(vk, "7", str(f" @id{user_id_test[0]}({fname} {lname}) " + "вам пришел ответ: " + response), attachment=say_photo())

                            if object1[0]['type'] == 'video':
                                attachment = f"video{object1[0]['video']['owner_id']}_{object1[0]['video']['id']}_{object1[0]['video']['access_key']}"
                                mes(vk, "7", str(f" @id{user_id_test[0]}({fname} {lname}) " + "вам пришел ответ: " + response), attachment=attachment)
                        else:
                            mes(vk, "7", str(f" @id{user_id_test[0]}({fname} {lname}) " + "вам пришел ответ: " + response))

    except Exception as E:
        print("Ошибка, ну с кем не бывает")
        print(E)
        restart = True
        sleep(1)                

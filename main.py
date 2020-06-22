import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from modules.VkBot import VkBot
# from modules.emphasis import WordImage
import random
import requests
import json



VK_TOKEN: str = "baca3eeb386a06da54e6a9b72d31c7a60112c35080e9d21cd02685b9ba719418acc9e86f0b40f165952f7"

# Авторизация
vk = vk_api.VkApi(token=VK_TOKEN)


# Главная Клавиатура 
keyboard = VkKeyboard(one_time=True)
keyboard.add_button(label='Ударение', color=VkKeyboardColor.PRIMARY)
# keyboard.add_line()
# keyboard.add_button(label='Декабрьское сочинение', color=VkKeyboardColor.PRIMARY)

# Работа с сообщениями
longpoll = VkLongPoll(vk=vk)

def send_message(user_id, message) -> None:
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id(), 'keyboard': keyboard.get_keyboard()})

def upload_photo(upload, photo) -> None:
    response = upload.photo_messages(photo)[0]

    owner_id = response['owner_id']
    photo_id = response['id']

    return owner_id, photo_id

def send_image(command, user_id):
    if command.upper() == 'УДАРЕНИЕ' or command == '1':

        with open('./data/emphasises.json', 'r') as file:
            words = json.load(file)

        rand_int = random.randint(0, len(words)-1)
        owner_id, photo_id = upload_photo(VkUpload(vk.get_api()), open('./res/emphasises/img_{}.png'.format(rand_int), 'rb'))
        attachment = "photo{}_{}".format(owner_id, photo_id)
        vk.method("messages.send", {"peer_id": user_id, "attachment": attachment, "random_id": get_random_id(), 'keyboard': keyboard.get_keyboard()})

# Основной цикл 
for event in longpoll.listen():
    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:
        # Если оно имеет метку 'Для меня'
        if event.to_me:

            # Сообщение от пользователя
            request = event.text
            print('USER_ID:', event.user_id)
            print('NEW MESSAGE:', event.text)

            bot = VkBot(event.user_id)
            COMMANDS = bot.COMMANDS
            if event.text.upper() == COMMANDS[3] or event.text.upper() == COMMANDS[4]:
                send_image(event.text, event.user_id)
            # elif event.text.upper() == COMMANDS[5] or event.text.upper() == COMMANDS[6]:
            #     send_image(event.text, event.user_id)
            else:
                send_message(event.user_id, bot.new_message(event.text))




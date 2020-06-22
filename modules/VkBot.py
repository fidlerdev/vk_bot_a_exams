import requests
import bs4
import modules.emphasis

class VkBot:
    
    def __init__(self, user_id):
        print('Bot object created.')
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id=user_id)

        self.COMMANDS = ['НАЧАТЬ', 'ПРИВЕТ', 'ПОКА', 'УДАРЕНИЕ', '1', 'ДЕКАБРЬСКОЕ СОЧИНЕНИЕ', '2']


    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get('https://vk.com/id' + str(user_id))
        bs = bs4.BeautifulSoup(request.text, 'html.parser')
        user_name = self._clean_all_tag_from_str(bs.findAll('title')[0])
        return user_name.split()[0]

    def new_message(self, message):
        if message.upper() == self.COMMANDS[0]:
            return 'Бот сообщества находится в разработке\n По всем вопросам можете обратиться к @benjamin_me'
        elif self.COMMANDS[1] in message.upper():
            return 'Привет-привет, {}'.format(self._USERNAME)
        elif 'милый мой' in message.lower():
            return 'К олимпиадам надо готовиться с пяти лет!'
        elif message.upper() == self.COMMANDS[2]:
            return 'До скорых встреч!'
        else:
            return (
            '''
Я не совсем понимаю...

Можете воспользоваться быстрыми командами:
1. Случайное ударение
Напишите номер команды...
            '''
            )
    @staticmethod
    def _clean_all_tag_from_str(string_line):
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """
        result = ''
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == '<':
                    not_skip = False
                else:
                    result += i
            else:
                if i == '>':
                    not_skip = True
                
        return result

    



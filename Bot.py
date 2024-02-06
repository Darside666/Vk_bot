import vk_api
import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# Здесь необходимо указать токен вашего сообщества ВКонтакте
token = 'your_group_token'
# Здесь необходимо указать ID администратора, которому будет отправляться уведомление
admin_id = 'admin_vk_id'
# Здесь необходимо указать номер телефона администратора для отправки SMS
admin_phone_number = 'your_admin_phone_number'
# Здесь необходимо указать ключ API для отправки SMS
sms_api_key = 'your_sms_api_key'

def send_sms_notification(message):
    url = f'https://api.example.com/send_sms?api_key={sms_api_key}&phone_number={admin_phone_number}&message={message}'
    response = requests.get(url)
    if response.status_code == 200:
        print('SMS notification sent successfully')
    else:
        print('Failed to send SMS notification')

def check_exam_help_request(message):
    exam_help_keywords = ['срочная помощь на экзамене', 'помощь на экзамене']
    for keyword in exam_help_keywords:
        if keyword in message.lower():
            return True
    return False

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, your_group_id)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        user_id = event.object.message['from_id']
        message = event.object.message['text']

        if not check_exam_help_request(message):
            # Обработка запросов
            if 'привет' or 'здравствуйте' in message.lower():
                vk.messages.send(user_id=user_id, message='Привет, я бот!')
            
            # Отправка уведомления администратору
            vk.messages.send(user_id=admin_id, message=f'Получено сообщение от пользователя с ID {user_id}: {message}')

            # Отправка SMS-уведомления
            sms_message = f'Получено сообщение от пользователя с ID {user_id}: {message}'
            send_sms_notification(sms_message)

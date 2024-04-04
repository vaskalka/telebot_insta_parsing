import telebot
import instaloader
import json

# Открываем файл и читаем его содержимое
with open('local.dev.json', 'r') as f:
    auth_data = json.load(f)

# Получаем данные из файла
token = auth_data['token']
user = auth_data['user']
passwd = auth_data['passwd']

print('Приложение инициализировано')
# Создаем экземпляр бота
bot = telebot.TeleBot(token)

# Создаем экземпляр класса Instaloader
L = instaloader.Instaloader()


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Кинь ссылку на рилс для скачивания.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    insta_url = "https://www.instagram.com"
    if message.text.startswith(insta_url):
        try:
            # Удаляем сообщение пользователя
            bot.delete_message(message.chat.id, message.message_id)
            # Отправляем сообщение "Processing..."
            processing_message = bot.send_message(message.chat.id, "Reels initialized. Processing...")

            # Аутентификация
            L.login(user=user, passwd=passwd)
            # Вытаскиваем shortcode из URL
            shortcode = message.text.split("/")[-2]
            # Тянем данные
            reel = instaloader.Post.from_shortcode(L.context, shortcode)
            # Получаем URL видео
            video_url = reel.video_url

            # Удаляем сообщение Processing...
            bot.delete_message(processing_message.chat.id, processing_message.message_id)
            # Формируем ссылку на профиль в инстаграм
            profile_url = f'{insta_url}/{reel.owner_username}'

            # Формируем текст сообщения, прикрепленного к рилсу
            message_text = f'Отправлено пользователем: @{message.from_user.username}\n Автор reels: {profile_url}'
            # Отправляем видео
            bot.send_video(
                message.chat.id,
                video_url,
                caption=message_text
            )

        except Exception as e:
            error_message = f'Что-то пошло не так: {e}'
            bot.send_message(message.chat.id, error_message)


if __name__ == "__main__":
    bot.polling()

import telebot
import webbrowser
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
current_pet = None


@bot.message_handler(commands=['start', ])
def welcome(message):
    bot.send_message(message.chat.id,
                     f'{message.chat.username}\U0001F496 \nТебя приветсвует <b>Московский Зоопарк</b> \U0001F308 \nО '
                     f'Московском Зоопарке жми\U0001F449 /info,\nЕсли <b>хочешь</b> посетить сайт жми \U0001F449 '
                     f'/website\n<b>Вопросы</b>"Отгадай животного"'
                     f' жми\U0001F449/quiz',
                     parse_mode="HTML")


@bot.message_handler(commands=['info', ])
def info(message):
    bot.send_message(message.chat.id,
                     f'{message.chat.username}\U0001F44B \n<b>Московский Зоопарк</b> \U0001F43E - Это  один из '
                     f'старейших зоопарков Европы с уникальной коллекцией животных и профессиональным сообществом, '
                     f'\n\n\U0001F97A При нынешних темпах развития цивилизации к 2050 году могут погибнуть около 10 '
                     f'000 биологических видов. Московский зоопарк пытается сохранить их.\n\n\U0001F60A Чтобы '
                     f'выполнять природоохранную функцию, у зоопарка есть специальные программы и даже целый Центр '
                     f'воспроизведения редких видов животных.',
                     parse_mode="HTML")


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://moscowzoo.ru/animals/')


class Reptiles:
    pass


@bot.message_handler(commands=['quiz', ])
def quiz(message):
    global current_pet
    current_pet = 'first_pet'
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Кошка", callback_data="Bear")
    button2 = types.InlineKeyboardButton("Персидаская Гадюка", callback_data="Snake")
    button3 = types.InlineKeyboardButton("Медведь", callback_data="Bear")
    markup.add(button1, button2, button3)
    bot.send_photo(message.chat.id, open('photo/Zmeya.jpg', 'rb'), 'Кто это ?', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data in ["Snake", "Bear"])
def callback_message(callback):
    if callback.data == 'Snake':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'О питомце \U0001F40D', callback_data="snake_info")
        markup.add(button1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Молодец правильно\U0001F4A5', reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Не правильно\U0001F4A5', reply_markup=markup)
        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["snake_info"])
def callback_worker_calc(callback):
    if callback.data == 'snake_info':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'Накормить питомца \U0001F400', callback_data="Yes1")
        markup.add(button1)
        bot.send_video(callback.message.chat.id, open('video/persgaduk.mp4', 'rb', ), timeout=60, reply_markup=markup)
    else:
        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["Yes1"])
def main_eat(callback):
    if callback.data == "Yes1":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton('\U0001F400', )
        markup.add(button1)
        bot.send_message(callback.message.chat.id, '<b>Я хочу кушать</b> \U0001F614', parse_mode='HTML',
                         reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '\U0001F400')
def main_victorine_one(message):
    global current_pet
    if message.text == "\U0001F400":
        bot.send_message(message.chat.id,
                         f'{message.chat.username}, Спасибо я наелся\U0001F60B\nТеперь, ты мой <b>Лушчий друг '
                         f'\U00002728</b>',
                         parse_mode='HTML')
        bot.send_message(message.chat.id, 'Следующий питомец \U0001F449/two_pet')
        bot.register_next_step_handler(message, two_pet)
        current_pet = 'second_pet'


@bot.message_handler(commands=['two_pet', ])
def two_pet(message):
    global current_pet
    current_pet = 'two_pet'
    markup = types.InlineKeyboardMarkup(row_width=1)
    button4 = types.InlineKeyboardButton("Собачка", callback_data="Stop")
    button5 = types.InlineKeyboardButton("Сиамская кобра", callback_data="Pers")
    button6 = types.InlineKeyboardButton("Каракатица", callback_data="Stop")
    markup.add(button4, button5, button6)
    bot.send_photo(message.chat.id, open('photo/siams.cobra.jpg', 'rb'), 'Кто это ?', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data in ["Pers", "Stop"])
def callback_message(callback):
    if callback.data == 'Pers':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'О питомце \U0001F40D', callback_data="snake_info2")
        markup.add(button1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Совершенно верно\U0001F4A5', reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Не правильно\U0001F4A5', reply_markup=markup)
        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["snake_info2"])
def callback_message(callback):
    if callback.data == 'snake_info2':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'Накормить питомца\U0001F42D', callback_data="Pit")
        markup.add(button1)
        bot.send_photo(callback.message.chat.id, open('photo/siams.cobra.jpg', 'rb', ),
                       'Класс: Пресмыкающиеся \nОтряд: Чешуйчатые \nСемейство: Аспиды \nРод: Настоящие кобры \nВид: '
                       'Сиамская кобра \n\nМеждународное научное название: \nNaja siamensis Laurenti, 1768 \n\nЭто '
                       'кобра средней величины с довольно тонким телом по сравнению с другими кобрами. Окрас '
                       'варьирует от серого до коричневого и чёрного, с белыми пятнами или полосами.',
                       reply_markup=markup)
    else:

        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["Pit"])
def main_eat(callback):
    if callback.data == "Pit":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton('\U0001F42D', )
        markup.add(button1)
        bot.send_message(callback.message.chat.id, '<b>Я хочу кушать</b> \U0001F614', parse_mode='HTML',
                         reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '\U0001F42D')
def main_victorine_two(message):
    global current_pet
    if message.text == '\U0001F42D':
        bot.send_message(message.chat.id,
                         f'{message.chat.username}, Спасибо я наелся\U0001F60B\nТеперь, <b>Ты мой герой '
                         f'\U00002728</b>',
                         parse_mode='HTML')
    if message.text == '\U0001F42D':
        bot.send_message(message.chat.id, 'Следующий питомец \U0001F449/tree_pet')
        bot.register_next_step_handler(message, tree_pet)
        current_pet = 'second_pet'


class Birds:
    pass


@bot.message_handler(commands=['tree_pet', ])
def tree_pet(message):
    global current_pet
    current_pet = 'tree_pet'
    murkup = types.InlineKeyboardMarkup(row_width=1)
    button4 = types.InlineKeyboardButton("Мышка", callback_data="Mouse")
    button5 = types.InlineKeyboardButton("Большой тукан", callback_data="Tukan")
    button6 = types.InlineKeyboardButton("Сверчок", callback_data="Mouse")
    murkup.add(button4, button5, button6)
    bot.send_photo(message.chat.id, open('photo/tukan.jpg', 'rb'), 'Кто это ?', reply_markup=murkup)


@bot.callback_query_handler(func=lambda callback: callback.data in ["Tukan", "Mouse"])
def callback_message(callback):
    if callback.data == 'Tukan':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'О питомце \U0001F99C', callback_data="tukan_info")
        markup.add(button1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Верно\U0001F4A5', reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Не правильно\U0001F4A5', reply_markup=markup)
        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["tukan_info"])
def callback_message(callback):
    if callback.data == 'tukan_info':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'Накормить питомца\U0001F41E', callback_data="Pit2")
        markup.add(button1)
        bot.send_video(callback.message.chat.id, open('video/tukanvideo.mp4', 'rb'), reply_markup=markup)
    else:

        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["Pit2"])
def main_eat(callback):
    if callback.data == "Pit2":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton('\U0001F41E', )
        markup.add(button1)
        bot.send_message(callback.message.chat.id, '<b>Я хочу кушать</b> \U0001F41E', parse_mode='HTML',
                         reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '\U0001F41E')
def main_victorine_two(message):
    global current_pet
    if message.text == '\U0001F41E':
        bot.send_message(message.chat.id,
                         f'{message.chat.username}, Спасибо я наелся\U0001F60B\nТы, <b>чудо '
                         f'\U00002728</b>',
                         parse_mode='HTML')

    if message.text == '\U0001F41E':
        bot.send_message(message.chat.id, 'Следующий питомец \U0001F449/four_pet')
        bot.register_next_step_handler(message, four_pet)
        current_pet = 'second_pet'


@bot.message_handler(commands=['four_pet', ])
def four_pet(message):
    global current_pet
    current_pet = 'four_pet'
    murkup = types.InlineKeyboardMarkup(row_width=1)
    button4 = types.InlineKeyboardButton("Ленивец", callback_data="Len")
    button5 = types.InlineKeyboardButton("Павлин", callback_data="Pavlin")
    button6 = types.InlineKeyboardButton("Воробей", callback_data="Len")
    murkup.add(button4, button5, button6)
    bot.send_photo(message.chat.id, open('photo/pavlinphoto.jpg', 'rb'), 'Кто это ?', reply_markup=murkup)


@bot.callback_query_handler(func=lambda callback: callback.data in ["Pavlin", "Len"])
def callback_message(callback):
    if callback.data == 'Pavlin':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'О питомце \U0001F99A', callback_data="Pavlin_info")
        markup.add(button1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Умница правильно\U0001F4A5', reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Не правильно\U0001F4A5', reply_markup=markup)
        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["Pavlin_info"])
def callback_message(callback):
    if callback.data == 'Pavlin_info':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'Накормить питомца\U0001F33D', callback_data="Pit3")
        markup.add(button1)
        bot.send_video(callback.message.chat.id, open('video/pavline.mp4', 'rb'))
        bot.send_message(callback.message.chat.id,
                         f"<b>Систематика:</b>\nРусское название – Обыкновенный или индийский или синий "
                         f"павлин.\nЛатинское название –  Pavocristatus.\nАнглийское название –  (Indian) "
                         f"peafowl.\nКласс – Птицы (Aves).\nОтряд – Курообразные (Galliformes).\nСемейство – "
                         f"Фазановые  (Phasianidae).\nРод – Павлины (Pavo).\n\nСамый многочисленный вид павлинов. "
                         f"Является монотипическим видом, т.е. в нем нет подвидов, но имеется несколько цветовых "
                         f"вариаций. Такой цветовой вариацией как раз и является белый павлин,белые павлины – не "
                         f"альбиносы.", parse_mode="HTML", reply_markup=markup)

    else:

        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["Pit3"])
def main_eat(callback):
    if callback.data == "Pit3":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton('\U0001F33D', )
        markup.add(button1)
        bot.send_message(callback.message.chat.id, '<b>Я хочу кушать</b> \U0001F33D', parse_mode='HTML',
                         reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '\U0001F33D')
def main_victorine_two(message):
    global current_pet
    if message.text == '\U0001F33D':
        bot.send_message(message.chat.id,
                         f'{message.chat.username}, Спасибо я наелся\U0001F60B\nТы, <b>Верный друг '
                         f'\U00002728</b>',
                         parse_mode='HTML')

    if message.text == '\U0001F33D':
        bot.send_message(message.chat.id, 'Следующий питомец \U0001F449/five_pet')
        bot.register_next_step_handler(message, five_pet)
        current_pet = 'second_pet'


class Mammalia:
    pass


@bot.message_handler(commands=['five_pet', ])
def five_pet(message):
    global current_pet
    current_pet = 'five_pet'
    murkup = types.InlineKeyboardMarkup(row_width=1)
    button4 = types.InlineKeyboardButton("Рыбка", callback_data="Fisher")
    button5 = types.InlineKeyboardButton("Енот", callback_data="Fisher")
    button6 = types.InlineKeyboardButton("Ушастый Ёж", callback_data="Ejik")
    murkup.add(button4, button5, button6)
    bot.send_photo(message.chat.id, open('photo/04.jpg', 'rb'), 'Кто это ?', reply_markup=murkup)


@bot.callback_query_handler(func=lambda callback: callback.data in ["Ejik", "Fisher"])
def callback_message(callback):
    if callback.data == 'Ejik':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'О питомце \U0001F994', callback_data="Ejik_info")
        markup.add(button1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Ты большой молодец\U0001F4A5', reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Не правильно\U0001F4A5', reply_markup=markup)
        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["Ejik_info"])
def callback_message(callback):
    if callback.data == 'Ejik_info':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'Накормить питомца\U0001F41B', callback_data="Pit4")
        markup.add(button1)
        bot.send_photo(callback.message.chat.id, open('photo/vidy-ezhej-17.jpeg', 'rb'),
                       f"<b>Систематика:</b>\nРусское название – Ушастый ёж.\nЛатинское название – Erinaceus auritus "
                       f"или Hemiechinus auritus.\nАнглийское название – Long-eared hedgehog.\nКласс – "
                       f"Млекопитающие (Mammalia).\nОтряд – Насекомоядные (Insectivora).\nСемейство – Ежовые ("
                       f"Erinaceidae).",
                       parse_mode="HTML", reply_markup=markup)

    else:

        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["Pit4"])
def main_eat(callback):
    if callback.data == "Pit4":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton('\U0001F41B', )
        markup.add(button1)
        bot.send_message(callback.message.chat.id, '<b>Я хочу кушать</b> \U0001F614', parse_mode='HTML',
                         reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '\U0001F41B')
def main_victorine_two(message):
    global current_pet
    if message.text == '\U0001F41B':
        bot.send_message(message.chat.id,
                         f'{message.chat.username}, Спасибо я наелся\U0001F41B\nТы, <b>Верный друг '
                         f'\U00002728</b>',
                         parse_mode='HTML')

    if message.text == '\U0001F41B':
        bot.send_message(message.chat.id, 'Следующий питомец \U0001F449/six_pet')
        bot.register_next_step_handler(message, six_pet)
        current_pet = 'second_pet'


@bot.message_handler(commands=['six_pet', ])
def six_pet(message):
    global current_pet
    current_pet = 'six_pet'
    murkup = types.InlineKeyboardMarkup(row_width=1)
    button4 = types.InlineKeyboardButton("Панда", callback_data="Panda")
    button5 = types.InlineKeyboardButton("Енот", callback_data="Makaka")
    button6 = types.InlineKeyboardButton("Ушастый Ёж", callback_data="Makaka")
    murkup.add(button4, button5, button6)
    bot.send_photo(message.chat.id, open('photo/pands.jpg', 'rb'), 'Кто это ?', reply_markup=murkup)


@bot.callback_query_handler(func=lambda callback: callback.data in ["Panda", "Makaka"])
def callback_message(callback):
    if callback.data == 'Panda':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'О питомце 🐼', callback_data="Panda_info")
        markup.add(button1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Ты большой молодец\U0001F4A5', reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=1)
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Не правильно\U0001F4A5', reply_markup=markup)
        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["Panda_info"])
def callback_message(callback):
    if callback.data == 'Panda_info':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button1 = types.InlineKeyboardButton(f'Накормить питомца🎋', callback_data="Pit5")
        markup.add(button1)
        bot.send_photo(callback.message.chat.id, open('photo/panda2.jpg', 'rb'),
                       f"<b>Систематика:</b>\nРусское название – Большая панда, панда, бамбуковый медведь.\nЛатинское "
                       f"название – Ailuropoda melanoleuca.\nАнглийское название – Giant panda , panda bear, "
                       f"panda.\nКласс – Млекопитающие (Mammalia).\nОтряд – Хищные (Carvinora).\nСемейство – Медвежьи "
                       f"(Ursidae).\nРод – Большие панды (Ailuropoda).\n\nНа родине этого зверя, в Китае, "
                       f"его называют «медведь-кошка»..",
                       parse_mode="HTML", reply_markup=markup)

    else:

        return


@bot.callback_query_handler(func=lambda callback: callback.data in ["Pit5"])
def main_eat(callback):
    if callback.data == "Pit5":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton('🎋', )
        markup.add(button1)
        bot.send_message(callback.message.chat.id, '<b>Я хочу кушать</b> \U0001F614', parse_mode='HTML',
                         reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🎋')
def main_victorine_two(message):
    global current_pet
    if message.text == '🎋':
        bot.send_message(message.chat.id,
                         f'{message.chat.username}, Спасибо я наелся\U0001F41B\nТы, <b>Верный друг '
                         f'\U00002728</b>',
                         parse_mode='HTML')

    if message.text == '🎋':
        bot.send_message(message.chat.id, 'Следующий питомец \U0001F449/victorines')
        bot.register_next_step_handler(message, victorines)
        current_pet = 'second_pet'


class Victorines:
    pass


@bot.message_handler(commands=['victorines', ])
def victorines(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    button = types.InlineKeyboardButton('Коала', callback_data='Coal')
    button1 = types.InlineKeyboardButton('Верблюд', callback_data='Coal')
    button2 = types.InlineKeyboardButton('Панда', callback_data='Okey')
    button3 = types.InlineKeyboardButton('Слон', callback_data="Coal")
    markup.add(button, button1, button2, button3)
    bot.send_message(message.chat.id, 'Какое животное обитает в <b> Китае </b>?', parse_mode="HTML",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data in ['Okey', 'Coal'])
def callback_data(callback):
    if callback.data == 'Okey':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button = types.InlineKeyboardButton('продолжить', callback_data='Next2')
        markup.add(button)
        bot.send_message(callback.message.chat.id, '☀️Правильно☀️', reply_markup=markup)
    else:
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Читай внимательно\U0001F4A5')


@bot.callback_query_handler(func=lambda callback: callback.data in ['Next2'])
def victorines_2(callback):
    if callback.data == 'Next2':
        markup = types.InlineKeyboardMarkup(row_width=2)
        button = types.InlineKeyboardButton('Овчар', callback_data='Ovchar')
        button1 = types.InlineKeyboardButton('Козёл', callback_data='Ovchar')
        button2 = types.InlineKeyboardButton('Баран', callback_data='Baran')
        button3 = types.InlineKeyboardButton('Овцебык', callback_data='Ovchar')
        markup.add(button, button1, button2, button3)
        bot.send_message(callback.message.chat.id, 'Муж<b> Овцы </b>?', parse_mode="HTML", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data in ['Baran', 'Ovchar'])
def callback_data(callback):
    if callback.data == 'Baran':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button = types.InlineKeyboardButton('продолжить', callback_data='Next3')
        markup.add(button)
        bot.send_message(callback.message.chat.id, '☀️Какой молодец☀️', reply_markup=markup)
    else:
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Читай внимательно\U0001F4A5')


@bot.callback_query_handler(func=lambda callback: callback.data in ['Next3'])
def victorines_3(callback):
    if callback.data == 'Next3':
        markup = types.InlineKeyboardMarkup(row_width=2)
        button = types.InlineKeyboardButton('Страус', callback_data='Ping')
        button1 = types.InlineKeyboardButton('Пингвин', callback_data='Ping')
        button2 = types.InlineKeyboardButton('Киви', callback_data='Ping')
        button3 = types.InlineKeyboardButton('Гусь', callback_data='Gus')
        markup.add(button, button1, button2, button3)
        bot.send_message(callback.message.chat.id, 'Какая из этих<b> Птиц </b>умеет летать?', parse_mode="HTML",
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data in ['Ping', 'Gus'])
def callback_data(callback):
    if callback.data == 'Gus':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button = types.InlineKeyboardButton('продолжить', callback_data='Next4')
        markup.add(button)
        bot.send_message(callback.message.chat.id, '☀️Совершенно верное☀️', reply_markup=markup)
    else:
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Читай внимательно\U0001F4A5')


@bot.callback_query_handler(func=lambda callback: callback.data in ['Next4'])
def victorines_4(callback):
    if callback.data == 'Next4':
        markup = types.InlineKeyboardMarkup(row_width=2)
        button = types.InlineKeyboardButton('Воздуха', callback_data='Air')
        button1 = types.InlineKeyboardButton('Мудрости', callback_data='Wisdom')
        button2 = types.InlineKeyboardButton('Лени', callback_data='Air')
        button3 = types.InlineKeyboardButton('Терпения', callback_data='Air')
        markup.add(button, button1, button2, button3)
        bot.send_message(callback.message.chat.id, 'Символ чего является<b> Сова </b>?', parse_mode="HTML",
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data in ['Wisdom', 'Air'])
def callback_data(callback):
    if callback.data == 'Wisdom':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button = types.InlineKeyboardButton('продолжить', callback_data='Next5')
        markup.add(button)
        bot.send_message(callback.message.chat.id, '😊Отлично😊', reply_markup=markup)
    else:
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Читай внимательно\U0001F4A5')


@bot.callback_query_handler(func=lambda callback: callback.data in ['Next5'])
def victorines_4(callback):
    if callback.data == 'Next5':
        markup = types.InlineKeyboardMarkup(row_width=2)
        button = types.InlineKeyboardButton('Пещерные', callback_data='Cave')
        button1 = types.InlineKeyboardButton('Горные', callback_data='Mountains')
        button2 = types.InlineKeyboardButton('Марсианские', callback_data='Cave1')
        button3 = types.InlineKeyboardButton('Подводные', callback_data='Cave')
        markup.add(button, button1, button2, button3)
        bot.send_message(callback.message.chat.id, 'Какие<b> Козы </b>бывают в природе?', parse_mode="HTML",
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data in ['Mountains', 'Cave', 'Cave1'])
def callback_data(callback):
    if callback.data == 'Mountains':
        markup = types.InlineKeyboardMarkup(row_width=1)
        button4 = types.InlineKeyboardButton('Узнай Кто ты )', callback_data='Next6')
        markup.add(button4)
        bot.send_message(callback.message.chat.id, '🔥Я в тебе не сомневался🔥', reply_markup=markup)
    elif callback.data == 'Cave1':
        bot.send_message(callback.message.chat.id, f'😅 Сам ты марсианский, подумай 😅')
    else:
        bot.send_message(callback.message.chat.id, f'\U0001F4A5Читай внимательно\U0001F4A5')


@bot.callback_query_handler(func=lambda callback: callback.data in ['Next6'])
def victorines_6(callback):
    if callback.data == 'Next6':
        bot.send_photo(callback.message.chat.id, open('photo/shim.jpg', 'rb'),
                       'Ты такой же умный и смешной\U0001F648 \b\n<b>Шимпанзе</b> – это млекопитающие животные из '
                       'семейства приматов.\n<b>Выделяют два вида</b> – это обыкновенный и карликовый '
                       'шимпанзе.\nЖивут они в Африке группами по 10-12 особей в каждой, ночуют на '
                       'деревьях.\nШимпанзе считаются самыми близкими родственниками <b>человеку</b> из животных. '
                       '\nСлово шимпанзе в переводе с языка коренных жителей Африки – племени луба означает подобный '
                       '<b>человеку</b>. Сходство ДНК человека и шимпанзе составляет 90%.',
                       parse_mode="HTML")
        bot.send_message(callback.message.chat.id, f'Ты дорогой друг {callback.message.chat.username} \U0001F496, '
                                                   f'только что сделал наших животных счастливыми и веселыми ,'
                                                   f'ты кормил и смеялся \U0001F602,тем самым спасая много животных '
                                                   f'мы тебе благодарны .\nА животные теперь всегда будут рядом с '
                                                   f'тобой\U0001F49F.')
        bot.send_message(callback.message.chat.id, 'Если захочешь приходи к нам  в <b>Московский Зоопарк</b> покормим '
                                                   'и посмеемся вместе с нашими друзьями . Узнать подробно переходи '
                                                   '/site', parse_mode="HTML")

        bot.send_message(callback.message.chat.id, 'Если хочешь попробовать еще раз переходи /quiz')


bot.polling(none_stop=True)

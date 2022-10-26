from config import TOKEN

import telebot
from telebot.types import (

    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton

)

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome_message(message):
    print(message)
    data_text = "Hello, Python !"
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    menu = InlineKeyboardButton("Меню", callback_data="menu")
    markup.add(menu)
    feedback_btn = InlineKeyboardButton("Оставить отзыв", callback_data="feedback")
    markup.add(feedback_btn)
    bot.send_message(message.chat.id, text=data_text, reply_markup=markup)


categories = {
    "first_meals": ["Борщ", "Чечевичный", "Окрошка"],
    "second_meals": ["Лагман", "Плов", "Спагетти"],
    "sweets": ["яблочный пирог", "шоколадный пирог", "пудинг"],
    "drinks": ["Cola", "sprite", "сок"]
}

food_prices = {
    categories["first_meals"][0]: 350,
    categories["first_meals"][1]: 400,
    categories["first_meals"][2]: 350,
    categories["second_meals"][0]: 450,
    categories["second_meals"][1]: 400,
    categories["second_meals"][2]: 390,
    categories["sweets"][0]: 300,
    categories["sweets"][1]: 350,
    categories["sweets"][2]: 470,
    categories["drinks"][0]: 150,
    categories["drinks"][1]: 135,
    categories["drinks"][2]: 250,
}


@bot.callback_query_handler(func=lambda call: call.data == "menu")
def answer_menu_callback(call):
    message = call.message
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    keys_of_dict = categories.keys()
    if keys_of_dict:
        for category in keys_of_dict:
            btn = InlineKeyboardButton(category, callback_data=category)
            markup.add(btn)
        back = InlineKeyboardButton("Назад", callback_data="back_to_menu")
        markup.add(back)
        bot.edit_message_text(chat_id=message.chat.id, text="Choose category", message_id=message.message_id,
                              reply_markup=markup)
    else:
        bot.edit_message_text(chat_id=message.chat.id, text="Sorry, Menu not available")


categories_keys = list(categories.keys())


@bot.callback_query_handler(func=lambda call: call.data in categories_keys)
def answer_category_callback(call):
    message = call.message
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    back = InlineKeyboardButton("Назад", callback_data="back_to_categories")
    markup.add(back)
    if call.data == categories_keys[0]:
        for meal in categories["first_meals"]:
            btn = InlineKeyboardButton(meal, callback_data=meal)
            markup.add(btn)

        bot.edit_message_text(
            chat_id=message.chat.id,
            text="Choose meal: ",
            message_id=message.id,
            reply_markup=markup
        )

    elif call.data == categories_keys[1]:
        for meal in categories["second_meals"]:
            btn = InlineKeyboardButton(meal, callback_data=meal)
            markup.add(btn)

        bot.edit_message_text(
            chat_id=message.chat.id,
            text="Choose meal: ",
            message_id=message.id,
            reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: str(call.data).startswith("back_to"))
def back_button(call):
    message = call.message
    if call.data == "back_to_menu":
        send_welcome_message(message)
    elif call.data == "back_to_categories":
        answer_menu_callback(call)
    print(call)


food_prices_keys = food_prices.keys()
food_prices_keys_list = list(food_prices_keys)


@bot.callback_query_handler(func=lambda call: call.data in food_prices_keys_list)
def get_meal_info(call):
    message = call.message
    message_date = message.date
    print(message_date)
    if call.data in food_prices_keys_list:
        if call.data == "Борщ":
            food_data = food_prices['Борщ']
            text = f" Meal {call.data} have price {food_data} som"
            bot.send_message(message.chat.id, text=text, reply_markup=None)
    if call.data in food_prices_keys_list:
        if call.data == "Чечевичный":
            food_data = food_prices['Чечевичный']
            text = f" Meal {call.data} have price {food_data} som"
            bot.send_message(message.chat.id, text=text, reply_markup=None)


@bot.callback_query_handler(func=lambda call: call.data == "feedback" )
def answer_of_feedback_callback(call):
    message = call.message
    print(message)
    text = "Напишите свой отзыв о нашем сервисе: "
    bot.send_message(message.chat.id, text, reply_markup=None)
    bot.register_next_step_handler(message=message, callback=get_feedback)


def get_feedback(message):
    #TODO: text, username, data
    from datetime import datetime
    text_of_message = message.text
    print(text_of_message)
    username = message.from_user.username
    print(username)
    message_date_time = message.date
    message_conv_time = datetime.fromtimestamp(message_date_time).strftime("%d-%m-%Y %H:%M:%S")
    print(message_conv_time)
    with open("feedbacks.txt", "a", encoding="utf-8") as file:
        full_text = f"""
        Время создания: {message_conv_time}
        Логин пользователя: {username}
        Текст отзыва: {text_of_message}
    """
        file.write(full_text)


"""
Создать функцию, которая получает данные заказа и заказчика (со временем)
и сохраняет их в текстовом файле с названием orders.txt. 
Можете определить кнопку заказать, которая передается пользователю,
при получении цены на блюдо. 
Пользователь должен переслать сообщение с названием блюда и его ценой
"""

bot.polling()
import DBflags
import telebot
from telebot import types
import configure

client = telebot.TeleBot(configure.config["token"])

def for_end(message):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_end = types.KeyboardButton("end")
    reply_markup.add(button_end)
    mes_id = client.send_message(message.chat.id, 'Press -end- to delete messages from chat.',
                                 reply_markup=reply_markup).id
    DBflags.add_id(message.from_user.id, mes_id)


def for_end_inCall(call):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_end = types.KeyboardButton("end")
    reply_markup.add(button_end)
    mes_id = client.send_message(call.message.chat.id, 'Press -end- to delete messages from chat.',
                                 reply_markup=reply_markup).id
    DBflags.add_id(call.from_user.id, mes_id)


def for_add(message):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("it's all")
    reply_markup.add(button)
    mes_id = client.send_message(message.message.chat.id, 'Press -it\'s all- to end adding process.',
                                 reply_markup=reply_markup).id
    DBflags.add_id(message.from_user.id, mes_id)


def for_cancel(message):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("cancel")
    reply_markup.add(button)
    mes_id = client.send_message(message.message.chat.id, 'Press -cancel- to cancel an operation.',
                                 reply_markup=reply_markup).id
    DBflags.add_id(message.from_user.id, mes_id)


def buttons(message):
    inline_button = types.InlineKeyboardMarkup()
    button_new = types.InlineKeyboardButton(text="NEW", callback_data="NEW")
    button_add = types.InlineKeyboardButton(text="ADD", callback_data="ADD")
    button_watch = types.InlineKeyboardButton(text="WATCH", callback_data="WATCH")
    inline_button.add(button_new, button_add, button_watch)
    button_delete = types.InlineKeyboardButton(text="DELETE ALBUM", callback_data="DELETE ALBUM")
    inline_button.add(button_delete)
    mes_id = client.send_message(message.chat.id, "Choose an option: ", reply_markup=inline_button).id
    DBflags.add_id(message.from_user.id, mes_id)


def buttons_inCall(call):
    inline_button = types.InlineKeyboardMarkup()
    button_new = types.InlineKeyboardButton(text="NEW", callback_data="NEW")
    button_add = types.InlineKeyboardButton(text="ADD", callback_data="ADD")
    button_watch = types.InlineKeyboardButton(text="WATCH", callback_data="WATCH")
    inline_button.add(button_new, button_add, button_watch)
    button_delete = types.InlineKeyboardButton(text="DELETE ALBUM", callback_data="DELETE ALBUM")
    inline_button.add(button_delete)
    mes_id = client.send_message(call.message.chat.id, "Choose an option: ", reply_markup=inline_button).id
    DBflags.add_id(call.from_user.id, mes_id)
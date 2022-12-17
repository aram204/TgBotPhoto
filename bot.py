from configure import info
import DBcontent
from buttons import *
import re

@client.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.from_user.id

    if DBcontent.exist(user_id) and DBflags.get_value(user_id, "flag_of_New") == True:
        DBflags.add_id(user_id, message.id)
        mes_id = client.send_message(message.chat.id, "Write another title:").id
        DBflags.add_id(user_id, mes_id)

    elif DBcontent.exist(user_id):
        DBflags.add_id(user_id, message.id)
        mes_id = client.send_message(message.chat.id, info).id
        DBflags.add_id(user_id, mes_id)
        for_end(message)
        buttons(message)
    
    else:
        DBcontent.create(user_id)
        DBflags.create(user_id)
        mes_id = client.send_message(message.chat.id, info).id
        DBflags.add_id(user_id, mes_id)
        for_end(message)
        buttons(message)
        client.delete_message(user_id, message.id)
        DBflags.delete_id(user_id, message.id)

@client.callback_query_handler(func = lambda call: True)
def callback(call):
    user_id = call.from_user.id

    if call.data == "NEW":
        for_cancel(call)
        mes_id = client.send_message(call.message.chat.id, "Write a title for an album:").id
        DBflags.add_id(user_id, mes_id)
        DBflags.change_value(user_id, "flag_of_New", True)


    elif call.data == "ADD":
        inline_button = types.InlineKeyboardMarkup()
        albums = DBcontent.get_albums(user_id)

        if len(albums) == 0:
            mes_id = client.send_message(call.message.chat.id, "You haven't got any albums. Create an album to add a photo or a video.").id
            DBflags.add_id(user_id, mes_id)
        
        else:
            for album in albums:
                button = types.InlineKeyboardButton(text=album, callback_data = album)
                inline_button.add(button)
            for_cancel(call)
            mes_id = client.send_message(call.message.chat.id, "Choose an album where you want to add photos or videos:", reply_markup=inline_button).id
            DBflags.add_id(user_id, mes_id)
            DBflags.change_value(user_id, "flag_of_Add", True)

        

    elif call.data == "WATCH":
        inline_button = types.InlineKeyboardMarkup()
        albums = DBcontent.get_albums(user_id)

        if len(albums) == 0:
            mes_id = client.send_message(call.message.chat.id, "You haven't got any albums.").id
            DBflags.add_id(user_id, mes_id)
        
        else:
            for album in albums:
                button = types.InlineKeyboardButton(text=album, callback_data = album)
                inline_button.add(button)
            for_cancel(call)
            mes_id = client.send_message(call.message.chat.id, "Choose an album which you want to watch:", reply_markup=inline_button).id
            DBflags.add_id(user_id, mes_id)
            DBflags.change_value(user_id, "flag_of_Watch", True)

    
    elif call.data == "DELETE ALBUM":
        inline_button = types.InlineKeyboardMarkup()
        albums = DBcontent.get_albums(user_id)
        if len(albums) == 0:
            mes_id = client.send_message(call.message.chat.id, "You haven't got any albums.").id
            DBflags.add_id(user_id, mes_id)

        else:
            for album in albums:
                button = types.InlineKeyboardButton(text=album, callback_data = album)
                inline_button.add(button)
            mes_id = client.send_message(call.message.chat.id, "Choose which album you want to delete:", reply_markup=inline_button).id
            DBflags.add_id(user_id, mes_id)
            DBflags.change_value(user_id, "del_alb", True)
            for_cancel(call)

    elif DBflags.get_value(user_id, "flag_of_Add") == True:
        DBflags.change_value(user_id, "chosen_album", call.data)
        mes_id = client.send_message(call.message.chat.id, "Now send your photos.").id
        DBflags.add_id(user_id, mes_id)
        for_add(call)


    elif DBflags.get_value(user_id, 'flag_of_Watch') == True:
        photos = DBcontent.watch_photos(user_id, call.data)
        for index in range(len(photos)):
            try:    
                mes_id = client.send_photo(call.message.chat.id, photos[index]).id
            except:
                mes_id = client.send_video(call.message.chat.id, photos[index]).id
            DBflags.add_id(user_id, mes_id)
            mes_id = client.send_message(call.message.chat.id, f"{index+1}").id
            DBflags.add_id(user_id, mes_id)
            
        mes_id = client.send_message(call.message.chat.id, "Here your photos.").id
        DBflags.add_id(user_id, mes_id)
        DBflags.change_value(user_id, "flag_of_Watch", False)

        inline_button = types.InlineKeyboardMarkup()
        button_yes = types.InlineKeyboardButton(text="YES", callback_data = "YES")
        button_no = types.InlineKeyboardButton(text="NO", callback_data="NO")
        inline_button.add(button_yes, button_no)
        mes_id = client.send_message(call.message.chat.id, "Do you want to delete anything?", reply_markup=inline_button).id
        DBflags.add_id(user_id, mes_id)
        DBflags.change_value(user_id, "chosen_album", call.data)
        DBflags.change_value(user_id, "del_ph", True)
        
    
    elif DBflags.get_value(user_id, 'del_alb') == True:
        reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Yes")
        button2 = types.KeyboardButton("No")
        reply.add(button1, button2)
        mes_id = client.send_message(call.message.chat.id, f"Are you sure that you want to delete album '{call.data}' with all photos and videos in it?", reply_markup=reply).id
        DBflags.add_id(user_id, mes_id)
        DBflags.change_value(user_id, "chosen_album", call.data)


    elif DBflags.get_value(user_id, "del_ph") == True and call.data == "YES":
        reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("delete")
        cancel = types.KeyboardButton("cancel")
        reply.add(button, cancel)
        mes_id = client.send_message(call.message.chat.id, "Send us indexes of photos written under them that you want to delete, then press -delete-.", reply_markup=reply).id
        DBflags.add_id(user_id, mes_id)

    elif DBflags.get_value(user_id, "del_ph") == True and call.data == "NO":
        mes_id = client.send_message(call.message.chat.id, "OK, you'll just watch your photos and videos.").id
        DBflags.add_id(user_id, mes_id)
        DBflags.change_value(user_id, "del_ph", False)
        for_end_inCall(call)
        buttons_inCall(call)
        

@client.message_handler(content_types=['text'])
def get_info(message):

    user_id = message.from_user.id
    DBflags.add_id(user_id, message.id)

    if message.text == 'cancel':
        DBflags.change_value(user_id, "flag_of_New", False)
        DBflags.change_value(user_id, "flag_of_Add", False)
        DBflags.change_value(user_id, "flag_of_Watch", False)
        DBflags.change_value(user_id, "del_alb", False)
        DBflags.change_value(user_id, "del_ph", False)
        DBflags.change_value(user_id, "chosen_album", None)
        DBflags.change_value(user_id, "photos_to_del", [])
        mes_id = client.send_message(message.chat.id, "OK, nothing will be done.").id
        DBflags.add_id(user_id, mes_id)
        for_end(message)
        buttons(message)

    elif DBflags.get_value(user_id, "flag_of_New") == True:
        if message.text in DBcontent.get_albums(user_id):
            mes_id = client.send_message(message.chat.id, f"You already have an album with the name '{message.text}'. Write another title.").id
            DBflags.add_id(user_id, mes_id)

        elif message.text == "end":
            mes_id = client.send_message(message.chat.id, "Write another title.").id
            DBflags.add_id(user_id, mes_id)

        else:
            DBcontent.new_album(message.from_user.id, message.text)
            mes_id = client.send_message(message.chat.id, f"We created an album with the name '{message.text}'.").id
            DBflags.add_id(user_id, mes_id)
            DBflags.change_value(user_id, "flag_of_New", False)
            for_end(message)
            buttons(message)


    elif message.text == "end":
        ids = DBflags.get_value(user_id, "message_ids")
        
        for id in range(len(ids)-1, 0, -1):
            client.delete_message(message.chat.id, ids[id])
            DBflags.delete_id(user_id, ids[id])
        DBflags.change_value(user_id, "flag_of_New", False)
        DBflags.change_value(user_id, "flag_of_Add", False)
        DBflags.change_value(user_id, "flag_of_Watch", False)
        DBflags.change_value(user_id, "del_alb", False)
        DBflags.change_value(user_id, "del_ph", False)
        DBflags.change_value(user_id, "chosen_album", None)
        for_end(message)
        buttons(message)

    elif DBflags.get_value(message.from_user.id, "flag_of_Add") == True and message.text == "it's all":
        mes_id = client.send_message(message.chat.id, "We have added your photos to album.").id
        DBflags.add_id(user_id, mes_id)
        for_end(message)
        buttons(message)
        DBflags.change_value(user_id, "flag_of_Add", False)
    
    elif DBflags.get_value(user_id, 'del_alb') == True and message.text == "Yes":
        album = DBflags.get_value(user_id, "chosen_album")
        DBcontent.delete_album(user_id, album)
        DBflags.change_value(user_id, "del_alb", False)
        mes_id = client.send_message(message.chat.id, f"Album '{album}' was deleted.").id
        DBflags.add_id(user_id, mes_id)
        for_end(message)
        buttons(message)

    elif DBflags.get_value(user_id, 'del_alb') == True and message.text == "No":
        DBflags.change_value(user_id, "del_alb", False)
        mes_id = client.send_message(message.chat.id, f"Ok, nothing will be deleted.").id
        DBflags.add_id(user_id, mes_id)
        for_end(message)
        buttons(message)

    elif DBflags.get_value(user_id, 'del_ph') == True and message.text == "Yes":
        indexes = sorted(DBflags.get_value(user_id, "photos_to_del"), reverse=True)

        for index in indexes:
            DBcontent.delete_photo(user_id, DBflags.get_value(user_id, "chosen_album"), index)
        DBflags.clean_del(user_id)
        mes_id = client.send_message(message.chat.id,
                                     f"All what you have sent was deleted from album '{DBflags.get_value(user_id, 'chosen_album')}'").id
        DBflags.add_id(user_id, mes_id)
        DBflags.change_value(user_id, "del_ph", False)
        for_end(message)
        buttons(message)

    elif DBflags.get_value(user_id, 'del_ph') == True and message.text == "No":
        mes_id = client.send_message(message.chat.id, "OK, nothing will be deleted.")
        DBflags.add_id(user_id, mes_id)
        DBflags.change_value(user_id, "del_ph", False)
        for_end(message)
        buttons(message)
    
    elif DBflags.get_value(user_id, 'del_ph') == True and message.text == "delete":
        reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Yes")
        button2 = types.KeyboardButton("No")
        reply.add(button1, button2)
        mes_id = client.send_message(message.chat.id, "Are you sure you want to delete what you have sent?", reply_markup=reply).id
        DBflags.add_id(user_id, mes_id)

    elif DBflags.get_value(user_id, 'del_ph') == True:
        indexes = re.findall("[0-9]+", message.text)
        for index in indexes:
            if 0 <= int(index)-1 < len(DBcontent.watch_photos(user_id, DBflags.get_value(user_id, "chosen_album"))):
                DBflags.add_to_del(user_id, int(index)-1)
            else:
                mes_id = client.send_message(message.chat.id, f"You haven't got photo or video with index {index}").id
                DBflags.add_id(user_id, mes_id)




@client.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    DBflags.add_id(user_id, message.id)

    if DBflags.get_value(user_id, "flag_of_Add") == True:
        DBcontent.add_photo(user_id,
                            DBflags.get_value(user_id, "chosen_album"),
                            message.photo[0].file_id
                            )

@client.message_handler(content_types=['video'])
def handle_video(message):
    user_id = message.from_user.id
    DBflags.add_id(user_id, message.id)

    if DBflags.get_value(user_id, "flag_of_Add") == True:
        DBcontent.add_photo(user_id,
                            DBflags.get_value(user_id, "chosen_album"),
                            message.video.file_id
                            )



client.polling(none_stop=True, interval=0)
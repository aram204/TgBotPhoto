import pymongo
from configure import server

client = pymongo.MongoClient(server)

db = client.telegram_users
coll = db.flags

coll.drop()

def create(user_id):
    new_doc = {
        "_id" : user_id,
        "flag_of_New" : False,
        "flag_of_Add" : False,
        "flag_of_Watch" : False,
        "message_ids" : [],
        "chosen_album" : None,
        "del_alb" : False,
        "del_ph" : False,
        "photos_to_del" : [],
    }
    coll.insert_one(new_doc)


def change_value(user_id, key, value):
    coll.update_one(
        {"_id" : user_id},
        {"$set" : {key : value}}
    )

def get_value(user_id, key):
    return coll.find_one(
        {"_id" : user_id},
        {"_id" : 0, key : 1}
    )[key]

def add_id(user_id, id):
    coll.update_one(
        {"_id" : user_id},
        {"$push" : {"message_ids" : id}}
    )

def delete_id(user_id, id):
    coll.update_one(
        {"_id" : user_id},
        {"$pull" : {"message_ids" : id}}
    )

def add_to_del(user_id, index):
    coll.update_one(
        {"_id" : user_id},
        {"$push" : {"photos_to_del" : index}}
    )

def clean_del(user_id):
    coll.update_one(
        {"_id" : user_id},
        {"$set" : {"photos_to_del" : []}}
    )

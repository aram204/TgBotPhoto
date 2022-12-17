import pymongo
from configure import server

client = pymongo.MongoClient(server)

db = client.telegram_users
coll = db.content

coll.drop()

def create(user_id):
    new_user = {
        "_id": user_id,
        "albums": {}
    }

    coll.insert_one(new_user)


def new_album(user_id, album_name):
    coll.update_one(
        {"_id": user_id},
        {"$set": {f"albums.{album_name}": []}}
    )


def add_photo(user_id, album_name, photo):
    coll.update_one(
        {"_id": user_id},
        {"$push": {f"albums.{album_name}": photo}}
    )



def watch_photos(user_id, album_name):
    return coll.find_one({"_id": user_id})['albums'][album_name]


def get_albums(user_id):
    albums = coll.find_one({"_id" : user_id}, {"_id" : 0})
    return albums["albums"]

def exist(user_id):
    return bool(coll.find_one({"_id" : user_id}))

def delete_photo(user_id, album, index):
    photo = coll.find_one({"_id" : user_id})['albums'][album][index]
    coll.update_one(
        {"_id" : user_id},
        {"$pull" : {f"albums.{album}" : photo}}
    )

def delete_album(user_id, album):
    coll.update_one(
        {"_id" : user_id},
        {"$unset" : {f"albums.{album}" : 1}}
    )

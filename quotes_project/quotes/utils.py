from pymongo import MongoClient

def get_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.banch
    return db
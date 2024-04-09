from pymongo import MongoClient

MONGO_URI = "mongodb+srv://sukeshthapa2023:ggubtAtMZSD7whvB@mongo.8uskutm.mongodb.net/?retryWrites=true&w=majority&appName=mongo"

def get_database():
    client = MongoClient(MONGO_URI)
    return client["library_db"]



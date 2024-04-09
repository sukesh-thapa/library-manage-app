from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb+srv://sukeshthapa2023:ggubtAtMZSD7whvB@mongo.8uskutm.mongodb.net/?retryWrites=true&w=majority&appName=mongo"

# Function to connect to MongoDB Atlas and return the database instance
def get_database():
    client = MongoClient(MONGO_URI)
    return client["library_db"]



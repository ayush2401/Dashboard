import pymongo 

connection_string = "mongodb+srv://ayushsaraf1:sarafayush1@cluster0.qyb7ajd.mongodb.net/"
client = pymongo.MongoClient(connection_string)
db = client['blackcof']
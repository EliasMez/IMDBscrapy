from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")
imdb = client.IMDB
collection = imdb.IMDB

def data1():
    data = collection.find({"isFilm":1}).sort("duree", -1).limit(1)
    return data

def data2():
    data = collection.find({"isFilm":1}).sort("score", -1).limit(5)
    return data

# n = collection.find({"isFilm": 1, "acteurs": {"$in": ["Morgan Freeman"]} }).count()
# print(n)

# data = collection.find({"isFilm": 1, "genre": "Horreur"}).sort("score", -1).limit(3)
# print([doc['titre'] for doc in data])

# col = collection.find({"isFilm": 1}).sort("score", -1).limit(100)
# print([(doc['titre'],doc['score']) for doc in col if 'France' in doc['pays']])
# # États-Unis


# for genre in collection.distinct("genre"):
#      if collection.count_documents({"genre": genre, "isFilm": 1}) > 0:
#         result = collection.aggregate([
#             {"$match": {"genre": genre,"isFilm": 1}},
#             {"$group": {"_id": "null", "avg_duree": {"$avg": "$duree"}}}
#         ])
#         print([(genre,round(doc["avg_duree"],2)) for doc in result])



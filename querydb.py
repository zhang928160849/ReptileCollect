import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'jia36'
# MONGO_COLLECTION = 'users_female'
MONGO_COLLECTION = 'user_male'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
f=open('out.txt','w',encoding='UTF-8-sig')
for i in collection.find():
    print(i)
    i.pop('_id')
    print(i,file=f)
f.close()

import pymongo


# 暂时提供上线数据，之后废除
MONGO_URL = 'localhost'
MONGO_DB = 'jia36'
# MONGO_COLLECTION = 'users_female'
MONGO_COLLECTION = 'user_male'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
f=open('out.txt','w',encoding='UTF-8-sig')
lists = list()
for i in collection.find():
    print(i)
    i.pop('_id')
    try:
        if i['id'] not in lists:
            print(i, file=f)
            lists.append(i['id'])
    except Exception as e:
        print(e)
f.close()

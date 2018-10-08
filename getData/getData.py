import pandas as pd
import pymongo as mongo

def getData():
    # MongoDB connection
    client = mongo.MongoClient('mongodb://localhost:27017/challenger')
    mongodb = client.challenger.users
    cursor=mongodb.aggregate([
        {"$unwind":"$purchases"},
        {"$project":
                {
                    "_id":0,
                    "purchaseID":"$purchases.purchaseID",
                    "purchaseTotal":"$purchases.purchaseTotal",
                    "purchaseDate":"$purchases.purchaseDate",
                    "dealID":"$purchases.dealID",
                    "categoryID":"$purchases.categoryID",
                    "category":"$purchases.category",
                    "userID":1,
                }
        }
    ])
    data=pd.DataFrame(list(cursor))
    client.close()
    return data


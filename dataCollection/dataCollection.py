import pandas as pd
import pymysql as mysql
import pymongo as mongo

# MySQL Connection
hostname = "localhost"
user = "chllg"
password = "123456"
database = "agora"
mysql_con = mysql.connect(host=hostname, user=user, passwd=password, db=database )


# MongoDB connection
client = mongo.MongoClient('mongodb://localhost:27017/challenger')
mongodb = client.challenger.users

def getData(mysql_con):
    data = pd.read_sql("SELECT p.user_id as userID, p.id as PurchaseID, p.total as totalPurchase, p.date_purchase as datePurchase, d.id as dealID,"+ 
    " c.id as categoryID, c.label as category"+
    " FROM purchases p INNER JOIN purchases_deals pd"+
    " ON pd.purchase_id=p.id"+
    " INNER JOIN deals as d"+
    " ON d.id=pd.deal_id"+
    " INNER JOIN categories c"+
    " ON c.id=d.l1_category_id"+
    " WHERE pd.purchases_deals_state_id=9 and"+
    " d.state_id=1 and d.deal_type_id in (1,2) and d.deal_multiplicity_id in (1,3) and d.date_begin  >= '2016-01-01' and"+
    " c.category_type_id=1"+
    " ORDER BY userID", con=mysql_con)
    print("read!!")
    return data

def insertToMongo(data):
    groups=data.groupby('userID')
    users=[]
    for key, item in groups:
        df=groups.get_group(key)
        user={}
        purchases=[]
        for index, row in df.iterrows():
            purchases.append({
                "purchaseID":int(row["PurchaseID"]),
                "purchaseTotal":int(row["totalPurchase"]),
                "purchaseDate":str(row["datePurchase"]),
                "dealID":int(row["dealID"]),
                "category":str(row["category"]),
                "categoryID":int(row["categoryID"])
            })
        user={
            "userID":int(key)   
        }
        user["purchases"]=purchases
        users.append(user)
    mongodb.insert_many(users)
    print("Inserted!")

def main():
    data=getData(mysql_con)
    insertToMongo(data)
    mysql_con.close()
    client.close()

main()


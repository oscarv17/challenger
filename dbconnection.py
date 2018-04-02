
# coding: utf-8

# # dbConnect

# In[ ]:


# Importing libraries


# In[1]:


import pandas as pd
import pymysql as mysql
import pymongo as mongo


# In[ ]:


# MySQL Connection


# In[8]:


hostname = "localhost"
user = "chllg"
password = "123456"
database = "agora"

mysql_con = mysql.connect( host=hostname, user=user, passwd=password, db=database )

deals = pd.read_sql("select id,title,l1_category_id from deals", con=mysql_con)
deals
mysql_con.close()


# In[ ]:


# MongoDB Connection


# In[15]:


client = mongo.MongoClient('mongodb://localhost:27017/challenger')
tests = client.challenger.test
test1 = {
    "name":"John",
    "lastname":"Doe",
    "city":"New York"
}
tests.insert_one(test1)


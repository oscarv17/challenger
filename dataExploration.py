
# coding: utf-8

# In[2]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import pandas as pd
import pymongo as mongo
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
import numpy as np
import seaborn as sbn
import datetime as dt


# In[3]:


# MongoDB connection
client = mongo.MongoClient('mongodb://localhost:27017/challenger')
mongodb = client.challenger.users


# In[10]:


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


# In[11]:


# metadata
data.info()


# In[12]:


data = data.set_index(["userID","purchaseID"])


# In[136]:


def makeGroup (df, groupField):
    grouped = df.groupby(groupField, as_index=False).size()
    grouped = pd.DataFrame(grouped).reset_index()

    grouped.columns = [groupField, 'Count']
    grouped=grouped.sort_values("Count",ascending = False)
    return grouped


# In[137]:


# Catidad de categorias
categories=makeGroup(data,"category")
plt.figure(figsize=(8,8))
ax = sbn.barplot(x="Count", y="category",data=categories);

ax.set_title("Cantidad de deals vendidos por categoria entre 2016 y 2017 \n")
ax.set_xlabel("")
ax.set_ylabel("")
plt.subplots_adjust(left=0.30)
plt.tick_params(top=False, bottom=False, left=False, right=False, labelleft=True, labelbottom=False)
for spine in plt.gca().spines.values():
    spine.set_visible(False)
for p in ax.patches:
        ax.annotate(int(p.get_width()), (p.get_width(),  p.get_y() + p.get_height()/2), va='center')


# In[138]:


# Categorias por fechas
df_date =data.sort_values("purchaseDate")

df_date_2016=df_date[(df_date["purchaseDate"]>="2016-01-01 00:00:00") & (df_date["purchaseDate"]<="2016-12-31 23:59:59")]
df_date_2017=df_date[(df_date["purchaseDate"]>="2017-01-01 00:00:00") & (df_date["purchaseDate"]<="2017-12-31 23:59:59")]


# In[139]:


# categorias 2016

categories_2016=makeGroup(df_date_2016,"category")
plt.figure(figsize=(8,8))
ax = sbn.barplot(x="Count", y="category",data=categories_2016);

ax.set_title("Cantidad de deals vendidos por categoria en el 2016 \n")
ax.set_xlabel("")
ax.set_ylabel("")
plt.subplots_adjust(left=0.30)
plt.tick_params(top=False, bottom=False, left=False, right=False, labelleft=True, labelbottom=False)
for spine in plt.gca().spines.values():
    spine.set_visible(False)
for p in ax.patches:
        ax.annotate(int(p.get_width()), (p.get_width(),  p.get_y() + p.get_height()/2), va='center')


# In[140]:


# categorias 2017

categories_2017=makeGroup(df_date_2017,"category")
plt.figure(figsize=(8,8))
ax = sbn.barplot(x="Count", y="category",data=categories_2017);

ax.set_title("Cantidad de deals vendidos por categoria en el 2017 \n")
ax.set_xlabel("")
ax.set_ylabel("")
plt.subplots_adjust(left=0.30)
plt.tick_params(top=False, bottom=False, left=False, right=False, labelleft=True, labelbottom=False)
for spine in plt.gca().spines.values():
    spine.set_visible(False)
for p in ax.patches:
        ax.annotate(int(p.get_width()), (p.get_width(),  p.get_y() + p.get_height()/2), va='center')


# In[141]:


def makeGroupSum (df, groupField, calcField):
    grouped = df.groupby(groupField, as_index=False)[calcField].sum()
   # grouped.columns = [groupField, 'Total']
    grouped=grouped.sort_values("purchaseTotal",ascending = False)
    return grouped


# In[142]:


totalC=makeGroupSum(data,"category","purchaseTotal")
plt.figure(figsize=(8,8))
ax = sbn.barplot(x="purchaseTotal", y="category",data=totalC);

ax.set_title("Total de Bs. por categoria \n")
ax.set_xlabel("")
ax.set_ylabel("")
plt.subplots_adjust(left=0.30)
plt.tick_params(top=False, bottom=False, left=False, right=False, labelleft=True, labelbottom=False)
for spine in plt.gca().spines.values():
    spine.set_visible(False)
for p in ax.patches:
        ax.annotate("{:,}".format(p.get_width()), (p.get_width(),  p.get_y() + p.get_height()/2), va='center')


# In[236]:


dfByMonth = data.copy()
dfByMonth["purchaseDate"] = pd.to_datetime(dfByMonth["purchaseDate"])
dfByMonthGroup=dfByMonth.groupby(dfByMonth["purchaseDate"].dt.strftime('%m-%Y'))["purchaseTotal"].sum().sort_values()
dfByMonthGroup = pd.DataFrame(dfByMonthGroup).reset_index()
dfByMonthGroup["purchaseDate"] = pd.to_datetime(dfByMonthGroup["purchaseDate"])
dfByMonthGroup.sort_values("purchaseDate", inplace=True)

dfByMonthGroup["purchaseDate"] = dfByMonthGroup["purchaseDate"].dt.strftime('%m-%Y')


# In[337]:


ax4 = dfByMonthGroup.plot(x="purchaseDate",y="purchaseTotal");

ax4.xaxis.set_major_locator(plt.MaxNLocator(25))
ax4.yaxis.set_major_locator(plt.MaxNLocator(20))

plt.ticklabel_format(style='plain', axis='y')

y = plt.yticks()
y=y[0]/1000000

ax4.set_xticks(np.arange(len(dfByMonthGroup["purchaseDate"])))
ax4.set_xticklabels(dfByMonthGroup["purchaseDate"], rotation="90")

ax4.set_yticklabels(y.astype(int))

plt.subplots_adjust(bottom=0.30)
plt.title("Cantidad de Bs. recaudados entre Enero 2016 a Agosto 2017 \n")
plt.legend(["Total de compras (Millones de Bs.)"])
plt.xlabel("Fecha de compra");


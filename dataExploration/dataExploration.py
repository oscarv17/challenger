get_ipython().run_line_magic('matplotlib', 'notebook')
import sys
sys.path.append('../getData')
from getData import getData
import pandas as pd
import pymongo as mongo
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MaxNLocator
import numpy as np
import seaborn as sbn
import datetime as dt

data = getData()

# metadata
data.info()

data = data.set_index(["userID","purchaseID"])
data.head()

def makeGroup (df, groupField):
    grouped = df.groupby(groupField, as_index=False).size()
    grouped = pd.DataFrame(grouped).reset_index()

    grouped.columns = [groupField, 'Count']
    grouped=grouped.sort_values("Count",ascending = False)
    return grouped

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

# Categorias por fechas
df_date =data.sort_values("purchaseDate")

df_date_2016=df_date[(df_date["purchaseDate"]>="2016-01-01 00:00:00") & (df_date["purchaseDate"]<="2016-12-31 23:59:59")]
df_date_2017=df_date[(df_date["purchaseDate"]>="2017-01-01 00:00:00") & (df_date["purchaseDate"]<="2017-12-31 23:59:59")]

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

def makeGroupSum (df, groupField, calcField):
    grouped = df.groupby(groupField, as_index=False)[calcField].sum()
   # grouped.columns = [groupField, 'Total']
    grouped=grouped.sort_values("purchaseTotal",ascending = False)
    return grouped

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

dfByMonth = data.copy()
dfByMonth["purchaseDate"] = pd.to_datetime(dfByMonth["purchaseDate"])
dfByMonthGroup=dfByMonth.groupby(dfByMonth["purchaseDate"].dt.strftime('%m-%Y'))["purchaseTotal"].sum().sort_values()
dfByMonthGroup = pd.DataFrame(dfByMonthGroup).reset_index()
dfByMonthGroup["purchaseDate"] = pd.to_datetime(dfByMonthGroup["purchaseDate"])
dfByMonthGroup.sort_values("purchaseDate", inplace=True)

dfByMonthGroup["purchaseDate"] = dfByMonthGroup["purchaseDate"].dt.strftime('%m-%Y')

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


from getData import getData
import pandas as pd
import numpy as np

data = getData()

data.info()

data = data.set_index(["userID","category"])

user_item=data.groupby(["userID","category"])["categoryID"].count().unstack(fill_value=0)
del data

user_item.head()

user_item.columns=user_item.columns.str.replace(" ","_")
user_item.columns=user_item.columns.str.replace("á","a")
user_item.columns=user_item.columns.str.replace("é","e")
user_item.columns=user_item.columns.str.replace("í","i")
user_item.columns=user_item.columns.str.replace("ó","o")
user_item.columns=user_item.columns.str.replace("ú","u")
user_item.columns=user_item.columns.str.replace("ñ","n")

user_item.columns.values

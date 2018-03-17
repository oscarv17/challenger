import pandas as pd
import pymysql as mysql

hostname = "localhost"
user = "chllg"
password = "123456"
database = "agora"

mysql_con = mysql.connect( host=hostname, user=user, passwd=password, db=database )

deals = pd.read_sql("select id,title,l1_category_id from deals", con=mysql_con)
deals

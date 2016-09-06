from textblob import TextBlob
import os
import pyodbc

from entity_functions_3 import *
from entity_functions_1 import *
from entity_functions_2 import *

dbConfig = dict (
        driver = 'FreeTDS',
        database = 'db',
        server = 'ip',
        port ='1433',
        uid = 'username',
        password = 'password'
    )
con = pyodbc.connect('DRIVER=%(driver)s;DATABASE=%(database)s;SERVER=%(server)s;PORT=%(port)s;UID=%(uid)s;PWD=%(password)s;CHARSET=UTF8;TDS_VERSION=8.0;'% dbConfig ,autocommit=False)
cur = con.cursor()

query1 = """
          Select Query
         """

query2 = """Insert Query
			"""
temp = cur.execute(query1)
all_notes = temp.fetchall()

for row in all_notes:
	print row
	nid = row[0]
	sid = row [1]
	sent = row[2]
	foldr = row[3]
	blob = TextBlob(sent)
	scores = blob.sentiment
	polarity = scores[0]
	#print polarity
	subjectivity = scores[1]
	#print subjectivity
	print "%s,%s,%s,%s,%s,%s" % (nid,sid,sent,polarity,subjectivity,foldr)
	q_s_2 = query2.format(nid = nid, sid = sid, sent = encode_text_for_sql_insertion(sent), polarity = polarity, subjectivity = subjectivity, foldr = foldr)
	
	cur.execute(q_s_2)
con.commit()
print 'Done!!!'

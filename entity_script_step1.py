import nltk
import pyodbc
import sys
import os

from geniatagger import GeniaTagger
from pymetamap import MetaMap
from entity_functions_3 import *
from entity_functions_1 import *
from entity_functions_2 import *

#load genia tagger
geni = GeniaTagger('/home/aoguntuga/myVirtualEnvs/sent2/geniatagger/geniatagger')

#connect to metamap isntance
mm = MetaMap.get_instance('/opt/public_mm_linux_main_2014/bin/metamap14')

#database configuration and connection
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
#WHERE NoteID = 51 and SourceFolder = 'DM_Good_100'
query2 = """Insert Query"""
temp = cur.execute(query1)
all_notes = temp.fetchall()

for row in all_notes:
        nid = row[0]
        sid = row[1]
        sent =row[2]
        folder = row[3]
        entities = extract_np_entity_step1(sent,geni)
        for entity in entities:
            if bool(entity):
                q_s_2 = query2.format(n1 = nid, n2 = sid, n3 = encode_entity_for_sql_insertion(entity), n4 = encode_text_for_sql_insertion(sent),  n5 = folder)
                print q_s_2
                cur.execute(q_s_2)
        con.commit()
        print "Committed: %s, %s, <%s>,<%s> " % (nid,sid,sent,entities)
print 'Done!!!'


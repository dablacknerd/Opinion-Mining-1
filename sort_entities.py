import pyodbc
import sys
import os
import xlsxwriter

from pymedtermino import *
from pymedtermino.snomedct import *

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
         SELECT SQL
         """

workbook = xlsxwriter.Workbook('list.xlsx')
worksheet = workbook.add_worksheet()

temp = cur.execute(query1)
all_notes = temp.fetchall()
items =[]
print 'Determining relevance...'
for row in all_notes:
	phrase = row[0]
	result = SNOMEDCT.search(phrase)
	if len(result) > 0:
		items.append((phrase,'RELEVANT'))
	else:
		items.append((phrase,'IRRELEVANT'))
print 'Done determining relevance...'

row = 0
col = 0

print 'Writing to the excel file...'
for item in items:
	worksheet.write(row,col, item[0])
	worksheet.write(row,col + 1, item[1])
	row += 1

workbook.close()
cur.close()
print 'Done!!!'

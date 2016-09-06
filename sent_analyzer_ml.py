from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import os
import pyodbc

def collect_scores(blob_sentences):
	if blob_sentences.sentiment[0] == 'pos':
		return ('1',blob_sentences.sentiment[0])
	elif blob_sentences.sentiment[0] == 'neg':
		return ('-1',blob_sentences.sentiment[0])
	else:
		return ('0',blob_sentences.sentiment[0])

def score(blob):
	if blob.sentiment == 'pos':
		return 1
	elif blob.sentiment == 'neg':
		return -1
	else:
		return 0

db = dict (
 driver = 'FreeTDS',
 database = 'db',
 server = 'ip',
 port ='1433',
 uid = 'username',
 password = 'password'
)
con = pyodbc.connect('DRIVER=%(driver)s;DATABASE=%(database)s;SERVER=%(server)s;PORT=%(port)s;UID=%(uid)s;PWD=%(password)s;CHARSET=UTF8;TDS_VERSION=8.0;'% db ,autocommit=False)
cur = con.cursor()
condensed_folder = raw_input("What is the name of the condensed folder: ")
original_folder = raw_input("What is the name of the original folder: ")

cwd = os.getcwd()

condensed_wd_folder = cwd + '/' + condensed_folder
original_wd_folder = cwd + '/' + original_folder

condensed_files = os.listdir(condensed_wd_folder)

for file in condensed_files:
	#file_temp_1 = file.rstrip('.xml')
	file_temp_2 = original_folder + '/' + file
	print "Processing file: %s" % file_temp_2
	q_s_1 = """ SELECT NoteID FROM Diabetes_List_A WHERE FileName like '{file_name}' """
	query1 = q_s_1.format(file_name = file_temp_2)
	#print query1
	result_temp1 = cur.execute(query1)
	result_temp2 = result_temp1.fetchone()
	if result_temp2:
		note_id = result_temp2[0]
	else:
		continue
	full_note_path = condensed_wd_folder + '/' + file
	f = open(full_note_path,'r')
	f.seek(0,os.SEEK_END)
	if f.tell() == 0:
		print 'File %s is empty, moving to next file' % file
		f.close()
		continue
	else:
		f.close()
	note_reader = open(full_note_path,'r')
	note_temp = note_reader.read()
	note_string = note_temp.decode('utf8','ignore')
	blob_scores = collect_scores(TextBlob(note_string,analyzer=NaiveBayesAnalyzer()))
	print blob_scores
	q_s_2 = """ 
	           INSERT SQL
			   """
	query2 = q_s_2.format( note_id = note_id,polarity = blob_scores[0], polarity_flag = blob_scores[1])
	cur.execute(query2)
	print "Done processing file: %s" % file_temp_2
print "Committing Scores...."
con.commit()
print "Done"

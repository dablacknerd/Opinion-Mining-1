from textblob import TextBlob
import os
import pyodbc

def collect_scores(blob_sentences):
	#array = []
	sum_polarity = 0
	sum_subjectivity = 0
	counter = 0
	for blob_senetnce in blob_sentences.sentences:
		#array.append(str(blob_senetnce),blob_senetnce.sentiment[0],blob_senetnce.sentiment[1])
		sum_polarity = sum_polarity +  blob_senetnce.sentiment[0]
		sum_subjectivity = sum_subjectivity + blob_senetnce.sentiment[1]
		counter = counter + 1
	return (sum_polarity/counter,sum_subjectivity/counter)

db = dict (
 driver = 'FreeTDS',
 database = 'tom_scratch',
 server = '129.106.31.89',
 port ='1433',
 uid = 'sa',
 password = 'T5iz3G1PcD39yAK'
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
	print query1
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
	blob_scores = collect_scores(TextBlob(note_string))
	q_s_2 = """ 
	           INSERT INTO Diabetes_List_A_Rule_Based
			   (NoteID,Subjectivity,Polarity)
			   VALUES('{note_id}','{polarity}','{subjectivity}')
			   """
	query2 = q_s_2.format( note_id = note_id,polarity = blob_scores[0],subjectivity = blob_scores[1])
	cur.execute(query2)
	print "Done processing file: %s" % file_temp_2
print "Committing Scores...."
con.commit()
print "Done"
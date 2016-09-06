from bs4 import BeautifulSoup as bs
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import os
import pyodbc

def rule_based_sentiment_analysis(text):
	utf8_friendly_text = text.decode('utf8','ignore')
	blob = TextBlob(utf8_friendly_text)
	return (blob.sentiment[0], blob.sentiment[1])

def machine_learning_sentiment_analysis(text):
	utf8_friendly_text = text.decode('utf8','ignore')
	blob = TextBlob(utf8_friendly_text,analyzer=NaiveBayesAnalyzer())
	return blob.sentiment.classification

def encode_text_for_sql_insertion(text):
	split_text = text.split(' ')
	new_text =[]
	for word in split_text:
		if word == ".eg":
			continue
		elif word.find("'") == -1:
			new_text.append(word)
		else:
			i = word.find("'")
			k = word[i:]
			new_text.append(word.rstrip(k) + "'" + k)
	return ' '.join(new_text)
#C0202054
cwd = os.getcwd()
#orig_folder = rawW
xml_folder = raw_input("What is the source xml_folder: ")
#output_folder = raw_input("What is the output folder: ")
#out_path_1 = cwd + '/' +output_folder
wd = cwd + '/' + xml_folder.lstrip(' ').rstrip(' ')

xml_file_list = os.listdir(wd) #Load list of SemRep XML Files

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
# Start Looking for HbA1C values in each file.
bowl = {}
orginal_file_name = raw_input('Enter original text file folder: ')
cui = raw_input('Enter Entity CUI: ')
aspect = raw_input('What aspect are you extracting: ')

for xml_file in xml_file_list:
	print 'Processing XML File %s' % xml_file
	key = xml_file.strip('xml')
	text_file_path = orginal_file_name + '/' + key + 'txt'
	input_file = wd + '/' + xml_file
	xml_reader = open(input_file,'r')
	xml_note = xml_reader.read()
	main_soup = bs(xml_note,'xml')
	#cui = 'C0005802'
	visit_id = 1
	query = "select NoteID from Diabetes_List_A where FileName like '{text_file_path}'"
	q_s = query.format(text_file_path = text_file_path)
	#print q_s
	cur.execute(q_s)
	temp = cur.fetchone()
	#print temp
	#print temp[0]
	if temp is None:
		continue
	else:
		note_id = temp[0]
	for sub_soup in main_soup.find_all('Utterance'):
		text = sub_soup['text']
		meat =[]
		i_vid = None
		#l_size = len(sub_soup.find_all('Entity'))
		for mini_soup in sub_soup.find_all('Entity'):
			if cui == mini_soup.get('cui'):
				#split_text = text.split(' ')
				#new_split_text =[]
				#for word in split_text:
				#hba1c = split_text[len(split_text)-1].rstrip('.eg')
				#try:
				#	float(hba1c)
				#except ValueError:
				#	continue
				#vid = visit_id
				#i_vid = vid
				#visit_id += 1
				#if l_size == k:
				#	flag = 'Y'
				#else:
				#flag = 'N'
				nid = note_id
				#text = ' '.join(split_text[1:])
				scores = rule_based_sentiment_analysis(text)
				polarity_ml = machine_learning_sentiment_analysis(text)
				it = {
				'NoteID':nid,
				'Text': encode_text_for_sql_insertion(text),
				'Aspect':aspect,
				'CUI': cui,
				'polarity_rb':str(scores[0]),
				'subjectivity':str(scores[1]),
				'polarity_ml': polarity_ml}
				meat.append(it)
		#size = len(meat)
		#k = 1
		#for ktem in meat:
			#if k == size:
				#ktem['IsLastVisit'] = 'Y'
				#continue
			#k += 1
		#size = len(meat)
		#if size == 0:
			#continue
		#else:
			#meat[size-1]["IsLastVisit"] ='Y'
		#last_item = meat[size-1]
		for item in meat:
			query1 = """
			INSERT INTO Diabetes_Entity_Aspect_List_A
			(NoteID,Text,Aspect,polarity_rb,subjectivity,polarity_ml,CUI)
			VALUES('{n1}','{n2}','{n3}','{n4}','{n5}','{n6}','{n7}')
			"""
			#print "%s | %s" % (size,item['VisitNumber'])
			#if size == item['VisitNumber']:
				#item['IsLastVisit'] = 'Y'
				#print " %s == %s " % (size,item['VisitNumber'])
			#if item == last_item:
				#q_s_1 = query1.format(n1 = item['NoteID'], n2 = item['Sentence'], n3 = item['HbA1C'], n4 = item['VisitNumber'],n5 = 'Y')
			#else:
			q_s_1 = query1.format(n1 = item['NoteID'], n2 = item['Text'], n3 = item['Aspect'], n4 = item['polarity_rb'],n5 = item['subjectivity'],n6 = item['polarity_ml'],n7 = item['CUI'])
			#print q_s_1
			#print 'Inserting for note %s' % item['NoteID']
			cur.execute(q_s_1)
			con.commit()
			print 'Committing to DB....%s' % xml_file.rstrip('.xml')

#print 'Committing to DB...'
con.commit()
cur.close()
print 'Done!!!'

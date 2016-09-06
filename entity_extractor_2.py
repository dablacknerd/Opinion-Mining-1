from bs4 import BeautifulSoup as bs
from cuis import primary_aspects
from functions import *
from cui_functions import *
from sentiment_analysis_functions import *
import os
import pyodbc



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
meat =[]
orginal_file_name = raw_input('Enter original text file folder: ')
for xml_file in xml_file_list:
	print 'Processing XML File %s' % xml_file
	key = xml_file.strip('xml')
	text_file_path = orginal_file_name + '/' + key + 'txt'
	input_file = wd + '/' + xml_file
	xml_reader = open(input_file,'r')
	xml_note = xml_reader.read()
	main_soup = bs(xml_note,'xml')
	visit_id = 1
	query = "select NoteID from Diabetes_List_A where FileName like '{text_file_path}'"
	q_s = query.format(text_file_path = text_file_path)
	#print q_s
	cur.execute(q_s)
	temp = cur.fetchone()
	#print "Temp variable: %s" % temp
	if temp is None:
		continue
	else:
		note_id = temp[0]
	#print "Processing Note %s" % note_id
	for sub_soup in main_soup.find_all('Utterance'):
		text = sub_soup['text']
		aspect = None
		i_vid = None
		#previous_cui = None
		for mini_soup in sub_soup.find_all('Entity'):
			temp_cui = mini_soup.get('cui')
			if temp_cui in primary_aspects:
				primary_cui = temp_cui
				primary_aspect = primary_aspects[primary_cui]
				if primary_aspect == "Blood Glucose":
					#aspect = return_secondary_blood_glucose_aspect(mini_soup,primary_aspect,primary_cui)
					aspect = primary_aspect
					#print '%s:%s' % (primary_aspect, aspect)
				elif primary_aspect == "Insulin Pump Device":
					#aspect = return_secondary_insulin_pump_device_secondary_aspects(mini_soup,primary_aspect,primary_cui)
					#print '%s:%s' % (primary_aspect, aspect)
					aspect = primary_aspect
				elif primary_aspect == "Biomedical Device":
					#aspect = return_secondary_insulin_pump_device_secondary_aspects(mini_soup,primary_aspect,primary_cui)
					#print '%s:%s' % (primary_aspect, aspect)
					aspect = primary_aspect
				elif primary_aspect == "Carbohydrates":
					#aspect = return_secondary_carbohydrates_secondary_aspects(mini_soup,primary_aspect,primary_cui)
					#print '%s:%s' % (primary_aspect, aspect)
					aspect = primary_aspect
				elif primary_aspect == "Insulin":
					#aspect = return_secondary_insulin_secondary_aspects(mini_soup,primary_aspect,primary_cui)
					#print '%s:%s' % (primary_aspect, aspect)
					aspect = primary_aspect
				elif primary_aspect == "Hypoglycaemia":
					aspect = primary_aspect
					#print '%s:%s' % (primary_aspect, aspect)
				elif primary_aspect == "Feet":
					aspect = primary_aspect
					#print '%s:%s' % (primary_aspect, aspect)
				elif primary_aspect == "Exercise":
					aspect = primary_aspect
					#print '%s:%s' % (primary_aspect, aspect)
				else:
					continue
				if aspect is None:
					continue
				elif aspect == 'N':
					aspect = primary_aspect
				else:
					scores = rule_based_sentiment_analysis(text)
					polarity_ml = machine_learning_sentiment_analysis(text)
					it = {
						'NoteID':note_id,
						'Text': encode_text_for_sql_insertion(text),
						'Aspect':aspect,
						'CUI':temp_cui,
						'polarity_rb':str(scores[0]),
						'subjectivity':str(scores[1]),
						'polarity_ml': polarity_ml}
					meat.append(it)
					#print "Item appended for note : %s" % note_id
			else:
				continue
		insert_into_database(meat,cur,con,key)
		meat = []

#prev_item = None
#for item in meat:
#	if item == prev_item:
#		continue
#	else:
#		prev_item = item 
#	query1 = """
#	INSERT INTO Diabetes_Entity_Aspect_List_A
#	(NoteID,Text,Aspect,polarity_rb,subjectivity,polarity_ml,CUI)
#	VALUES('{n1}','{n2}','{n3}','{n4}','{n5}','{n6}','{n7}')
#	"""
#	#print "%s | %s" % (size,item['VisitNumber'])
#	#if size == item['VisitNumber']:
#	#item['IsLastVisit'] = 'Y'
#	#print " %s == %s " % (size,item['VisitNumber'])
#	#if item == last_item:
#	#q_s_1 = query1.format(n1 = item['NoteID'], n2 = item['Sentence'], n3 = item['HbA1C'], n4 = item['VisitNumber'],n5 = 'Y')
#	#else:
#	q_s_1 = query1.format(n1 = item['NoteID'], n2 = item['Text'], n3 = item['Aspect'], n4 = item['polarity_rb'],n5 = item['subjectivity'],n6 = item['polarity_ml'],n7 = item['CUI'])
#	#print q_s_1
#	#print 'Inserting for note %s' % item['NoteID']
#	cur.execute(q_s_1)
#	con.commit()
#	print 'Committing to DB....%s' % xml_file.rstrip('.xml') 
cur.close()
print 'Done!!!'

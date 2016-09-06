from bs4 import BeautifulSoup as bs
from cuis import primary_aspects
from functions import *
from cui_functions import *
from sentiment_analysis_functions import *
import os
import pyodbc
import sys
from multiprocessing import Process, JoinableQueue

class EndOfQueue(Exception):
	pass

def main_function(files,orginal_file_name):
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
	for xml_file in files:
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
						aspect = return_secondary_blood_glucose_aspect(mini_soup,primary_aspect,primary_cui)
					elif primary_aspect == "Insulin Pump Device":
						aspect = return_secondary_insulin_pump_device_secondary_aspects(mini_soup,primary_aspect,primary_cui)
					elif primary_aspect == "Biomedical Device":
						aspect = return_secondary_insulin_pump_device_secondary_aspects(mini_soup,primary_aspect,primary_cui)
					elif primary_aspect == "Carbohydrates":
						aspect = return_secondary_carbohydrates_secondary_aspects(mini_soup,primary_aspect,primary_cui)
					elif primary_aspect == "Hypoglycaemia":
						aspect = primary_aspect
					elif primary_aspect == "Feet":
						aspect = primary_aspect
					elif primary_aspect == "Exercise":
						aspect = primary_aspect
					else:
						continue
					if aspect is None or aspect == 'N':
						continue
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

if __name__ == '__main__':
	#uidFile = open('uidFile2', 'r')
	PROC_WORKERS = 5
	xml_folder = raw_input("What is the source xml_folder: ")
	orginal_file_name = raw_input('Enter original text file folder: ')
	print "Starting workers"
	fileCue = JoinableQueue(1000000) # size of cue for main task
	procWorkers = []
	for n in range(PROC_WORKERS):
		procWorkers.append(Process(target=main_function, args=(fileCue,orginal_file_name)))
		procWorkers[-1].start()
	cwd = os.getcwd()
	#orig_folder = rawW
	#output_folder = raw_input("What is the output folder: ")
	#out_path_1 = cwd + '/' +output_folder
	wd = cwd + '/' + xml_folder.lstrip(' ').rstrip(' ')
	xml_file_list = os.listdir(wd) #Load list of SemRep XML Files
	for xml_file in xml_file_list:
		fileCue.put(xml_file)
	print "Assigning end of shift"
	for n in range(PROC_WORKERS):
		fileCue.put(EndOfQueue())
	
	print "Processing file queue"
	fileCue.join()
	print "Joined file queue"
	print "Waiting for processor workers"
	for procWorker in procWorkers:
		procWorker.join()
		print "Joined a processor worker"

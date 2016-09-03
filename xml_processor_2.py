from bs4 import BeautifulSoup as bs
import os
import pyodbc

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
 database = 'tom_scratch',
 server = '129.106.31.89',
 port ='1433',
 uid = 'sa',
 password = 'T5iz3G1PcD39yAK'
)
con = pyodbc.connect('DRIVER=%(driver)s;DATABASE=%(database)s;SERVER=%(server)s;PORT=%(port)s;UID=%(uid)s;PWD=%(password)s;CHARSET=UTF8;TDS_VERSION=8.0;'% db ,autocommit=False)
cur = con.cursor()
# Start Looking for HbA1C values in each file.
bowl = {}
orginal_file_name = raw_input('Enter original text file folder: ')
for xml_file in xml_file_list:
	key = xml_file.strip('xml')
	text_file_path = orginal_file_name + '/' + key + 'txt'
	input_file = wd + '/' + xml_file
	xml_reader = open(input_file,'r')
	xml_note = xml_reader.read()
	main_soup = bs(xml_note,'xml')
	cui = 'C0202054'
	visit_id = 1
	query = "select NoteID from Diabetes_List_A where FileName like '{text_file_path}'"
	q_s = query.format(text_file_path = text_file_path)
	#print q_s
	cur.execute(q_s)
	temp = cur.fetchone()
	print temp
	#print temp[0]
	if temp is None:
		continue
	else:
		note_id = temp[0]
	for sub_soup in main_soup.find_all('Document'):
		text = sub_soup['text']
		meat =[]
		i_vid = None
		#l_size = len(sub_soup.find_all('Entity'))
		for mini_soup in sub_soup.find_all('Entity'):
			if cui == mini_soup.get('cui'):
				split_text = text.split(' ')
				hba1c = split_text[len(split_text)-1].rstrip('.eg')
				try:
					float(hba1c)
				except ValueError:
					continue
				vid = visit_id
				i_vid = vid
				visit_id += 1
				#if l_size == k:
				#	flag = 'Y'
				#else:
				flag = 'N'
				nid = note_id
				it = {
				'NoteID':nid,
				'Sentence':' '.join(split_text[1:]),
				'HbA1C':hba1c,
				'VisitNumber':vid,
				'IsLastVisit':flag}
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
			INSERT INTO DM_Note_HbA1C_A
			(NoteID,Sentence,HbA1C,VisitNumber,IsLastVisit)
			VALUES('{n1}','{n2}','{n3}','{n4}','{n5}')
			"""
			#print "%s | %s" % (size,item['VisitNumber'])
			#if size == item['VisitNumber']:
				#item['IsLastVisit'] = 'Y'
				#print " %s == %s " % (size,item['VisitNumber'])
			#if item == last_item:
				#q_s_1 = query1.format(n1 = item['NoteID'], n2 = item['Sentence'], n3 = item['HbA1C'], n4 = item['VisitNumber'],n5 = 'Y')
			#else:
			q_s_1 = query1.format(n1 = item['NoteID'], n2 = item['Sentence'], n3 = item['HbA1C'], n4 = item['VisitNumber'],n5 = item['IsLastVisit'])
			print q_s_1
			#print 'Inserting for note %s' % item['NoteID']
			cur.execute(q_s_1)
con.commit()

q_s_2 = """
		SELECT NoteID,MAX(VisitNumber) FROM DM_Note_HbA1C_A
		GROUP BY NoteID
		"""

temp2 = cur.execute(q_s_2)
mcdreamy = temp2.fetchall()
for dream in mcdreamy:
	query2 = """
			UPDATE DM_Note_HbA1C_A
			SET IsLastVisit ='Y'
			WHERE NoteID = {note_id} AND
				VisitNumber = {visit_number}
			"""
	q_s_3 = query2.format(note_id = dream[0],visit_number = dream[1])
	cur.execute(q_s_3)
	con.commit()
cur.close()
print 'Done!!!'
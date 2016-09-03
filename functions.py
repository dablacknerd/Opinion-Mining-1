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

def insert_into_database(meat,cur,con,key):
	prev_item = None
	for item in meat:
		if item == prev_item:
			continue
		else:
			prev_item = item 
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
		print 'Committing to DB....%s' % key 
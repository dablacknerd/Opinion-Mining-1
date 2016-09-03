import nltk
#from entity_functions_2 import issymbol
name_dict ={}
dr_dict = {'1':'a','2':'b','3':'c','4':'d',
		   '5':'e','6':'f','7':'g','8':'h',
		   '9':'i','10':'j','11':'k','12':'l',
		   '13':'m','14':'n','15':'o','16':'p',
		   '17':'q','18':'r','19':'s','20':'t',
		   '21':'u','22':'v','23':'w','24':'x',
		   '25':'y','26':'z'}

def issymbol(string):
	if string == '%' or string == '(' or string ==')' or string =='/' or string =='\\' or string == '<' or string =='>' or string =='~':
		return True
	else:
		return False

def left_right_strip_symbols(string):
	#new_string =''
	size = len(string)
	if size == 0:
		r_size = size
	else:
		r_size = size - 1
	#print 'Working on string: %s %s %s' % (string,size,r_size)
	if string[0] == '%' or string[0] == '(' or string[0] ==')' or string[0] =='/' or string[0] =='\\' or string[0] == '<' or string[0] =='>' or string[0] =='~':
		string = string.lstrip(string[0])
		r_size = len(string) - 1
	if string[r_size] == '%' or string[r_size] == '(' or string[r_size] ==')' or string[r_size] =='/' or string[r_size] =='\\' or string[r_size] == '<' or string[r_size] =='>' or string[r_size] =='~':
		string = string.rstrip(string[r_size])
	return string.lstrip().rstrip()

def return_doctor_entry_sentences(content):
	sentence_list =[]
	for c in content:
		if len(c.rstrip('\n')) > 2:
			tokens = nltk.word_tokenize(c)
			if tokens[len(tokens) - 1] == '.':
				sentence_list.append(c)
			else:
				continue
		else:
			continue
	return ' '.join(sentence_list)

def entity_chunker_v1(document,d_id):
	entity_chunk_list =[]
	sentences = nltk.sent_tokenize(document)
	np_grammar = """NP: {<DT>?<JJ.*>*<NN.*>*}
	                  {<NNP>+}
					  {<NNPS>}"""
	np_chunker = nltk.RegexpParser(np_grammar)
	sent_id = 1
	for sentence in sentences:
		if len(sentence) > 2:
			word_tokens = nltk.word_tokenize(scramble_patient_and_dr_name(sentence))
			sentence_pos = nltk.pos_tag(word_tokens)
			sentence_chunk = np_chunker.parse(sentence_pos)
			entity_chunk_list.append((d_id,
									  sent_id,
									  scramble_patient_and_dr_name(sentence),
									  None
									  ))
			sent_id = sent_id + 1
		else:
			continue
	name_dict ={}
	return entity_chunk_list

def entity_chunker_v2(sentence):
	#entity_chunk_list =[]
	np_grammar = "NP: {<DT>?<JJ.*>*<NN.*>*}"
	np_chunker = nltk.RegexpParser(np_grammar)
	word_tokens = nltk.word_tokenize(sentence)
	sentence_pos = nltk.pos_tag(word_tokens)
	sentence_chunk = np_chunker.parse(sentence_pos)
	return retrieve_entities(sentence_chunk)

def entity_chunker_v3(sentence):
	#entity_chunk_list =[]
	np_grammar = "NP: {<DT>?<JJ.*>*<NN.*>*}"
	np_chunker = nltk.RegexpParser(np_grammar)
	word_tokens = nltk.word_tokenize(sentence)
	sentence_pos = nltk.pos_tag(word_tokens)
	sentence_chunk = np_chunker.parse(sentence_pos)
	return retrieve_entities_v3(sentence_chunk)

def retrieve_entities(chunk):
	e_list = []
	for c in chunk:
		if isinstance(c,list):
			k = [ i[0] for i in c if i[1] =='NN' or i[1] == 'NNP' or i[1] == 'NNS' or i[1] == 'NNPS']
			e_list.append(' '.join(k))
		else:
			continue
	return e_list

def retrieve_entities_v2(chunk):
	e_list = []
	for c in chunk:
		if isinstance(c,list):
			k = [ i[0] for i in c]
			e_list.append(' '.join(k))
		else:
			continue
	return e_list

def retrieve_entities_v3(chunk):
	e_list = []
	for c in chunk:
		if isinstance(c,list):
			k0 = [ i[0] for i in c]
			k3 = [ i[1] for i in c]
			k1 = [ i[0] for i in c if i[1] =='NN' or i[1] == 'NNP' or i[1] == 'NNS' or i[1] == 'NNPS']
			k2 = [ i[1] for i in c if i[1] =='NN' or i[1] == 'NNP' or i[1] == 'NNS' or i[1] == 'NNPS']
			#if len(k2) == 1:
				#if k2[0] == 'DT' or k2
			if ' '.join(k1).isspace() or ' '.join(k1) == '' or issymbol(' '.join(k1)) or ' '.join(k1).lower() == 'pm cst' or ' '.join(k1).lower() == 'am cst' or ' '.join(k1).lower() == 'PM CST' or ' '.join(k1).lower() == 'AM CST':
				string = ' '.join(k0)
				pos = ' '.join(k3)
				#print 'Skipping: %s, POS: %s' % (k0,k3)
				continue
			
			tupe = (left_right_strip_symbols(' '.join(k1)),' '.join(k2))
			e_list.append(tupe)
		else:
			continue
	return e_list

def retrieve_entities_v4(chunk):
	e_list = []
	type_dict 
	key_words = ['blood sugar','blood suagar','blood glucose','blood pressure','hba1c','hb a1c','hbaic','hb aic','hemoglobin','insulin','weight']
	for c in chunk:
		if isinstance(c,list):
			k1_0 = [ i[0] for i in c]
			k2_0 = [ i[1] for i in c]
			k
			tupe = (' '.join(k1),' '.join(k2))
			e_list.append(tupe)
		else:
			continue
	return e_list

def retrieve_entities_with_tags(chunk):
	e_list = [] 
	for c in chunk:
		if isinstance(c,list):
			k = [(i[0],i[1]) for i in c if i[1] =='NN' or i[1] == 'NNP' or i[1] == 'NNS' or i[1] == 'NNPS'] 
			#print k
			e_list.append(k)
		else:
			continue
	return e_list

def insert_into_sentence_table(note_id,sentence_id,sentence,disease,path):
	query = """INSERT INTO Sentences
			(NoteID,SentenceID,Sentence,NoteType,SourceFolder)
			VALUES('{n1}','{n2}','{n3}','{n4}','{5}')
			"""
	print note_id
	print sentence_id
	print sentence
	print disease
	print path
	q_s = query.format(n1 = note_id, n2= sentence_id, n3 = sentence, n4 = disease, n5= path)
	return q_s

def scramble_patient_and_dr_name(sentence):
	sent = sentence
	sent_bi = nltk.bigrams(nltk.word_tokenize(sentence))
	dr_count = 1
	for bi in sent_bi:
		if bi[0] =='Mr.' or bi[0] == 'mr.' or bi[0] =='Mister' or bi[0] == 'mister':
			key = bi[0] + ' ' + bi[1]
			if key in name_dict:
				#replacement = patient_dict[key]
				continue
			else:
				name_dict[key] = 'the patient'
				#replacement = 'patient'
		elif bi[0] =='Mrs.' or bi[0] == 'mrs.' or bi[0] =='Misses' or bi[0] == 'misses' or bi[0] =='Ms.' or bi[0] == 'ms.':
			key = bi[0] + ' ' + bi[1]
			if key in name_dict:
				#replacement = patient_dict[key]
				continue
			else:
				name_dict[key] = 'the patient'
				#replacement = 'patient'
		elif bi[0] =='Dr.' or bi[0] == 'dr.' or bi[0] =='Doctor':
			key = bi[0] + ' ' + bi[1]
			if key in name_dict:
				#replacement = patient_dict[key]
				continue
			else:
				name_dict[key] = 'Dr. ' + dr_dict[str(dr_count)].upper() + bi[1][0]
				dr_count = dr_count + 1
		else:
			continue
				#replacement = 'patient'
	for key in (name_dict.keys()):
		sent = sent.replace(key,name_dict[key])
	#print sent
	return sent
def extract_pos_metamap(concept_trigger):
	lis = concept_trigger.lstrip('[').rstrip(']')
	lst = lis.split('-')
	return lst[4]
def concept_and_semtype(concept_list):
	concepts = []
	for concept in concept_list:
		pos = extract_pos_metamap(concept.trigger)
		if pos == 'noun':
			con_tupe ={}
			if concept.preferred_name == 'Blood group antibody' or concept.preferred_name == 'Logarithm':
				continue
			con_tupe['preferred_name'] = concept.preferred_name
			sem_list =[]
			semtype_dict = {
			"aapp":"Amino Acid, Peptide, or Protein","acab":"Acquired Abnormality","acty":"Activity",
			"aggp":"Age Group","amas":"Amino Acid Sequence","amph":"Amphibian","anab":"Anatomical Abnormality",
			"anim":"Animal","anst":"Anatomical Structure","antb":"Antibiotic","arch":"Archaeon","bacs":"Biologically Active Substance",
			"bact":"Bacterium","bdsu":"Body Substance","bdsy":"Body System","bhvr":"Behavior","biof":"Biologic Function",
			"bird":"Bird","blor":"Body Location or Region","bmod":"Biomedical Occupation or Discipline","bodm":"Biomedical or Dental Material",
			"bpoc":"Body Part, Organ, or Organ Component","bsoj":"Body Space or Junction","carb":"Carbohydrate","celc":"Cell Component",
			"celf":"Cell Function","cell":"Cell","cgab":"Congenital Abnormality","chem":"Chemical","chvf":"Chemical Viewed Functionally",
			"chvs":"Chemical Viewed Structurally","clas":"Classification","clna":"Clinical Attribute","clnd":"Clinical Drug",
			"cnce":"Conceptual Entity","comd":"Cell or Molecular Dysfunction","crbs":"Carbohydrate Sequence","diap":"Diagnostic Procedure",
			"dora":"Daily or Recreational Activity","drdd":"Drug Delivery Device","dsyn":"Disease or Syndrome","edac":"Educational Activity",
			"eehu":"Environmental Effect of Humans","eico":"Eicosanoid","elii":"Element, Ion, or Isotope","emod":"Experimental Model of Disease",
			"emst":"Embryonic Structure","enty":"Entity","enzy":"Enzyme","euka":"Eukaryote","evnt":"Event","famg":"Family Group",
			"ffas":"Fully Formed Anatomical Structure","fish":"Fish","fndg":"Finding","fngs":"Fungus","food":"Food","ftcn":"Functional Concept",
			"genf":"Genetic Function","geoa":"Geographic Area","gngm":"Gene or Genome","gora":"Governmental or Regulatory Activity",
			"grpa":"Group Attribute","grup":"Group","hcpp":"Human-caused Phenomenon or Process","hcro":"Health Care Related Organization",
			"hlca":"Health Care Activity","hops":"Hazardous or Poisonous Substance","horm":"Hormone","humn":"Human","idcn":"Idea or Concept",
			"imft":"Immunologic Factor","inbe":"Individual Behavior","inch":"Inorganic Chemical","inpo":"Injury or Poisoning","inpr":"Intellectual Product",
			"irda":"Indicator, Reagent, or Diagnostic Aid","lang":"Language","lbpr":"Laboratory Procedure","lbtr":"Laboratory or Test Result",
			"lipd":"Lipid","mamm":"Mammal","mbrt":"Molecular Biology Research Technique","mcha":"Machine Activity","medd":"Medical Device",
			"menp":"Mental Process","mnob":"Manufactured Object","mobd":"Mental or Behavioral Dysfunction","moft":"Molecular Function",
			"mosq":"Molecular Sequence","neop":"Neoplastic Process","nnon":"Nucleic Acid, Nucleoside, or Nucleotide","npop":"Natural Phenomenon or Process",
			"nsba":"Neuroreactive Substance or Biogenic Amine","nusq":"Nucleotide Sequence","ocac":"Occupational Activity","ocdi":"Occupation or Discipline",
			"opco":"Organophosphorus Compound","orch":"Organic Chemical","orga":"Organism Attribute","orgf":"Organism Function","orgm":"Organism",
			"orgt":"Organization","ortf":"Organ or Tissue Function","patf":"Pathologic Function","phob":"Physical Object","phpr":"Phenomenon or Process",
			"phsf":"Physiologic Function","phsu":"Pharmacologic Substance","plnt":"Plant","podg":"Patient or Disabled Group","popg":"Population Group",
			"prog":"Professional or Occupational Group","pros":"Professional Society","qlco":"Qualitative Concept","qnco":"Quantitative Concept",
			"rcpt":"Receptor","rept":"Reptile","resa":"Research Activity","resd":"Research Device","rnlw":"Regulation or Law","sbst":"Substance",
			"shro":"Self-help or Relief Organization","socb":"Social Behavior","sosy":"Sign or Symptom","spco":"Spatial Concept","strd":"Steroid",
			"tisu":"Tissue","tmco":"Temporal Concept","topp":"Therapeutic or Preventive Procedure","virs":"Virus","vita":"Vitamin","vtbt":"Vertebrate"}
			semtype_list = concept.semtypes.lstrip('[').rstrip(']').split(',')
			#con_tupe['semantic_type'] = semtype_dict[concept.semtypes.lstrip('[').rstrip(']')]
			if len(semtype_list) == 1:
				con_tupe['semantic_type'] = semtype_dict[semtype_list[0]]
			else:
				for sem in semtype_list:
					sem_list.append(semtype_dict[sem])
				con_tupe['semantic_type'] = ' '.join(sem_list)
			con_tupe['cui'] = concept.cui
			concepts.append(con_tupe)
		else:
			continue
	return concepts
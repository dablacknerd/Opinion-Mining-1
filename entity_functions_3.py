
def extract_np_entity_step1(sentence,geni):
	parse_result = geni.parse(sentence)
	entity_list =[]
	entity = []
	pos =[]
	#start_flag = False # set to true if the beginning of an IOB structure has been encountered
	for p in parse_result:
		chunk_type_position = p[3]
		chunk_type = p[3][2:]
		#print p
		if chunk_type_position == 'B-NP' and len(entity) == 0:
			#if p[2][0:2] == 'NN': 
			entity.append(p[0])
			pos.append(p[2])
			#start_flag = True
		elif chunk_type_position == 'B-NP' and len(entity) > 0:
			#if p[2][0:2] == 'NN': 
			entity_list.append(((' '.join(entity)),(' '.join(pos))))
			entity = []
			pos =[]
			entity.append(p[0])
			pos.append(p[2])
			#start_flag = True
		elif chunk_type_position == 'I-NP' :
			#if p[2][0:2] == 'NN':
			entity.append(p[0])
			pos.append(p[2])
		else:
			#entity_list.append(' '.join(entity))
			#entity = []
			continue
	if len(entity) > 0: 
		entity_list.append(((' '.join(entity)),(' '.join(pos))))
		entity = []
		pos =[]
	return extract_np_entity_step2(entity_list)
	#return entity_list

def extract_np_entity_step2_v2(entity_list):
	entities =[]
	for item in entity_list:
		ent =[]
		words = item[0].split()
		pos = item[1].split()
		s1 = len(words)
		k = 0
		for w in words:
			if pos[k][0:2] == 'NN':
				ent.append(w)
				k += 1
			else:
				k +=1
				continue
		entities.append(' '.join(ent).rstrip().lstrip())
	return entities

def extract_np_entity_step2(entity_list):
	entities =[]
	for item in entity_list:
		#ent = []
		pos = item[1].split()
		s1 = len(pos) - 1
		if pos[s1][0:2] == 'NN':
			entities.append(item[0])
		else:
			continue
	return entities
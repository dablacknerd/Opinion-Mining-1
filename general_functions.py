def polarity_score(syn_set_list):
	limp =[]
	for s in syn_set_list:
		word = s.name().split('.')[0]
		pos_score = swn.senti_synset(s.name()).pos_score()
		neg_score = swn.senti_synset(s.name()).neg_score()
		polarity_score = float(pos_score) - float(neg_score)
		limp.append(polarity_score)
	arr = np.array(limp)
	return arr.mean()

def return_synset_list_1(sentence):
	return_list_1 = []
	return_list_2 = []
	sent = nltk.word_tokenize(sentence)
	sent_pos = nltk.pos_tag(sent)
	for s_pos in sent_pos:
		if s_pos[1][:2] == 'NN':
			return_list_1.append((s_pos[0],'n'))
		elif s_pos[1][:2] == 'VB' :
			return_list_1.append((s_pos[0],'v'))
		elif s_pos[1][:2] == 'RB' :
			return_list_1.append((s_pos[0],'r'))
		elif s_pos[1][:2] == 'JJ' :
			return_list_1.append((s_pos[0],'a'))
		else:
			continue
	if len(return_list_1) == 0:
		return 0
	else:
		for item in return_list_1:
			return_list_2.append(lesk(sentence,item[0],item[1])
		return return_list_2

def return_synset_list_2(sentence):
	return_list_1 = []
	return_list_2 = []
	sent = nltk.word_tokenize(sentence)
	sent_pos = nltk.pos_tag(sent)
	for s_pos in sent_pos:
		if s_pos[1][:2] == 'NN':
			return_list_1.append((s_pos[0],'n'))
		elif s_pos[1][:2] == 'VB' :
			return_list_1.append((s_pos[0],'v'))
		elif s_pos[1][:2] == 'RB' :
			return_list_1.append((s_pos[0],'r'))
		elif s_pos[1][:2] == 'JJ' :
			return_list_1.append((s_pos[0],'a'))
		else:
			continue
	if len(return_list_1) == 0:
		return 0
	else:
		for item in return_list_1:
			return_list_2.append(simple_lesk(sentence,item[0],pos=item[1])
		return return_list_2


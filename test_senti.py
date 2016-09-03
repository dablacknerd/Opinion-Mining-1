from nltk.corpus import sentiwordnet as swn
from nltk.wsd import lesk
from pywsd.lesk import simple_lesk
from geniatagger import GeniaTagger
import pandas as pd
import nltk
from general_functions import *

geni = GeniaTagger('/home/aoguntuga/myVirtualEnvs/sent2/geniatagger/geniatagger')

xl_file = pd.ExcelFile("/home/aoguntuga/myVirtualEnvs/sent2/Test/Test Cases.xlsx")

sent_df = xl_file.parse('Sheet1')

sentences = list(sent_df['Sentence'].values)

polarity_list_1 = []
polarity_list_2 = []

for s in sentences:
	syn1 = return_synset_list_1(sentence)
	syn2 = return_synset_list_2(sentence)
	p1 = polarity_score(syn1)
	p2 = polarity_score(syn2)
	polarity_list_1.append(p1)
	polarity_list_2.append(p2)

sent_df['lesk_wsd_polarity'] = polarity_list_1
sent_df['siplelesk_wsd_polarity'] = polarity_list_2

sent_df.to_excel("/home/aoguntuga/myVirtualEnvs/sent2/Test/test_case_result.xlsx")
print 'Done!!!'

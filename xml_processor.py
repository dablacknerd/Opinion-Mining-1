from bs4 import BeautifulSoup as bs
import os

########Load DM CUI List ########
r1 = open('diabetes_cuis.txt','r')
cui_list =[]
content = r1.read()
cui_list = content.split('\n')

###########Get ready to read xml files#######
cwd = os.getcwd()
xml_folder = raw_input("What is the source xml_folder: ")
output_folder = raw_input("What is the output folder: ")
out_path_1 = cwd + '/' +output_folder
wd = cwd + '/' + xml_folder.lstrip(' ').rstrip(' ')
xml_file_list = os.listdir(wd)

for xml_file in xml_file_list:
	input_file = wd + '/' + xml_file
	xml_reader = open(input_file,'r')
	xml_note = xml_reader.read()
	main_soup = bs(xml_note,'xml')
	output_file = out_path_1 + '/' + xml_file.strip('xml') + 'txt'
	writeout = open(output_file,'w')
	for sub_soup in main_soup.find_all('Document'):
		text = sub_soup['text']
		sub_cui_list =[]
		for mini_soup in sub_soup.find_all('Entity'):
			sub_cui_list.append(mini_soup.get('cui'))
		flag = False
		for cui in sub_cui_list:
			if cui in cui_list:
				flag = True
		if flag is True:
			text = text + '\n'
			writeout.write(text)
	writeout.close()
	xml_reader.close()
	print "%s....closed \n" % xml_file
	print "%s....closed \n" % xml_file.strip('xml') + 'txt'
	print "Moving on to next file....\n"
	print "......\n"

print "Done with all the processing for %s" % xml_folder
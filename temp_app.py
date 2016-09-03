import os
import pyodbc

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

sqlStatement = """
               select a.NoteID,FileName
               from Diabetes_List_A as a where a.Lab_HbA1C <> '0' and a.[FileName] is not NULL
               """

cur.execute(sqlStatement)
file_dict ={}
file_list_xml =[]
for row in cur.fetchall():
    #file_list[row[0]] = row[1]
    #print "Here: %s" % row
    file_txt = row[1].split('/')[1]
    file_dict[file_txt[:-4]] = row[0]
    file_xml = file_txt[:-4] + '.xml'
    file_list_xml.append(file_xml)

cwd = os.getcwd()
path_folder = cwd + '/Diabetes_List_A_Done'

file_list_xml_2 = os.listdir(path_folder)

fulloutput_path = cwd + '/text_to_xml_mapper.txt'
writer = open(fulloutput_path,'wb')

sqlStatement2 = """ INSERT INTO Text_To_XML_Mapper (NoteID,TextFileName,XMLFileName) VALUES (???)"""
sqlTableInsert = """ INSERT INTO Text_To_XML_Mapper (NoteID,TextFileName,XMLFILEName) values (?,?,?) """ 
for filr in file_list_xml:
    if filr in file_list_xml_2:
        xml_file = '/Diabetes_List_A_Done/' + filr
        text_file = '/Diabetes_List_A_Folder/' + filr[:-4] + '.txt'
        note_id = file_dict[filr[:-4]]
        line = "%s,%s,%s \n" % (note_id,text_file,xml_file)
        #cur.execute(sqlStatement2,line)
    else:
        xml_file = 'None'
        text_file = '/Diabetes_List_A_Folder/' + filr[:-4] + '.txt'
        note_id = file_dict[filr[:-4]]
        line =  "%s,%s,%s \n" % (note_id,text_file,xml_file)
    
    print "Writing: %s" % line
    writer.write(line)
    #cur.execute(sqlTableInsert, line)
    #print "%s committed" % filr

print 'Done!!!'
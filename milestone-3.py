from deep_translator import GoogleTranslator
import os

translator = GoogleTranslator(source='en', target='german')
trs_text = translator.translate('Hello World')

file = open('captions\Bill Gates.txt')

trs_dir_name = 'translations'
current_dir = os.getcwd()
trs_dir_path = os.path.join(current_dir, trs_dir_name)

if(not(os.path.exists(trs_dir_path))):
    os.makedirs(trs_dir_path)

for file in os.listdir('captions'): #iterates through each caption file
    opened_file = open('captions\\'+file, 'r', encoding="utf8") #opening captions
    new_file = open("TRS "+file, 'w', encoding="utf8") #creating a file for translated captions

    for i in opened_file.readlines(): #reading all files in the 'captions' directory
        translated_line = translator.translate(i)
        new_file.write(translated_line+'\n')

    print(str(file)+' has been translated')
    opened_file.close() 
    new_file.close()

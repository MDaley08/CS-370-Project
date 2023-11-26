from deep_translator import MyMemoryTranslator

import os

def translate_text(input_file:str, output_path:str, lang: str):

    translator = MyMemoryTranslator(source= 'english', target=lang)

    try: #try to open our caption file
        in_file = open(input_file, 'r', encoding="utf8") #opening file to read
    except FileNotFoundError:
        print("%s file was not found " % input_file)

    try: #try to create a new file to store translation
        out_file_name = (input_file.split('/')[-1]).split('.')[0] + ' translation.txt' # we do a split incase file is abs path then take old name
        out_file_path = os.path.join(output_path, out_file_name)
        out_file = open(out_file_path, 'w', encoding='utf8')
    except FileNotFoundError:
        print("%s this dir can't be accessed " % output_path)
        
    for i in in_file.readlines(): #reading all files in the 'captions' directory
        translated_line = translator.translate(i)
        out_file.write(translated_line+'\n')

    print('%s has be sucessfully translated' % input_file)
    in_file.close()
    out_file.close()

def main():

    trs_dir_name = 'translations'
    text_dir_name = 'whisper_transcripts'
    current_dir = os.getcwd()
    trs_dir_path = os.path.join(current_dir, trs_dir_name)
    text_dir_path = os.path.join(current_dir, text_dir_name)


    if(not(os.path.exists(trs_dir_path))):
        os.makedirs(trs_dir_path)

    for file in os.listdir(text_dir_path): #iterates through each caption file
        file_path = os.path.join(text_dir_path,file)
        translate_text(file_path,trs_dir_path,'german')


main()
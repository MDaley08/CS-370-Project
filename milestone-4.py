import os
from gtts import gTTS
import gtts.lang


def text_to_speech(input_file:str, output_path:str):
    try:
        in_file = open(input_file,'r',encoding="utf8")

    except FileNotFoundError:
        print("%s file was not found \n" % input_file)
    
    out_file_name = (input_file.split('/')[-1]).split('.')[0] + '.mp3'
    out_file_path = os.path.join(output_path, out_file_name)

    in_text = ""
    language = 'de'

    for i in in_file.readlines():
        in_text += i

    output = gTTS(text= in_text, lang= language)
    output.save(out_file_path)

def main():

    trs_dir_name = 'translations'
    tts_dir_name = 'tts_audio'

    current_dir = os.getcwd()
    trs_dir_path = os.path.abspath(trs_dir_name)
    tts_dir_path = os.path.join(current_dir, tts_dir_name)

    if(not(os.path.exists(tts_dir_path))):
        os.makedirs(tts_dir_path)

    for file in os.listdir(trs_dir_path): #iterates through each translation file
        file_path = os.path.join(trs_dir_path, file)
        text_to_speech(file_path,tts_dir_path)


main()

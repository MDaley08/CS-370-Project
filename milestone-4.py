import os
from gtts import gTTS


def text_to_speech(input_file:str, output_path:str):
    pass

def main():

    trs_dir_name = 'translations'
    tts_dir_name = 'tts_audio'

    current_dir = os.getcwd()
    trs_dir_path = os.path.abspath(trs_dir_name)
    tts_dir_path = os.path.join(current_dir, tts_dir_name)


    # if(not(os.path.exists(trs_dir_path))):
    #     os.makedirs(trs_dir_path)

    # for file in os.listdir(text_dir_path): #iterates through each caption file
    #     file_path = os.path.join(text_dir_path,file)
    #     translate_text(file_path,trs_dir_path,'german')


main()
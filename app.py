import whisper
import os
import ffmpeg
import textwrap 
from flask import Flask
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter
from deep_translator import GoogleTranslator

def get_captions(url:str):

    formatter = SRTFormatter()

    try:
        yt = YouTube(url)
        vid_id = url.split("v=")[1]
        caption = YouTubeTranscriptApi.get_transcript(vid_id)
        return caption
        srt_formatted = formatter.format_transcript(caption)
        file_name = yt.title + '.srt'
        file_path = os.path.join(download_path, file_name)
        with open(file_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_formatted)
    except KeyError:
        return 400, "Error: video not avaliable or cannot be download"
    except ValueError:
        return 400, "Error: invalide URL"
    except Exception as e:
        400, "Error extracting transcript from: " + str(e)

def translate_text(input_file:str, output_path:str, lang: str):

    translator = GoogleTranslator(source= 'english', target=lang)

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

    print('%s has be sucessfully translate' % input_file)
    in_file.close()
    out_file.close()


### FRONT END ###
import streamlit as st
from transformers import pipeline

text = st.text_area('Enter a video url!')
submit = st.button('Generate')  
if submit:
    captions = get_captions(text)
    
    for i in range(len(captions)): #prints captions
        st.write(captions[i]["text"])
    
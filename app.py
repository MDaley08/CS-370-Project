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

def translate_line(input_str: str, lang: str):

    translator = GoogleTranslator(source= 'english', target=lang)
    translated_line = translator.translate(input_str)

    return translated_line

### FRONT END ###
import streamlit as st
import streamlit_scrollable_textbox as stx
from transformers import pipeline

text = st.text_area('Enter a YouTube video url! (shorts not allowed)')
submit = st.button('Generate')  
if submit:
    captions = get_captions(text)
    
    col1, col2, col3 = st.columns(3)
    col1.header("Original")
    col2.header("Translated")
    col3.header("Timestamp")

    caption_string = ""
    translated_string = ""

    bar = st.progress(0, text='Translating text...')
    for i in range(len(captions)): #prints captions
        caption_line = captions[i]["text"]
        translated_line = translate_line(captions[i]["text"], 'de')

        caption_string += caption_line
        translated_string += translated_line

        percent = i / len(captions)
        bar.progress(percent, text='Translating text... '+str(i)+' out of '+str(len(captions))+ " lines")

        col1.write(captions[i]["text"], use_column_width=True) #original
        col2.write(translated_line, use_column_width=True) #translated
        col3.write(captions[i]["start"], use_column_width=True) #timestamps

    bar.progress(100, text='Done! '+str(len(captions))+' out of '+str(len(captions))+ " lines")

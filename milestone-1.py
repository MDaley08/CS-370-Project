from flask import Flask, request, jsonify
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

import os

"""
API Commands
GET -> Request data from a specified resource
POST -> Create a resource
PUT -> Update a resource
DELETE -> Delete a resource
"""
app = Flask(__name__)

@app.route("/")
def download_videos():
    vid_dir_name = 'videos'
    current_dir = os.getcwd()
    vid_dir_path = os.path.join(current_dir, vid_dir_name)

    if(not(os.path.exists(vid_dir_path))):
        os.makedirs(vid_dir_path)

    youtube_links = ['https://www.youtube.com/watch?v=bNKdlnoAqIs',
                     'https://www.youtube.com/watch?v=RldpC8a9Zv4',
                     'https://www.youtube.com/watch?v=aDzm9_vthFo',
                     'https://www.youtube.com/watch?v=6in8fx1Tc38',
                     'https://www.youtube.com/watch?v=n9adLsXTpZQ',
                     'https://www.youtube.com/watch?v=_Lx5VmAdZSI',
                     'https://www.youtube.com/watch?v=EIVTf-C6oQo',
                     'https://www.youtube.com/watch?v=FwEKCP7DVFc',
                     'https://www.youtube.com/watch?v=FTWOBNTWLb4',
                     'https://www.youtube.com/watch?v=Du-RQu4soIs'
                     ]

    for i in range(len(youtube_links)):
        current_link = youtube_links[i]
        vid_id = current_link.split("v=")[1]
        vid_src = YouTube(current_link)

        video = vid_src.streams[1].download(output_path=vid_dir_path)
        
    return 'Complete',200

if __name__ == "__main__":
    app.run(debug=True)
    download_videos()
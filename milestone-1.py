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
    cap_dir_name = 'captions'
    current_dir = os.getcwd()
    vid_dir_path = os.path.join(current_dir, vid_dir_name)
    cap_dir_path = os.path.join(current_dir, cap_dir_name)

    if(not(os.path.exists(vid_dir_path))):
        os.makedirs(vid_dir_path)
    if(not(os.path.exists(cap_dir_path))):
        os.makedirs(cap_dir_path)
    

    youtube_links = ['https://www.youtube.com/watch?v=bNKdlnoAqIs&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=27',
                     'https://www.youtube.com/watch?v=RldpC8a9Zv4&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=31',
                     'https://www.youtube.com/watch?v=aDzm9_vthFo&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=32',
                     'https://www.youtube.com/watch?v=6in8fx1Tc38&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=37',
                     'https://www.youtube.com/watch?v=n9adLsXTpZQ&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=63',
                     'https://www.youtube.com/watch?v=_Lx5VmAdZSI&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=54',
                     'https://www.youtube.com/watch?v=EIVTf-C6oQo&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=58',
                     'https://www.youtube.com/watch?v=FwEKCP7DVFc&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=56',
                     'https://www.youtube.com/watch?v=cU3rmlDgfbg&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=60',
                     'https://www.youtube.com/watch?v=Du-RQu4soIs&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=61'
                     ]
    formatter = SRTFormatter()

    for i in range(len(youtube_links)):
        current_link = youtube_links[i]
        vid_id = current_link.split("v=")[1]
        vid_src = YouTube(current_link)

        video = vid_src.streams[1].download(output_path=vid_dir_path)
        transcript = YouTubeTranscriptApi.get_transcript(vid_id)
        srt_formatted = formatter.format_transcript(transcript)

        file_name = vid_src.title + '.srt'
        file_path = os.path.join(cap_dir_name, file_name)
        with open(file_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_formatted)
        
    return 'Complete',200

if __name__ == "__main__":
    app.run(debug=True)
    download_videos()
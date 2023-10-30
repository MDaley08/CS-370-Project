from flask import Flask, request, jsonify
from pytube import YouTube, Caption
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
    dir_name = 'videos'
    current_dir = os.getcwd()
    dir_path = os.path.join(current_dir, dir_name)

    if(not(os.path.exists(dir_path))):
        os.makedirs(dir_path)
    
    youtube_links = ['https://www.youtube.com/watch?v=bNKdlnoAqIs&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=27',
                     'https://www.youtube.com/watch?v=RldpC8a9Zv4&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=31',
                     'https://www.youtube.com/watch?v=aDzm9_vthFo&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=32',
                     'https://www.youtube.com/watch?v=6in8fx1Tc38&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=37',
                     'https://www.youtube.com/watch?v=u1UC89H4Swc&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=51',
                     'https://www.youtube.com/watch?v=_Lx5VmAdZSI&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=54',
                     'https://www.youtube.com/watch?v=EIVTf-C6oQo&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=58',
                     'https://www.youtube.com/watch?v=FwEKCP7DVFc&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=56',
                     'https://www.youtube.com/watch?v=cU3rmlDgfbg&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=60',
                     'https://www.youtube.com/watch?v=Du-RQu4soIs&list=PLI1yx5Z0Lrv77D_g1tvF9u3FVqnrNbCRL&index=61'
                     ]

    for i in range(len(youtube_links)):
        src = YouTube(youtube_links[i])
        video = src.streams[1].download(output_path=dir_path)
    return "test"

if __name__ == "__main__":
    app.run(debug=True)
    download_videos()
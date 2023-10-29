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


if __name__ == "__main__":
    app.run(debug=True)
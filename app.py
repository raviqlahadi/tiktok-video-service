from flask import Flask, request, jsonify, Response
import os
import requests
import asyncio
import logging
from TikTokApi import TikTokApi
from dotenv import load_dotenv

# Set up logging to debug and see detailed output
logging.basicConfig(level=logging.DEBUG)
#load env fie 

load_dotenv()

# Set up Flask app
app = Flask(__name__)

# Your TikTok ms_token
ms_token = os.getenv("MS_TOKEN")

# Helper function to fetch trending videos
async def fetch_trending_videos():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        videos = []
        logging.info(f'token: {ms_token}')
        async for video in api.trending.videos(count=10):
            videos.append(video.as_dict)
        return videos

# Helper function to fetch videos by hashtag
async def fetch_videos_by_hashtag(hashtag):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        videos = []
        async for video in api.hashtag(name=hashtag).videos(count=10):
            videos.append(video.as_dict)
        return videos

# Helper function to fetch videos by keyword
async def fetch_videos_by_keyword(keyword):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        videos = []
        async for video in api.search.search_type(search_term=keyword, obj_type="user", count=10):
            videos.append(video.as_dict)
        return videos

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"message": "Gunicorn server is running!"}), 200

# Route for fetching trending videos
@app.route('/api/trending', methods=['GET'])
def trending_videos():
    videos = asyncio.run(fetch_trending_videos())
    return jsonify(videos)

# Route for searching videos by hashtag
@app.route('/api/category', methods=['GET'])
def search_by_hashtag():
    hashtag = request.args.get('hashtag')
    if not hashtag:
        return jsonify({"error": "Please provide a hashtag"}), 400
    videos = asyncio.run(fetch_videos_by_hashtag(hashtag))
    return jsonify(videos)

# Route for searching videos by keyword
@app.route('/api/keyword', methods=['GET'])
def search_by_keyword():
    keyword = request.args.get('query')
    if not keyword:
        return jsonify({"error": "Please provide a query"}), 400
    videos = asyncio.run(fetch_videos_by_keyword(keyword))
    return jsonify(videos)


if __name__ == "__main__":
    app.config['DEBUG'] = os.getenv('DEBUG', 'False') == True 
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    app.run(host=host, port=port)
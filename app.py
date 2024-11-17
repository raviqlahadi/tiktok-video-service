from flask import Flask, request, jsonify, Response
import os
import requests
import asyncio
import logging
from TikTokApi import TikTokApi
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

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

# Playwright health check function
def playwright_health_check():
    try:
        # Check if Playwright can launch a browser and open a page
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Run headless for health check
            page = browser.new_page()
            page.goto("https://www.google.com")
            page_title = page.title()
            browser.close()

        # If the page title was successfully retrieved, Playwright is working fine
        return {"status": "success", "message": f"Playwright is working. Page title: {page_title}"}, 200

    except Exception as e:
        # If there's an error during the Playwright check
        return {"status": "error", "message": f"Playwright health check failed: {str(e)}"}, 500


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"message": "Gunicorn server is running!"}), 200

# Playwright health check route
@app.route('/playwright', methods=['GET'])
def playwright_health():
    # Run Playwright health check as part of this route
    playwright_status, status_code = playwright_health_check()
    return jsonify(playwright_status), status_code

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
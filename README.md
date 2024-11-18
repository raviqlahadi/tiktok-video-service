# TikTok Video Fetching Microservice

A Python microservice for dynamically retrieving TikTok videos based on trending topics, hashtags, or general search queries. This service acts as a backend data provider for the TikTok Video App.

---

## Features

- **Trending Videos**: Fetches the latest trending videos on TikTok.
- **Search by Hashtag**: Retrieves videos associated with specific hashtags.
- **JSON Responses**: Delivers structured JSON data, including metadata and playable video URLs.

---

## System Overview

This microservice fetches data in real-time from TikTok's platform. It does not store data locally or in a database, ensuring lightweight and dynamic performance.

---

## API Endpoints

### 1. Trending Videos
- **URL**: `/trending`
- **Method**: `GET`
- **Description**: Fetches a list of trending TikTok videos.
- **Response Example**:
  ```json
  {
        "id": "7428543665926180103",
        "description": "Video Desc",
        "author": {
            "nickname": "Username",
            "uniqueId": "User unique id",
            ...
        },
        "stats": {
            "playCount": 27200000,
            ...
        },
        "hashtags": [
            {
                "id": "17584774",
                "title": "hashtag"
            }
        ],
        "video": {
            "url": "video url",
            "width": 720,
            "height": 1280,
            "duration": 75
        },
        ...
    }
  ```

### 2. Search by Hashtag
- **URL**: `/category`
- **Method**: `GET`
- **Query Parameter**: 
  - `hashtag` (string): The hashtag to search for.
- **Description**: Returns videos related to the specified hashtag.
- **Example Request**:
  ```
  GET /category?hashtag=food
  ```
- **Response Example**:
  ```json
  {
        "id": "7428543665926180103",
        "description": "Video Desc",
        "author": {
            "nickname": "Username",
            "uniqueId": "User unique id",
            ...
        },
        "stats": {
            "playCount": 27200000,
            ...
        },
        "hashtags": [
            {
                "id": "17584774",
                "title": "hashtag"
            }
        ],
        "video": {
            "url": "video url",
            "width": 720,
            "height": 1280,
            "duration": 75
        },
        ...
    }
  ```
---

## Setup and Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/tiktok-fetch-service.git
   cd tiktok-fetch-service
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Service**:
   ```bash
   python app.py
   ```
   The service will start on `http://localhost:5000` by default.

---

## Configuration

- **Port**: The service runs on port `5000` by default. This can be configured in `app.py`.
- **Dependencies**:
  - `Flask`: For API routing.
  - `requests`: For fetching TikTok data.
  - Other scraping and utility libraries as required.

---

## Known Limitations

- **Latency**: Each request takes approximately 8 seconds to fetch 30 videos.
- **No Caching**: Video data is fetched in real-time and not stored locally.
- **TikTok API Restrictions**: Service may be affected by TikTok's rate limits or changes in their API structure.

---

## Deployment

### Using Gunicorn
1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Server Configuration
- Use a reverse proxy like Nginx for better performance and SSL handling.

---



## Future Enhancements

- Add caching for commonly searched hashtags to improve response time.
- Implement rate-limiting to handle high traffic and prevent service abuse.
- Improve scraping techniques to reduce latency further.

---

## License

This project is licensed under the [MIT License](LICENSE).
```

This Markdown should now render properly in any Markdown viewer. Let me know if you need additional modifications!

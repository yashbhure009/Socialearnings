from flask import Flask, request, render_template, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

YOUTUBE_API_KEY = os.getenv('AIzaSyAJ9Vl-vHjn97opVrRiuynyMKiQyH35kuQ')
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN')

def get_youtube_video_data(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={AIzaSyAJ9Vl-vHjn97opVrRiuynyMKiQyH35kuQ}'
    response = requests.get(url)
    data = response.json()
    if 'items' in data and len(data['items']) > 0:
        stats = data['items'][0]['statistics']
        return {
            'views': stats.get('viewCount', 0),
            'likes': stats.get('likeCount', 0),
            'comments': stats.get('commentCount', 0)
        }
    return None

def get_instagram_video_data(post_id):
    url = f'https://graph.instagram.com/{post_id}?fields=like_count,comments_count,media_url&access_token={INSTAGRAM_ACCESS_TOKEN}'
    response = requests.get(url)
    data = response.json()
    return {
        'likes': data.get('like_count', 0),
        'comments': data.get('comments_count', 0),
        'media_url': data.get('media_url', '')
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form['url']
    if 'youtube.com' in url:
        video_id = url.split('v=')[-1]
        data = get_youtube_video_data(video_id)
    elif 'instagram.com' in url:
        post_id = url.split('/')[-2]
        data = get_instagram_video_data(post_id)
    else:
        return jsonify({'error': 'Invalid URL'}), 400

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
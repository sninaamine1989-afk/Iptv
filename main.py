from flask import Flask, Response, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://dlive.sx/'
}

@app.route('/stream.m3u8')
def get_stream():
    try:
        # 1. جلب محتوى الصفحة الأصلية
        page_res = requests.get("https://dlive.sx/stream/stream-91.php", headers=HEADERS, timeout=10)
        
        # 2. البحث عن رابط m3u8 الحقيقي داخل السكريبت
        match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', page_res.text)
        
        if match:
            m3u8_url = match.group(1)
            # جلب ملف m3u8
            stream_res = requests.get(m3u8_url, headers=HEADERS, timeout=10)
            
            response = Response(stream_res.content, content_type='application/vnd.apple.mpegurl')
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            return jsonify({"error": "m3u8 URL not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

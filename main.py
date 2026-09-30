from flask import Flask, Response, jsonify, request
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
        # جلب الصفحة الأصلية
        page_res = requests.get("https://dlive.sx/stream/stream-91.php", headers=HEADERS, timeout=10)
        
        # استخراج رابط m3u8
        match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', page_res.text)
        
        if match:
            m3u8_url = match.group(1)
            stream_res = requests.get(m3u8_url, headers=HEADERS, timeout=10)
            
            # إرجاع ملف m3u8 مع تصاريح CORS كاملة وتحديد نوع المحتوى
            response = Response(stream_res.content, content_type='application/vnd.apple.mpegurl')
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            return response
        else:
            return jsonify({"error": "Stream URL not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

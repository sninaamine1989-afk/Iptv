from flask import Flask, Response, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://dlive.sx/'
}

@app.route('/stream.m3u8')
def get_stream():
    try:
        # 1. جلب صفحة البث الأصلية
        target_url = "https://dlive.sx/stream/stream-91.php"
        res = requests.get(target_url, headers=HEADERS, timeout=10)
        
        # 2. استخراج رابط ملف .m3u8 الحقيقي
        match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', res.text)
        
        if match:
            m3u8_url = match.group(1)
            
            # 3. جلب ملف m3u8 الخام (بدون واجهة أو إعلانات الموقع)
            stream_res = requests.get(m3u8_url, headers=HEADERS, timeout=10)
            
            # 4. إرجاع محتوى البث الصافي مع تفعيل CORS بالكامل
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

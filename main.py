from flask import Flask, Response, jsonify
from flask_cors import CORS
import streamlink
import requests

app = Flask(__name__)
CORS(app)  # السماح التام لجميع المواقع والتطبيقات بقراءة البث

@app.route('/stream.m3u8')
def get_stream():
    try:
        # 1. جلب رابط البث الصافي من Streamlink
        streams = streamlink.streams("https://dlive.sx/stream/stream-91.php")
        if 'best' in streams:
            stream_url = streams['best'].url
            
            # 2. قراءة محتوى ملف الـ m3u8 عبر الخادم نفسه
            res = requests.get(stream_url, timeout=10)
            
            # 3. تمرير ملف m3u8 مباشرة إلى المشغل مع ترويسات CORS كاملة
            response = Response(res.content, content_type='application/vnd.apple.mpegurl')
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = '*'
            return response
        else:
            return jsonify({"error": "Stream not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

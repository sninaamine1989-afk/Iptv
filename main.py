from flask import Flask, Response, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/stream.m3u8')
def get_stream():
    try:
        # إرسال طلب مع ترويسات متصفح وهمية لتجاوز الحماية
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://dlive.sx/'
        }
        
        # رابط صفحة البث الأصلية
        source_url = "https://dlive.sx/stream/stream-91.php"
        res = requests.get(source_url, headers=headers, timeout=10)
        
        # تحويل الاستجابة وإضافة ترويسات CORS كاملة لتشغيلها في بلوجر
        response = Response(res.content, content_type='text/html')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

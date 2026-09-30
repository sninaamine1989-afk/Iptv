from flask import Flask, Response, jsonify, redirect
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
        
        # 2. استخراج رابط ملف .m3u8 الحقيقي من الكود
        match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', res.text)
        
        if match:
            stream_url = match.group(1)
            # إعادة توجيه التطبيق أو المشغل مباشرة إلى رابط البث الخام
            return redirect(stream_url, code=302)
        else:
            return jsonify({"error": "Stream URL not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

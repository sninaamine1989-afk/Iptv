from flask import Flask, redirect, jsonify, Response
from flask_cors import CORS
import streamlink

app = Flask(__name__)
CORS(app)  # السماح لجميع المواقع وبلوجر بقراءة البث بدون حظر CORS

@app.route('/stream.m3u8')
def get_stream():
    try:
        streams = streamlink.streams("https://dlive.sx/stream/stream-91.php")
        if 'best' in streams:
            stream_url = streams['best'].url
            # عمل توجيه مباشر برأس CORS واضح
            response = redirect(stream_url, code=302)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            return jsonify({"error": "Stream not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from flask import Flask, redirect, jsonify
import streamlink

app = Flask(__name__)

@app.route('/stream.m3u8')
def get_stream():
    try:
        streams = streamlink.streams("https://dlive.sx/stream/stream-91.php")
        stream_url = streams['best'].url
        return redirect(stream_url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

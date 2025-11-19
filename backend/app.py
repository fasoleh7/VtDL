from flask import Flask, request, send_file, jsonify
import yt_dlp
import tempfile
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json() or {}
    url = data.get('url')
    if not url:
        return jsonify({"error": "missing url"}), 400

    try:
        tmpdir = tempfile.mkdtemp()
        outtmpl = os.path.join(tmpdir, '%(id)s.%(ext)s')

        ydl_opts = {
            'outtmpl': outtmpl,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if not os.path.exists(filename):
                files = os.listdir(tmpdir)
                if files:
                    filename = os.path.join(tmpdir, files[0])
                else:
                    raise Exception("file not found")

        return send_file(filename, as_attachment=True, download_name=os.path.basename(filename))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

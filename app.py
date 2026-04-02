from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    video_url = data.get('url')

    if not video_url:
        return jsonify({"status": "error", "message": "Please enter a valid URL."}), 400

    try:
        # Ek temporary folder banate hain
        temp_dir = tempfile.mkdtemp()
        
        # YouTube Bot-Block Bypass Settings
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'geo_bypass': True,           # Cloud servers ke location blocks ko bypass karega
            'nocheckcertificate': True,   # SSL errors ko ignore karega
            'extractor_args': {'youtube': {'player_client': ['android']}} # YouTube ko lagega ki request Android mobile se aayi hai
        }

        # Video Download karna
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        # File sidha aapke phone/browser par bhej dega
        return send_file(filename, as_attachment=True)

    except Exception as e:
        # Ab agar error aaya toh actual YouTube ki taraf se aaya error aapki screen par dikhega!
        return jsonify({"status": "error", "message": f"Error Info: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

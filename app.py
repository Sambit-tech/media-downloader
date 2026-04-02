from flask import Flask, render_template, request, jsonify
import requests

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
        # Hum direct Cobalt API ka use kar rahe hain jo bot-blocks bypass karti hai
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "url": video_url
        }
        
        # API request bhejna
        response = requests.post("https://api.cobalt.tools/api/json", json=payload, headers=headers)
        
        if response.status_code == 200:
            res_data = response.json()
            if "url" in res_data:
                # API ne video ka direct direct link de diya!
                return jsonify({"status": "success", "download_url": res_data["url"]}), 200
            else:
                return jsonify({"status": "error", "message": "API could not process this video."}), 500
        else:
            return jsonify({"status": "error", "message": "YouTube blocked the API request temporarily."}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

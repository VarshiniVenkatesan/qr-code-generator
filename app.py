from flask import Flask, render_template, request, send_file, jsonify
import qrcode
import os
import tempfile
from datetime import datetime

app = Flask(__name__)

# Use temporary directory (since Render does not support persistent storage)
DOWNLOADS_FOLDER = tempfile.gettempdir()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.form.get('data', '').strip()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Generate filename from domain name or use a timestamp
    domain = data.split('//')[-1].split('/')[0].replace('.', '_')
    filename = f"{domain}.png" if domain else f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"

    filepath = os.path.join(DOWNLOADS_FOLDER, filename)
    
    # Generate QR code
    qr = qrcode.make(data)
    qr.save(filepath)  # Save in temp folder

    return jsonify({"filename": filename, "download_url": f"/download_qr/{filename}"})

@app.route('/download_qr/<filename>')
def download_qr(filename):
    file_path = os.path.join(DOWNLOADS_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Required for Render

from flask import Flask, render_template, request, send_file
import qrcode
import os
from datetime import datetime
import platform

app = Flask(__name__)

# Detect OS and set Downloads folder
if platform.system() == "Windows":
    DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
else:
    DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)  # Ensure folder exists

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.form['data']
    
    if not data:
        return {"error": "No data provided"}, 400
    
    # Generate filename from domain name or generic
    domain = data.split('//')[-1].split('/')[0].replace('.', '_')
    filename = f"{domain}.png" if domain else f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"

    filepath = os.path.join(DOWNLOADS_FOLDER, filename)
    
    # Generate QR code
    qr = qrcode.make(data)
    qr.save(filepath)  # Save QR code in Downloads folder

    return {"filename": filename}

@app.route('/download_qr/<filename>')
def download_qr(filename):
    file_path = os.path.join(DOWNLOADS_FOLDER, filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

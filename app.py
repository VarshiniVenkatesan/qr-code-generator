from flask import Flask, render_template, request, send_file
import qrcode
import io
import os
from datetime import datetime

app = Flask(__name__)

SAVE_FOLDER = "static/qrcodes"  # Folder to save QR codes
os.makedirs(SAVE_FOLDER, exist_ok=True)  # Create folder if not exists

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.form['data']
    
    if not data:
        return "No data provided", 400
    
    # Generate QR code
    qr = qrcode.make(data)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Unique filename
    filename = f"qr_{timestamp}.png"
    filepath = os.path.join(SAVE_FOLDER, filename)
    
    qr.save(filepath)  # Save QR code in static folder

    return {"filepath": filepath, "filename": filename}

if __name__ == '__main__':
    app.run(debug=True)

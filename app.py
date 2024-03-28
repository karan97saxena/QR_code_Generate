from flask import Flask, render_template, request, send_file
import qrcode
import base64
import os

app = Flask(__name__)

def generate_qr_code(url, file_name='qr_code.png', scale=8, border=4):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=scale,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_path = os.path.join('qr_code_folder', file_name)
    qr_img.save(qr_img_path)
    return qr_img_path

@app.route('/')
def index():
    return render_template('index.html', qr_code_data=None)

@app.route('/', methods=['POST'])
def generate_qr():
    url = request.form['url']
    qr_img_path = generate_qr_code(url)
    with open(qr_img_path, 'rb') as f:
        qr_img_data = base64.b64encode(f.read()).decode('utf-8')
    return render_template('index.html', qr_code_data=qr_img_data)

@app.route('/download')
def download_qr():
    file_path = os.path.join('qr_code_folder', 'qr_code.png')
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

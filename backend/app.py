from flask import Flask, request, jsonify
import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

fmgr_ip = os.getenv("FMGR_IP")
username = os.getenv("FMGR_USERNAME")
password = os.getenv("FMGR_PASSWORD")

def login():
    url = f"https://{fmgr_ip}/jsonrpc"
    payload = {
        "method": "exec",
        "params": [
            {
                "url": "/sys/login/user",
                "data": {
                    "user": username,
                    "passwd": password
                }
            }
        ],
        "id": 1
    }
    response = requests.post(url, json=payload, verify=False)
    return response.json().get("session")

def get_device_info(adom, session_id):
    url = f"https://{fmgr_ip}/jsonrpc"
    headers = {"Authorization": f"Bearer {session_id}"}
    payload = {
        "method": "get",
        "params": [
            {
                "url": f"/dvmdb/adom/{adom}/device",
                "fields": ["name", "vdom", "ip", "vlan"]
            }
        ],
        "id": 2
    }
    response = requests.post(url, headers=headers, json=payload, verify=False)
    return response.json().get("result")[0].get("data")

@app.route('/get_device_info', methods=['POST'])
def device_info():
    adom = request.json.get('adom')
    session_id = login()
    devices = get_device_info(adom, session_id)
    return jsonify(devices)

@app.route('/send_email', methods=['POST'])
def send_email():
    html_content = request.json.get('html_content')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Device Information"
    msg['From'] = "your_email@example.com"
    msg['To'] = "recipient@example.com"

    part = MIMEText(html_content, 'html')
    msg.attach(part)

    with smtplib.SMTP('smtp.example.com') as server:
        server.login("your_email@example.com", "your_password")
        server.sendmail(msg['From'], [msg['To']], msg.as_string())

    return jsonify({"message": "Email sent successfully"})

if __name__ == '__main__':
    app.run(debug=True)

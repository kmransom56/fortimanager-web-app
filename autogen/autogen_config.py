import os
import autogen
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration for AutoGen
config_list = [
    {"model": "gpt-4-turbo-preview", "api_key": os.getenv("OPENAI_API_KEY")}
]

# Define the Engineer agent
engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config={"temperature": 0, "config_list": config_list},
    system_message="I'm Engineer. I'm an expert in Python programming and JavaScript development. I'm executing code tasks required by Admin."
)

# Define the Admin agent
admin = autogen.UserProxyAgent(
    name="Admin",
    human_input_mode="ALWAYS",
    code_execution_config=False
)

# Set up the group chat
groupchat = autogen.GroupChat(
    agents=[engineer, admin],
    messages=[],
    max_round=500,
    speaker_selection_method="round_robin",
    enable_clear_history=True
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"temperature": 0, "config_list": config_list})

# Define functions for backend generation
@admin.register_for_execution()
@engineer.register_for_llm(description="Generate Flask backend code.")
def generate_backend():
    backend_code = """
    from flask import Flask, request, jsonify
    import requests
    import json
    import pandas as pd
    from dotenv import load_dotenv
    import os
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from jinja2 import Template
    import smtplib
    
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
    """
    return backend_code

# Define functions for frontend generation
@admin.register_for_execution()
@engineer.register_for_llm(description="Generate React frontend code.")
def generate_frontend():
    frontend_code = """
    import React, { useState } from 'react';
    import axios from 'axios';
    import AdomSelector from './AdomSelector';
    import DeviceInfoTable from './DeviceInfoTable';
    import { exportToExcel, generateHtml, sendEmail } from './utils';

    function App() {
        const [adom, setAdom] = useState('');
        const [devices, setDevices] = useState([]);

        const fetchDeviceInfo = async () => {
            const response = await axios.post('/get_device_info', { adom });
            setDevices(response.data);
        };

        const handleExportToExcel = () => {
            exportToExcel(devices);
        };

        const handleSendEmail = () => {
            const htmlContent = generateHtml(devices);
            sendEmail(htmlContent);
        };

        return (
            <div>
                <AdomSelector setAdom={setAdom} />
                <button onClick={fetchDeviceInfo}>Get Device Info</button>
                <DeviceInfoTable devices={devices} />
                <button onClick={handleExportToExcel}>Export to Excel</button>
                <button onClick={handleSendEmail}>Send Email</button>
            </div>
        );
    }

    export default App;
    """
    return frontend_code

# Define utility functions
@admin.register_for_execution()
@engineer.register_for_llm(description="Generate utility functions for frontend.")
def generate_utils():
    utils_code = """
    import { saveAs } from 'file-saver';
    import XLSX from 'xlsx';
    import { template } from 'lodash';
    import axios from 'axios';

    export const exportToExcel = (devices) => {
        const data = devices.map(device => ({
            Device: device.name,
            VDOM: device.vdom,
            IP: device.ip,
            VLAN: device.vlan
        }));
        const worksheet = XLSX.utils.json_to_sheet(data);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Devices');
        const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
        const dataBlob = new Blob([excelBuffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        saveAs(dataBlob, 'device_info.xlsx');
    };

    export const generateHtml = (devices) => {
        const htmlTemplate = `
        <html>
        <body>
            <h1>Device Information</h1>
            <table border="1">
                <tr>
                    <th>Device</th>
                    <th>VDOM</th>
                    <th>IP</th>
                    <th>VLAN</th>
                </tr>
                <% devices.forEach(device => { %>
                <tr>
                    <td><%= device.name %></td>
                    <td><%= device.vdom %></td>
                    <td><%= device.ip %></td>
                    <td><%= device.vlan %></td>
                </tr>
                <% }); %>
            </table>
        </body>
        </html>
        `;
        return template(htmlTemplate)({ devices });
    };

    export const sendEmail = (htmlContent) => {
        axios.post('/send_email', { html_content: htmlContent })
            .then(response => {
                console.log('Email sent successfully');
            })
            .catch(error => {
                console.error('Error sending email:', error);
            });
    };
    """
    return utils_code

# Generate the backend and frontend code
manager.run()

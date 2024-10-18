import pandas as pd
import { saveAs } from 'file-saver';
import XLSX from 'xlsx';
import { jsPDF } from 'jspdf';
import { template } from 'lodash';

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
    // Assuming you have a backend route to handle sending emails
    axios.post('/send_email', { html_content: htmlContent })
        .then(response => {
            console.log('Email sent successfully');
        })
        .catch(error => {
            console.error('Error sending email:', error);
        });
};

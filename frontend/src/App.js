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

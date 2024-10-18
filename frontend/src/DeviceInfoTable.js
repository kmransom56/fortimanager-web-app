import React from 'react';

const DeviceInfoTable = ({ devices }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Device</th>
                    <th>VDOM</th>
                    <th>IP</th>
                    <th>VLAN</th>
                </tr>
            </thead>
            <tbody>
                {devices.map(device => (
                    <tr key={device.name}>
                        <td>{device.name}</td>
                        <td>{device.vdom}</td>
                        <td>{device.ip}</td>
                        <td>{device.vlan}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}

export default DeviceInfoTable;

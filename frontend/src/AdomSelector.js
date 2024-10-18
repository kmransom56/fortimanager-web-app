import React from 'react';

const AdomSelector = ({ setAdom }) => {
    return (
        <select onChange={(e) => setAdom(e.target.value)}>
            <option value="adom1">ADOM 1</option>
            <option value="adom2">ADOM 2</option>
        </select>
    );
}

export default AdomSelector;

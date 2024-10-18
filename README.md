# FortiManager Web App

This web app allows users to interact with FortiManager, retrieve IP addresses and VLANs for each FortiGate, and output the results in various formats.

## Autogen Installation

There is an autogen script in the autogen directory. 
Prior to running the script. 
Ensure you have AutoGen installed. You can install it using pip:

pip install autogen-agentchat.
cd autogen

python -m venv venv
source venv/bin/activate 

python autogen_config.py

## Manual Installation

## Backend

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   
2. Create a virtual environment and activate it:
bash

Copy
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the required packages:

bash

Copy
pip install -r requirements.txt

4. Create a .env file with your FortiManager credentials:
env

Copy
FMGR_IP=your_fortimanager_ip
FMGR_USERNAME=your_username
FMGR_PASSWORD=your_password
FMGR_ADOM=your_adom_name

5. Run the Flask app:
bash
Copy
flask run

## Frontend

1. Navigate to the frontend directory:

bash

Copy
cd frontend

2. Install the required packages:

bash
Copy
npm install
3. Start the React app:

bash

Copy
npm start

##Usage
Open your browser and navigate to http://localhost:3000.

Select the ADOM and retrieve the device information.

Export the data to Excel or generate an HTML report for email.

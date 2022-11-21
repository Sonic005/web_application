import json
from base64 import b64encode
import pandas as pd
import requests  # To install requests, use: pip install requests
import urllib3

endpoint = '/agents?select=lastKeepAlive&select=id&status=disconnected'
protocol = 'https'
host = '192.168.1.9'
port = 55000
user = 'wazuh-wui'
password = 'MyS3cr37P450r.*-'


class Conn:
    def __init__(self):
        self.endpoint = '/agents?select=lastKeepAlive&select=id&status=disconnected'
        self.protocol = 'https'
        self.host = '192.168.1.9'
        self.port = 55000
        self.user ='wazuh-wui'
        self.password ='MyS3cr37P450r.*-'
        self.token =None
    
    # Disable insecure https warnings (for self-signed SSL certificates)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    def connect_to_wazuh (self):       
        try:
            base_url = f"{self.protocol}://{self.host}:{self.port}"
            login_url = f"{base_url}/security/user/authenticate"
            basic_auth = f"{self.user}:{self.password}".encode()
            self.token = {'Authorization': f'Basic {b64encode(basic_auth).decode()}'}          
            self.token['Authorization'] = f'Bearer {self.get_response(login_url, self.token)["data"]["token"]}'   
            #Request
            response = self.get_response(base_url + self.endpoint, self.token)            
            return True
        except requests.exceptions.RequestException as e:
            print("Error Connections")
            raise SystemExit(e)
    

    def get_response(self ,url, headers, verify=False):
        print("Get API result")
        request_result = requests.get( url, headers=headers, verify=verify)

        if request_result.status_code == 200:
            return json.loads(request_result.content.decode())
        else:
            raise Exception(f"Error obtaining response: {request_result.json()}")

    
    def get_rule (self, rule_id):
        base_url = f"{self.protocol}://{self.host}:{self.port}"
        try:
            response = self.get_response(base_url+'/rules?rule_ids='+rule_id+'&pretty=true',self.token)
            return response
        except requests.exceptions.RequestException as e:
            print("Error Connections")
            raise SystemExit(e)


    def get_agents (self ):
        base_url = f"{self.protocol}://{self.host}:{self.port}"
        try:
            response = self.get_response(base_url+'/agents?pretty=true&sort=-ip,name',self.token)
            return response
        except requests.exceptions.RequestException as e:
            print("Error Connections")
            raise SystemExit(e)
        
    
    def add_agen(self , name , agent_name):
        params = {'pretty': 'true',}
        json_data = {'name': '<agent_name>',}
        base_url = f"{self.protocol}://{self.host}:{self.port}"
        try:
            response = requests.post( base_url, params=params, headers=self.token, json=json_data)
            print("Successfully added AGENT")
            return response
        except requests.exceptions.RequestException as e:
            print("Error Connections")
            raise SystemExit(e)


    def delete_agent(self, agent_id):
        base_url = f"{self.protocol}://{self.host}:{self.port}"
        try:
            response = requests.delete(base_url+"/agents?pretty=true&older_than=0s&agents_list="+agent_id+"&status=all", headers=self.token)
            print("Successfully DELETED AGENT")
            return response
        except requests.exceptions.RequestException as e:
            print("Error Connections")
            raise SystemExit(e)
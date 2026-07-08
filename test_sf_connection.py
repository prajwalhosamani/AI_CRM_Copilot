import os
import requests
from simple_salesforce import Salesforce

MY_DOMAIN = os.environ["SF_MY_DOMAIN"]

auth_url = f"{MY_DOMAIN}/services/oauth2/token"

payload = {
    "grant_type": "client_credentials",
    "client_id": os.environ["SF_CLIENT_ID"],
    "client_secret": os.environ["SF_CLIENT_SECRET"]
}

response = requests.post(auth_url, data=payload)
if response.status_code != 200:
    print("Error response from Salesforce:")
    print(response.text)
response.raise_for_status()
auth_data = response.json()

sf = Salesforce(
    instance_url=auth_data["instance_url"],
    session_id=auth_data["access_token"]
)

result = sf.query("SELECT Id, Name, Amount, StageName FROM Opportunity LIMIT 5")
for record in result["records"]:
    print(record["Name"], record["Amount"], record["StageName"])
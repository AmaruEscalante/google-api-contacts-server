"""
Script that uses google services to manage your google account contacts.
Author: Amaru Escalante
"""

from google.oauth2 import service_account
import googleapiclient.discovery

import json

SCOPES = ["https://www.googleapis.com/auth/contacts"]
SERVICE_ACCOUNT_FILE = "old-credentials.json"

# https://stackoverflow.com/questions/65897777/google-contacts-are-not-showing-by-using-google-people-api
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES, subject="your@mail.com"
)
people_service = googleapiclient.discovery.build("people", "v1", credentials=credentials)

givenName = "Jhon"
familyName = "Doe"
phone = "+56988888888"
email = "test@mail.com"
event = people_service.people().createContact(
    body={
        "names": [{"givenName": givenName, "familyName": familyName}],
        "phoneNumbers": [{"value": str(phone)}],
        "emailAddresses": [{"value": email}],
    }
)
resp = event.execute()
print(f"Response of Create Contact for {givenName} {familyName}", json.dumps(resp, sort_keys=True, indent=4))


# Send an empty request first to prepare the cache https://developers.google.com/people/api/rest/v1/people/searchContacts
event = people_service.people().searchContacts(pageSize="1", query="", readMask="names,emailAddresses")
event.execute()
event = people_service.people().searchContacts(pageSize="1", query=givenName, readMask="names,emailAddresses")
resp = event.execute()
print(json.dumps(resp, sort_keys=True, indent=4))

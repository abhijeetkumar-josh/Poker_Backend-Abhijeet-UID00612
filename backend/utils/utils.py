import requests
from requests.auth import HTTPBasicAuth
from api_keys.models import ApiKeys
from rest_framework import status
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
import json


def load_private_key():
    with open("private.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key


def decrypt_message(encrypted_message_b64: str) -> str:
    private_key = load_private_key()

    encrypted_bytes = base64.b64decode(encrypted_message_b64)

    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.PKCS1v15()
    )

    return  json.loads(decrypted.decode("utf-8"))

class JiraValidation:
    def validate_and_store_api(self, apikey, cloudsite, host, save=False):

        url = f"https://{cloudsite}/rest/api/3/myself"

        try:
            response = requests.get(
                url,
                auth=HTTPBasicAuth(host.email, apikey),
                headers={"Accept": "application/json"}
            )

            try:
                data = response.json()
            except ValueError:
                data = {"error": response.text}

            if save and response.status_code == 200:
                ApiKeys.objects.create(
                    user=host,
                    apikey= apikey,
                    cloudsite=cloudsite,
                )

            return data, response.status_code

        except requests.RequestException as e:
            return {"error": str(e)}, status.HTTP_400_BAD_REQUEST

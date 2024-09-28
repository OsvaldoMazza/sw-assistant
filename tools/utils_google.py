import json
import os

def create_google_credentials_json():
    # Recuperar variables de entorno con prefijo 'google_'
    client_id = os.getenv('google_client_id')
    client_secret = os.getenv('google_client_secret')
    project_id = os.getenv('google_project_id')
    auth_uri = os.getenv('google_auth_uri', 'https://accounts.google.com/o/oauth2/auth')
    token_uri = os.getenv('google_token_uri', 'https://oauth2.googleapis.com/token')
    auth_provider_x509_cert_url = os.getenv('google_auth_provider_cert_url', 'https://www.googleapis.com/oauth2/v1/certs')
    redirect_uris = os.getenv('google_redirect_uris', 'urn:ietf:wg:oauth:2.0:oob,http://localhost').split(',')

    # Construir el contenido del archivo JSON
    credentials_data = {
        "installed": {
            "client_id": client_id,
            "project_id": project_id,
            "auth_uri": auth_uri,
            "token_uri": token_uri,
            "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
            "client_secret": client_secret,
            "redirect_uris": redirect_uris
        }
    }

    file_path = os.path.join(os.getcwd(), 'temp', 'client_secrets.json')

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as json_file:
        json.dump(credentials_data, json_file, indent=4)


def check_exist_credentials():
    pathfile = './temp/client_secrets.json'
    if os.path.exists(pathfile):
        return
    else:
        create_google_credentials_json()

def ensure_gmt_offset(datetime_string, gmt):
    if gmt not in datetime_string:
        return datetime_string + gmt
    return datetime_string
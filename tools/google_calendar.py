import os
import datetime
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import tools.utils_google as utils_google
from models.google_model import event_calendar

default_max_events = 3
gmt = '-03:00'

# Si modificas estos alcances, elimina el archivo token.pickle
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service2():
    try:
        creds = None
        # Si existe el archivo token.json, carga las credenciales
        if os.path.exists('./temp/token.json'):
            creds = Credentials.from_authorized_user_file('./temp/token.json', SCOPES)
        
        # Si no hay credenciales válidas, o no hay token.json, solicita un nuevo inicio de sesión
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './temp/client_secrets.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Guarda las credenciales para el próximo uso
            with open('./temp/token.json', 'w') as token:
                token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)
    
    except Exception as e:
        print(f"### ERROR ### Get_calendar_service: {e}")
        
        return None


def get_calendar_service():
    try:
        utils_google.check_exist_credentials()
        creds = None
        # El archivo token.pickle almacena las credenciales de acceso del usuario.
        # Si el archivo ya existe, las carga para evitar una nueva autenticación.
        if os.path.exists('./temp/token.pickle'):
            with open('./temp/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # Si no hay credenciales válidas, el usuario debe iniciar sesión.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './temp/client_secrets.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Guarda las credenciales para futuras ejecuciones.
            with open('./temp/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # Llama a la API de Google Calendar
        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(f"### ERROR ### Get_calendar_service: {e}")
        
        return None


def get_events(arguments):
    days = arguments.get('days')
    number_events = arguments.get('number_events')
    date = datetime.datetime.now()
    if days != None:
       date += datetime.timedelta(days = days)
    date = date.isoformat() + 'Z'  # 'Z' indica UTC
    
    if number_events == None:
        number_events = default_max_events

    service = get_calendar_service2()

    if (service == None):
        return None
    
    events_result = service.events().list(calendarId='primary', timeMin=date,
                                        maxResults=number_events, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    events_with_days = []
    date_now = datetime.datetime.now()

    if not events:
        print('Google Calendar: No hay eventos próximos.')

        return 'No hay eventos próximos'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        event_date = datetime.datetime.strptime(start[:10], "%Y-%m-%d")
        days_left = event_date.day - date_now.day
        events_with_days.append({
            "event": event['summary'],
            "date": start,
            "days_left": days_left,
            "id": event['id']
        })
    
    response_object = {
        "date_now": date_now.strftime("%Y-%m-%d %H:%M:%S"),
        "events": events_with_days
    }
    
    return response_object

def set_events(arguments):
    if arguments.get('end_datetime'):
        endtime = arguments.get('end_datetime')
    else:
        endtime =  datetime.datetime.strptime(arguments.get('start_datetime')[:-6], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=1)

    endtime = endtime.replace('Z','')
    startime = (arguments.get('start_datetime')).replace('Z','')

    reminder = None
    if arguments.get('reminder_minutes'):
        reminder = arguments.get('reminder_minutes')
    else: 
        reminder = None

    event = event_calendar(
        arguments.get('summary'),
        startime,
        endtime,
        arguments.get('location'),
        arguments.get('description'),
        reminder
        )

    event_to_send = event.to_dict()

    service = get_calendar_service2()

    try:
        if arguments.get('eventId'):
            service.events().update(calendarId='primary', eventId = arguments.get('eventId') ,body=event_to_send).execute()
            print("Google Calendar: updated Event")
            return "evento actualizado"
        else:
            service.events().insert(calendarId='primary', body=event_to_send).execute()
            print("Google Calendar: created Event")
            return "evento agendado"
        
        
    except Exception as e:
        print(f"Google Calendar insert Error: {e}")
        
        return "No pude agendar el evento"
    
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Credenciales de la API de Spotify
SPOTIPY_CLIENT_ID = os.getenv('spotify_client_id')
SPOTIPY_CLIENT_SECRET = os.getenv('spotify_client_secret')
SPOTIPY_REDIRECT_URI = os.getenv('spotify_redirect_url')  # La URL de redirección que configuraste en tu app de Spotify

# Crear autenticación usando Spotipy con el ámbito necesario para controlar la reproducción
scope = "user-read-playback-state,user-modify-playback-state"

def search_and_play_song(song_name):
    # Buscar la canción
    sp = get_credencial()

    if (sp == None):
        return "Falló las credenciales de SPOTIFY"
    
    result = sp.search(q=song_name, type='track', limit=1)
    if result['tracks']['items']:
        track = result['tracks']['items'][0]
        track_uri = track['uri']
        print(f"Reproduciendo {track['name']} de {track['artists'][0]['name']}")

        # Obtener el dispositivo de reproducción actual
        devices = sp.devices()
        if devices['devices']:
            device_id = devices['devices'][0]['id']

            # Iniciar la reproducción en el dispositivo
            sp.start_playback(device_id=device_id, uris=[track_uri])
        else:
            print("No se encontraron dispositivos disponibles para la reproducción.")
    else:
        print("No se encontró la canción.")

def stop_play():
    # Obtener el dispositivo actual
    devices = sp.devices()
    if devices['devices']:
        device_id = devices['devices'][0]['id']

        # Pausar la reproducción
        sp = get_credencial()

        if (sp == None):
            return "Falló las credenciales de SPOTIFY"
    
        sp.pause_playback(device_id=device_id)
        print("La reproducción ha sido pausada.")
    else:
        print("No se encontró un dispositivo activo para pausar la reproducción.")

def get_credencial():
    try: 
        credencial = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                client_secret=SPOTIPY_CLIENT_SECRET,
                                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                                scope=scope))
    
        return credencial
    
    except Exception as e:
        print(f"### ERROR ### get_credencial SPOTIFY: {e}")
        
        return None

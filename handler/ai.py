
import json
import os
from openai import OpenAI, AzureOpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
import tiktoken

from tools.google_weather import get_weather
from tools.google_calendar import get_events, set_events
from tools.spotify import search_and_play_song, stop_play
import config
from management.utils import get_assistant_behavior, get_tools, get_lang_value

class Openai_handler:   
    def __init__(self, behavior= get_assistant_behavior()):
        self.client = get_client()
        self.chat_history = [{"role": "system", "content": behavior}]
        self.tiktoken = tiktoken.encoding_for_model(config.chat_model)
    
    def trim_history(self):
        available_tokens = config.max_tokens - config.max_response_tokens
        while self.count_tokens() > available_tokens:
            self.chat_history .pop(1)
        return self.chat_history
    
    def count_tokens(self):
        num_tokens = 0
        for message in self.chat_history:
            num_tokens += len(self.tiktoken.encode(message["content"]))
        print(f"+-- tokens: {num_tokens} ...")
        
        return num_tokens

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def send_query(self, text, tools=None, tool_choice=None):
        self.chat_history.append({"role": "user", "content": text})
        self.trim_history()
        try:
            return self.client.chat.completions.create(
                model= config.chat_model,
                tools = tools,
                tool_choice = tool_choice,
                messages= self.chat_history
            )
        except Exception as e:
            print("Unable to generate ChatCompletion response")
            print(f"Exception: {e}")
        return e
    
    def send_question(self, text):
        tools = get_tools() if config.enable_tools == True else None
        tool_choice = None
        result = self.send_query(text, tools, tool_choice)
        text_to_say = self.analyze_result(result)
        print(f"+-- IA response: {text_to_say} ...")

        return text_to_say
    
    def analyze_result(self, ai_response):
        message = ai_response.choices[0].message

        if message.content:
            assistant_message = message.content.strip()
            self.chat_history.append({"role": "assistant", "content": assistant_message})
            return assistant_message

        if hasattr(message, 'tool_calls'):
            for call in message.tool_calls:
                arguments = json.loads(call.function.arguments)
                func_name = call.function.name

                if func_name == 'get_current_weather':
                    return get_weather(arguments)

                if func_name == 'get_n_day_weather_forecast':
                    return get_weather(arguments)

                if func_name == 'get_calendar_events':
                    result = get_events(arguments)
                    if result == None:
                        return "No se pudo realizar la tarea"
                    return self.send_question(json.dumps(result))
                
                if func_name == 'set_calendar_event':
                    return set_events(arguments)
                
                if func_name == 'play_song_spotify':
                    return search_and_play_song(arguments)
                
                if func_name == 'stop_song_spotify':
                    return stop_play(arguments)
                
                return get_lang_value('not_understand')

def get_client():
    if config.connection_type == 'openai':
        return  OpenAI(api_key = os.getenv("openai_apikey"),)
    
    if config.connection_type == 'azure':
        return AzureOpenAI(
                azure_endpoint = os.getenv("azure_endpoint"), 
                api_key= os.getenv("azure_apikey"),  
                api_version= config.azure_api_version
            )
    
    return None
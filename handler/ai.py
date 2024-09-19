
import json
import os
from openai import OpenAI
from tenacity import retry, wait_random_exponential, stop_after_attempt
from tools.google_weather import get_weather

import config
from management.utils import get_tools, get_lang_value

class Openai_handler:   
    def __init__(self, behavior= get_lang_value('assistant_behavior')):
        self.client = OpenAI(
             api_key = os.getenv("apikey"),
        )
        self.system_behavior = behavior

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def send_query(self, text, tools=None, tool_choice=None):
        try:
            return self.client.chat.completions.create(
                model= config.chat_model,
                tools = tools,
                tool_choice = tool_choice,
                messages=[
                    {"role": "system", "content": self.system_behavior},
                    {"role": "user", "content": text}
                ]
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
        if message.content != None:
            return message.content.strip()
        elif hasattr(message, 'tool_calls'):
            for call in message.tool_calls:
                arguments = json.loads(call.function.arguments)
                if (call.function.name == 'get_current_weather'):
                  return get_weather(arguments['location'])
                if (call.function.name == 'get_n_day_weather_forecast'):
                    return get_weather(arguments['location'], arguments['num_days'])
        
        return get_lang_value('not_understand')

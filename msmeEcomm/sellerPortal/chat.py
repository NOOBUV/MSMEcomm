import os
from dotenv import load_dotenv
import time
from requests.exceptions import RequestException

load_dotenv()
from groq import Groq


class chatBot:
    def __init__(self,message):
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        self.message = message
        print(self.chat_completion())

    def chat_completion(self, max_retries=3):
        print('hello')
        for attempt in range(max_retries):
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": self.message,
                        }
                    ],
                    model="llama3-8b-8192",
                )
                return chat_completion.choices[0].message.content
            except RequestException as e:
                print(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  
                else:
                    raise
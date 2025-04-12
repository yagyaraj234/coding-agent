import json
from openai import OpenAI
from prompt import USER_PROMPT_MODIFIED
from tools import run_command
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

messages = [{
    "role": "system",
    "content": USER_PROMPT_MODIFIED
}]

while True:

    user_input= input("> ")
    messages.append({
            "role": "user",
            "content": user_input
        })
    

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"}
    )

    output = json.loads(response.choices[0].message.content)
    print("Output:", output)
import json
from openai import OpenAI
from prompt import SYSTEM_PROMPT
from tools import run_command,get_file_content
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

available_tools = {
    "run_command":{
        "fn": run_command,
        "description": "Run a command in the shell",
    },
    "get_file_content":{
        "fn": get_file_content,
        "description": "Get the content of a file",
    }
 
}

messages = [{
    "role": "system",
    "content": SYSTEM_PROMPT
}]

user_input= input("> ")

messages.append({
        "role": "user",
        "content": user_input
    })

while True:
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"}
    )

    output = json.loads(response.choices[0].message.content)
    # print("Output:", output)
    messages.append({
        "role": "assistant",
        "content": json.dumps(output)
    })

    if(output.get("state") == "FINALIZE"):

        print("ai : ",output.get("output"))
        next_input = input("> ")
        messages.append({
                "role": "user",
                "content": json.dumps({"state":"START", "input": next_input})
            })
        continue
    
    if(output.get("state") == "ACT"):
        fn = output.get("tool")

        if fn in available_tools:
            tool = available_tools[fn]
            tool_fn = tool.get("fn")
            print("Tool function:", tool_fn)
            tool_input = output.get("input")  # Renamed from 'input' to 'tool_input'
            print("Input:", tool_input)
            command = tool_fn(tool_input)  # Use the renamed variable here
            messages.append({
                "role": "assistant",
                "content": json.dumps(command)
            })
            continue



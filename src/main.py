import json
from openai import OpenAI
from prompts import SYSTEM_PROMPT
from tools import run_command,edit_file,check_file_exists
from dotenv import load_dotenv

load_dotenv()



client = OpenAI()

available_tools = {
    "run_command":{
        "fn": run_command,
        "description": "Run a command in the shell",
    },
    "edit_file":{
        "fn": edit_file,
        "description": "Edit a file",
          },
    "check_file_exists":{
        "fn": check_file_exists,
       
    }
}


messages = [{
    "role": "system",
    "content": SYSTEM_PROMPT
}]



user_input= input(">")

while True:
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
    messages.append({
        "role": "assistant",
        "content": json.dumps(output)
    })


    if(output.get("state") == "FINALIZE"):
        print(" Is there anything else you would like me to do? (y/n)")
        next_input = input("Is there anything else you would like me to do? (y/n) ")
        if next_input.lower() == "y":
            user_input = input(">")
            messages.append({
                "role":"user",
                "content":user_input
            })
            continue
        else:
            print("Thank you for using the tool. Goodbye!")
            break

    if(output.get("state") == "ACT"):
        tool_name = output.get("fn")
        tool_input = output.get("input")
        tool_command = output.get("command")
        tool_file_name = output.get("file_name")
        tool_updated_content = output.get("updated_content")

        if tool_name in available_tools:
            tool = available_tools[tool_name]
            fn = tool["fn"]
            parameters = tool["parameters"]
            if "command" in parameters["required"]:
                fn(tool_command)
            if "file_name" in parameters["required"]:
                fn(tool_file_name)
            if "updated_content" in parameters["required"]:
                fn(tool_updated_content)
        else:
            print(f"Tool {tool_name} not found.")
            break
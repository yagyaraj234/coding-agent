import json
from openai import OpenAI
from prompts import SYSTEM_PROMPT
from tools import run_command,edit_file,check_file_exists



client = OpenAI()

available_tools = {
    "run_command":{
        fn:run_command,
        description:"Run a command in the shell",
        parameters:{
            "type":"object",
            "properties":{
                "command":{
                    "type":"string",
                    "description":"The command to run"
                },
                "path":{
                    "type":"string",
                    "description":"The path to run the command in"
                }
            },
            "required":["command"]
        }
    },
    "edit_file":{
        fn:edit_file,
        description:"Edit a file",
        parameters:{
            "type":"object",
            "properties":{
                "file_name":{
                    "type":"string",
                    "description":"The name of the file to edit"
                },
                "updated_content":{
                    "type":"string",
                    "description":"The updated content of the file"
                }
            },
            "required":["file_name","updated_content"]
        }
    },
    "check_file_exists":{
        fn:check_file_exists,
        description:"Check if a file exists",
        parameters:{
            "type":"object",
            "properties":{
                "file_name":{
                    "type":"string",
                    "description":"The name of the file to check"
                }
            },
            "required":["file_name"]
        }
    }
}


messages = [{
    role:"system",
    content:SYSTEM_PROMPT
}]





user_input= input(">")

while True:
    messages.append({
        role:"user",
        content:user_input
    })


    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={type:"json_object"}
    )

    output = json.loads(response.choices[0].message.content)
    messages.append({
        role:"assistant",
        content=json.dumps(output)
    })


    if(output.get("state") == "FINALIZE"):
        print(" Is there anything else you would like me to do? (y/n)")
        next_input = input("Is there anything else you would like me to do? (y/n) ")
        if next_input.lower() == "y":
            user_input = input(">")
            messages.append({
                role:"user",
                content=user_input
            })
            continue
        else:
            print("Thank you for using the tool. Goodbye!")
            break

    
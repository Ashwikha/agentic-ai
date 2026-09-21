import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import (
    student_tool,
    drive_tool,
    eligibility_tool
)

from prompts import SYSTEM_PROMPT


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

print("Groq API key loaded:", bool(os.getenv("GROQ_API_KEY")))


# --------------------------------------------------
# 2. Create Groq client
# --------------------------------------------------

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# --------------------------------------------------
# 3. Define tools
# --------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "name": "student_tool",
        "description": "Get student information using roll number.",
        "parameters": {
            "type": "object",
            "properties": {
                "roll_no": {
                    "type": "string",
                    "description": "Student roll number"
                }
            },
            "required": ["roll_no"]
        }
    },

    {
        "type": "function",
        "name": "drive_tool",
        "description": "Get placement drive information using company name.",
        "parameters": {
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "Company name"
                }
            },
            "required": ["company_name"]
        }
    },

    {
        "type": "function",
        "name": "eligibility_tool",
        "description": "Get eligibility rules using drive ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "drive_id": {
                    "type": "integer",
                    "description": "Placement drive ID"
                }
            },
            "required": ["drive_id"]
        }
    }
]


# --------------------------------------------------
# 4. Execute tools
# --------------------------------------------------

def execute_tool(name, arguments):

    if name == "student_tool":
        return student_tool(**arguments)

    elif name == "drive_tool":
        return drive_tool(**arguments)

    elif name == "eligibility_tool":
        return eligibility_tool(**arguments)

    else:
        return {
            "error": f"Unknown tool: {name}"
        }


# --------------------------------------------------
# 5. Agent loop
# --------------------------------------------------

def run_agent(user_message):

    # First request to the LLM
    response = client.responses.create(
        model="openai/gpt-oss-20b",
        instructions=SYSTEM_PROMPT,
        input=user_message,
        tools=TOOLS
    )

    while True:

        tool_called = False

        # Check everything returned by the model
        for item in response.output:

            # ------------------------------------------
            # Model wants to call a tool
            # ------------------------------------------

            if item.type == "function_call":

                tool_called = True

                name = item.name
                arguments = json.loads(item.arguments)

                print(f"\nTool called: {name}")
                print(f"Arguments: {arguments}")

                # Execute Python function
                result = execute_tool(
                    name,
                    arguments
                )

                print(f"Tool result: {result}")

                # --------------------------------------
                # Send tool result back to the model
                # --------------------------------------

                response = client.responses.create(
                    model="openai/gpt-oss-20b",
                    instructions=SYSTEM_PROMPT,
                    input=[
                        {
                            "role": "user",
                            "content": user_message
                        },
                        *response.output,
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(result)
                        }
                    ],
                    tools=TOOLS
                )

                break

        # ----------------------------------------------
        # No more tools → final answer
        # ----------------------------------------------

        if not tool_called:
            return response.output_text


# --------------------------------------------------
# 6. Main program
# --------------------------------------------------

if __name__ == "__main__":

    print("Placement Agent")
    print("Type 'exit' to quit.")

    while True:

        user_message = input("\nYou: ")

        if user_message.lower() == "exit":
            break

        try:

            answer = run_agent(user_message)

            print("\nAgent:", answer)

        except Exception as e:

            print("\nError:", e)
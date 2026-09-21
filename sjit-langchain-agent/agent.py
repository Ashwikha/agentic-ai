import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

from tools import (
    get_student_info,
    get_student_marks,
    calculator,
    get_passing_rules
)

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)


tools = [
    get_student_info,
    get_student_marks,
    calculator,
    get_passing_rules
]


agent = create_agent(
    model=llm,
    tools=tools
)


def ask_agent(question):
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    return result["messages"][-1].content


if __name__ == "__main__":
    question = input("Ask your question: ")

    answer = ask_agent(question)

    print("\nAgent:")
    print(answer)
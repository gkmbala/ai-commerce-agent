import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .tools import (
    search_products,
    check_inventory,
    add_to_cart,
)

from .rag import search_knowledge


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_products",
                description="Search photography products using customer requirements.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "query": types.Schema(
                            type=types.Type.STRING,
                            description="Search keywords such as portable flash, wedding, Godox."
                        ),
                        "max_price": types.Schema(
                            type=types.Type.NUMBER,
                            description="Maximum price in GBP."
                        ),
                        "category": types.Schema(
                            type=types.Type.STRING,
                            description="Product category."
                        ),
                        "use_case": types.Schema(
                            type=types.Type.STRING,
                            description="Photography use case."
                        ),
                    },
                    required=[
                        "query",
                        "max_price",
                        "category",
                        "use_case",
                    ],
                ),
            ),

            types.FunctionDeclaration(
                name="check_inventory",
                description="Check current demo inventory for a product.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "product_id": types.Schema(
                            type=types.Type.INTEGER
                        )
                    },
                    required=["product_id"],
                ),
            ),

            types.FunctionDeclaration(
                name="add_to_cart",
                description="Add a product to the demo shopping cart.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "product_id": types.Schema(
                            type=types.Type.INTEGER
                        ),
                        "quantity": types.Schema(
                            type=types.Type.INTEGER
                        ),
                    },
                    required=[
                        "product_id",
                        "quantity",
                    ],
                ),
            ),
        ]
    )
]


def execute_tool(name, arguments):

    if name == "search_products":
        return search_products(**arguments)

    if name == "check_inventory":
        return check_inventory(**arguments)

    if name == "add_to_cart":
        return add_to_cart(**arguments)

    return {
        "error": f"Unknown tool: {name}"
    }


def run_agent(user_message: str):

    knowledge = search_knowledge(user_message)

    context = "\n".join(
        f"{item['title']}: {item['content']}"
        for item in knowledge
    )

    instructions = f"""
You are SmartShop Agent.

You are an Agentic Commerce assistant for a photography
equipment store.

You can:

1. Search products
2. Check inventory
3. Add products to cart

Use tools whenever the customer asks about:

- products
- prices
- recommendations
- availability
- stock
- adding products to cart

Use the retrieved knowledge below for product,
delivery and policy information.

Retrieved knowledge:

{context}

Important rules:

- Never invent product information.
- Never invent inventory.
- Never claim a product was added unless add_to_cart succeeds.
- Product prices and stock are DEMO data.
- Give practical photography recommendations.
"""

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.7-flash"
    )

    # Keep the complete conversation history.
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=user_message
                )
            ]
        )
    ]

    while True:

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=instructions,
                tools=TOOLS,
            ),
        )

        # Add Gemini's complete response to the history.
        contents.append(
            response.candidates[0].content
        )

        function_calls = []

        for part in response.candidates[0].content.parts:

            if part.function_call:
                function_calls.append(
                    part.function_call
                )

        # No tool call means Gemini has produced
        # the final answer.
        if not function_calls:
            return response.text

        # Execute every requested function.
        function_response_parts = []

        for function_call in function_calls:

            name = function_call.name

            arguments = dict(
                function_call.args
            )

            result = execute_tool(
                name,
                arguments
            )

            print(
                f"TOOL CALL: {name}"
            )

            print(
                f"ARGUMENTS: {arguments}"
            )

            print(
                f"RESULT: {result}"
            )

            function_response_parts.append(
                types.Part.from_function_response(
                    name=name,
                    response={
                        "result": result
                    }
                )
            )

        # Function responses must be the next user turn.
        contents.append(
            types.Content(
                role="user",
                parts=function_response_parts
            )
        )
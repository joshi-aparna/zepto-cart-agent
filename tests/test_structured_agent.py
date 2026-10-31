from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
import os
from langchain.tools import tool
from shopping_agent_models import ShoppingItems

@tool
def view_cart() -> str:
    """Retrieve the shopping cart."""
    return "Cart contains 2 items. 1. Aashirvaad Soya Chunks - ₹38 (Qty: 1)\n2. Nandini Fresh Paneer (Pouch) - ₹96 (Qty: 1)\n'"

@tool
def another_dummy_tool() -> str:
    """Return a test message."""
    return "This is a dummy tool response."

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:30b")
model = ChatOllama(
    model=MODEL_NAME,
    temperature=0,
)

agent = create_agent(
    model=model,
    tools=[view_cart, another_dummy_tool],
    response_format=ToolStrategy(
        ShoppingItems,
        handle_errors=True,
    ),
    system_prompt = """
        You are a shopping assistant.

        You MUST:
        1. Call view_cart to retrieve the cart.
        2. After receiving its result, call the ShoppingItems
        structured output tool.
        3. Include every cart item in the structured response.
        """
)

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": (
                "view_cart to find all items in the cart."
            ),
        }
    ]
})

print("Messages:")
for i, message in enumerate(result["messages"]):
    print(f"\n--- Message {i}: {type(message).__name__} ---")
    print("Content:", repr(message.content))
    print("Tool calls:", getattr(message, "tool_calls", None))
    print("Invalid tool calls:", getattr(message, "invalid_tool_calls", None))
    print("Additional kwargs:", message.additional_kwargs)
    print("Response metadata:", message.response_metadata)

print("\nStructured response:")
print(repr(result.get("structured_response")))
from pydantic import BaseModel
from langchain_ollama import ChatOllama
import os

from shopping_agent_models import ShoppingItems


MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:30b")
model = ChatOllama(
    model=MODEL_NAME,
    temperature=0,
)

structured_model = model.with_structured_output(
    ShoppingItems,
    method="json_schema",
)

result = structured_model.invoke(
    "Cart contains 2 items. 1. Aashirvaad Soya Chunks - ₹38 (Qty: 1)\n   pvid: 99bb7937-2648-40cc-872a-ae80500968ff, spid: 9f0593b4-104b-5180-b8ea-0b3377d9cdef\n2. Nandini Fresh Paneer (Pouch) - ₹96 (Qty: 1)\n   pvid: be889ba2-ef6e-4e34-a40c-b979419d82cc, spid: b4a6e98b-2e2a-4e2a-8572-7494f8b8fad6', 'id': 'lc_9607ccd6-e5aa-41b4-8328-2910806ece06' "
    "Return structured response for cart contents"
)

print(result)
print(type(result))
print("result.items: " + str(result.items))
print("items count: " + str(len(result.items)))
if len(result.items) > 0:
    print("First item: " + str(result.items[0]))
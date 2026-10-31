# Zepto Cart Agent

An LLM-powered shopping cart agent that interacts with Zepto through its MCP server.

This project explores building a practical AI agent using local LLMs, LangChain and Model Context Protocol (MCP). The agent translates structured shopping requests into actions on a real shopping cart.

## What it does

The Zepto agent currently supports:

- **Add items:** Search for products and add matching products to the Zepto cart.
- **View cart:** Retrieve the current cart contents.
- **Cart value:** Retrieve the cart's current value.
- **Clear cart:** Remove items from the cart.

The agent does not place orders or make payments. It only manages the shopping cart.

## Architecture

The agent uses LangChain to orchestrate an LLM with tools exposed by Zepto's remote MCP server.

```text
User Request
     |
     v
Message Interpreter
     |
     v
ShoppingItems (structured output)
     |
     v
Command Router
     |
     +---- cartadd
     |        |
     |        v
     |    Zepto Agent
     |        |
     |        v
     |    LangChain Agent
     |        |
     |        v
     |    Zepto MCP Server
     |
     +---- listadd
              |
              v
          Notion
```

The message interpreter is responsible for understanding the user's intent and producing structured shopping items. The command router decides where those items should go.

The Zepto agent handles cart operations independently.

## Technology

- **Python** – Agent implementation.
- **Ollama** – Runs the local LLM.
- **LangChain / LangGraph** – Agent orchestration and tool execution.
- **Model Context Protocol (MCP)** – Integration with Zepto's tools.
- **Pydantic** – Structured input and output models.
- **Authlib / Cryptography** – OAuth authentication and encrypted token storage.

## Design decisions

Some of the interesting engineering decisions explored in this project:

### 1. Don't expose every MCP tool to the LLM

An MCP server can expose many tools, but that doesn't mean an agent should have access to all of them.

The agent uses a curated set of tools relevant to its responsibilities.

### 2. Treat tool descriptions and results carefully

Tool descriptions can contain instructions that influence model behaviour. Tool responses can also contain text that looks like instructions.

The agent needs clear boundaries between system instructions, tool metadata, tool results and user intent.

### 3. Use structured responses

The agent uses Pydantic models to represent operation results instead of relying entirely on conversational text.

This makes it easier for the calling application to consume results reliably.

### 4. Keep the agent's responsibilities narrow

The Zepto agent manages the cart. It does not interpret the entire shopping workflow, manage shopping lists or place orders.

Those responsibilities belong to other components.

## Development

This is an experimental project for exploring local LLM agents, MCP integrations, structured outputs and tool orchestration.

The implementation and architecture are evolving as new patterns and limitations are explored.

## Scope and limitations

- Cart management only.
- Requires Zepto MCP authentication.
- Requires a locally running Ollama instance.
- Product matching and tool execution depend on the underlying Zepto MCP implementation.
- No checkout, order placement or payment functionality.

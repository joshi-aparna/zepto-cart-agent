
### Overall architecture

Telegram Message
      |
      v
Message Interpreter
  ├── command: listadd | cartadd
  └── items: ShoppingItem[]
      |
      v
Command Router
  |
  +── listadd
  |     └── Write items to Notion
  |           └── Return result
  |
  +── cartadd
        |
        +── Zepto agent
        |     ├── cartadd(items)
        |     ├── view_cart()
        |     └── cartvalue()
        |     └── clearcart()
        |
        +── Blinkit agent
        |
        +── Swiggy agent
              |
              v
        Wait for all results
              |
              v
        Return combined cart
        statuses and values
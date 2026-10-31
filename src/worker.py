from shopping_agent_models import (
    ShoppingItems,
    ShoppingAgent,
    CartAddResult,
    CartValue,
    ClearCartResult,
    ShoppingOperation,
)
import asyncio
from agent import handle_request


class ZeptoAgent:

    async def cartadd(
        self,
        items: ShoppingItems
    ) -> list[CartAddResult]:

        results = []

        for item in items.items:
            text = f"Add {item.quantity or 1}"
            if item.unit:
                text += f" {item.unit}"
            text += f" of {item.item} to my cart."

            try:
                result = await handle_request(ShoppingOperation.CART_ADD, text)
                results.append(
                    CartAddResult(
                        item=item.item,
                        success=True,
                        message=str(result),
                    )
                )
            except Exception as exc:
                results.append(
                    CartAddResult(
                        item=item.item,
                        success=False,
                        message=str(exc),
                    )
                )

        return results

    async def view_cart(self) -> ShoppingItems:
        result = await handle_request(ShoppingOperation.VIEW_CART, "", ShoppingItems)
        return result

    async def cartvalue(self) -> CartValue:
        result = await handle_request(ShoppingOperation.CART_VALUE, "Using response from get_payment_methods tool, you MUST invoke the structured response tool and Return structured response containing total order value and count of items.", CartValue)
        return result

    async def clear_cart(self) -> ClearCartResult:
        try:
            result = await handle_request(
                ShoppingOperation.CLEAR_CART,
                "Remove every item from my current cart.View the cart first, keep count of items, remove each item, then verify the cart is empty.",
                ClearCartResult
            )
            return result
        except Exception as exc:
            return ClearCartResult(
                success=False,
                items_removed=0,
                message=str(exc),
            )

zepto_agent: ShoppingAgent = ZeptoAgent()

if __name__ == "__main__":
    command = input("Command (add to cart,view cart, clear cart,cart value): \n")
    command = command.strip().lower()
    command = "view cart" if command.startswith("view") else "add to cart" if command.startswith("add") else "clear cart" if command.startswith("clear") else "cart value" if command.startswith("cart value") else "unknown"
    request = input("Message: \n")
    response_model = ShoppingItems if command in ("view cart", "add to cart") else ClearCartResult if command == "clear cart" else CartValue if command == "cart value" else None
    if command == "add to cart":
        items = ShoppingItems.parse_raw(request)
        results = asyncio.run(zepto_agent.cartadd(items))
        print(results)
    elif command == "view cart":
        result = asyncio.run(zepto_agent.view_cart())
        print(result)
    elif command == "clear cart":
        result = asyncio.run(zepto_agent.clear_cart())
        print(result)
    elif command == "cart value":
        result = asyncio.run(zepto_agent.cartvalue())
        print(result)
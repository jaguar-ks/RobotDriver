import asyncio
from fastapi import FastAPI, Query
from SauceDemo import SauceDemoAutomation


app = FastAPI(title="SauceDemo automation API")

@app.get("/run")
async def run_automation(product: str = Query(..., description="Product name to search")):
    automator = SauceDemoAutomation(headless=True)

    # ✅ Correctly await the coroutine
    try:
        price = await automator.run(product)

        if price:
            return {
                'status': '✅ Success!',
                'product': product,
                'price': price
                }
        else:
            return {
                'status': f'❌ Failed!: product ({product}) not found.'
                    }
    except Exception as e:
        return {
            'status': f"Error: {e}"
        }


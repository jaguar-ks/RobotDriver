from fastapi import FastAPI, Query, Response, status
from SauceDemo import SauceDemoAutomation
from typing import Any, Dict

app = FastAPI(
    title="SauceDemo automation API",
    docs_url="/docs",
    description="""An API service that uses Playwright to log
    into SauceDemo.com and retrieve product prices.""",
    version='1.0.0'
)


@app.get(
    "/run",
    response_model=Dict[str, Any],
    summary="Execute product search automation"
)
async def run_automation(
    response: Response,
    product: str = Query(
        ...,
        description="""The exact name of the product to search for after
        successful login (e.g., 'Sauce Labs Backpack')."""
    )
) -> Dict[str, Any]:
    """
    Executes the SauceDemo automation workflow.

    The service launches a browser, logs in as the standard user, searches the
    inventory page for the specified product name, and returns its price.

    param product: The name of the product to locate. This parameter
    is required.
    return: A JSON dictionary indicating the status, the product name,
    and the price (if found).
    """

    automator = SauceDemoAutomation(headless=True)
    try:
        price: str | None = await automator.run(product)

        if price:
            return {
                'status': 'success',
                'details': f'✅ Product ({product}) found! with price: {price}'
                }
        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {
                'status': 'Error',
                'details': f'❌ Failed!: product ({product}) not found.'
                }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            'status': "Error",
            'detail': f"❌ Error occurred: {e.__class__.__name__}: {e}"
        }

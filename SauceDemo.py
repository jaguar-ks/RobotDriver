import asyncio
from playwright.async_api import async_playwright, Browser, Page, expect


class SauceDemoAutomation:
    """
    Automates the process of logging into the SauceDemo website and searching
    for a specific product using Playwright.

    This class encapsulates the browser lifecycle (launch and close)
    and the core automation steps (login and search).
    """

    BASE_URL = "https://www.saucedemo.com/"
    USERNAME = "standard_user"
    PASSWORD = "secret_sauce"

    def __init__(self, headless: bool = True):
        """
        Initializes the SauceDemoAutomation instance.

        :param headless: Whether to run the browser in headless mode.
                         Defaults to True (no UI visible).
        :type headless: bool
        """

        self.headless = headless
        self.__browser: Browser | None = None
        self.__page: Page | None = None

    async def login(self) -> None:
        """
        Navigates to the base URL, fills in the standard user credentials,
        clicks the login button, and waits for the 'Products' heading to appear.

        :raises RuntimeError: If any step of the login process fails (e.g., navigation,
                              element interaction, or the 'Products' heading doesn't appear).
        """

        try:
            await self.__page.goto(self.BASE_URL)
            await self.__page.get_by_role("textbox", name="UserName").fill(self.USERNAME)
            await self.__page.get_by_role("textbox", name="Password").fill(self.PASSWORD)
            await self.__page.get_by_role("button", name="Login").click()
            await expect(self.__page.locator("span", has_text="Products")).to_be_visible()
        except Exception as e:
            raise RuntimeError('LoginError ❌: login failed') from e

    async def find_product_details(self, product_name: str) -> str | None:
        """
        Searches the current inventory page for a product by name.

        It iterates through all product items on the page and returns the
        price text if a match is found.

        :param product_name: The exact name of the product to search for.
        :type product_name: str
        :returns: The price of the product as a string (e.g., '$29.99'),
                  or None if the product is not found.
        :rtype: str | None
        """

        products = await self.__page.query_selector_all(".inventory_item")
        for product in products:
            name = await product.query_selector(".inventory_item_name")
            price = await product.query_selector(".inventory_item_price")
            if name and (await name.text_content()) == product_name:
                return await price.text_content()
        return None

    async def run(self, product_to_search: str) -> str | None:
        """
        The main execution method. It handles the full automation workflow:
        1. Starts Playwright and launches the browser.
        2. Performs login.
        3. Searches for the specified product.
        4. Closes the browser and stops Playwright in a finally block.

        :param product_to_search: The name of the product to search for after logging in.
        :type product_to_search: str
        :returns: The price of the found product, or None if the search was unsuccessful.
        :rtype: str | None
        :raises RuntimeError: If any critical error occurs during setup or workflow execution.
        """

        p = await async_playwright().start()
        self.__browser = await p.chromium.launch(headless=self.headless)
        self.__page = await self.__browser.new_page()
        try:
            await self.login()
            return await self.find_product_details(product_to_search)
        except Exception as e:
            raise RuntimeError(f"Error accurred: {e}.") from e
        finally:
            if self.__browser:
                await self.__browser.close()
            await p.stop()


async def main():
    product = "Sauce Labs Backpack"
    automator = SauceDemoAutomation(headless=False)
    try:
        price = await automator.run(product)
        if price:
            print(f"✅ Success! product ({product}) find with price:{price}")
        else:
            print(f"❌Failed! product ({product}) not found.")
    except Exception as e:
        print(f"❌Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

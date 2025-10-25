import asyncio
from playwright.async_api import async_playwright, TimeoutError, Browser, Page, expect


class SauceDemoAutomation:
    """
    A simpler class to automate the SauceDemo workflow.
    It manages the browser lifecycle within a single 'run' method.
    """

    BASE_URL: str = "https://www.saucedemo.com/"
    USERNAME: str = "standard_user"
    PASSWORD: str = "secret_sauce"

    def __init__(self, headless: bool = True):
        """
        Initializes the class and sets the browser mode.
        """
        self.headless = headless
        self.__browser: Browser | None = None
        self.__page: Page | None = None

    async def login(self) -> None:
        """
        Navigates to the site, fills credentials, and logs in.
        """
        if not self.__page:
            raise RuntimeError("🛑 Page not initialized.")

        try:
            print("Opening the website...")
            await self.__page.goto(self.BASE_URL, timeout=15000)
            print("Logging in...")
            await self.__page.get_by_role("textbox", name='UserName').fill(self.USERNAME)
            await self.__page.get_by_role("textbox", name='Password').fill(self.PASSWORD)
            await self.__page.get_by_role('button', name='Login').click()
            await expect(self.__page.locator('span', has_text='Products')).to_be_visible(timeout=1500)
        except TimeoutError:
            raise RuntimeError("⚠️ Timeout during login process.")
        except Exception as e:
            raise RuntimeError(f"🛑 Cannot proceed with search: Login failed {e}.")

    async def find_product_details(self, product_name: str) -> str | None:
        """
        Searches for a product and returns its price.
        """
        if not self.__page:
            raise RuntimeError("Page not initialized.")

        print(f"Searching for '{product_name}'...")
        try:
            products = await self.__page.query_selector_all(".inventory_item")
            for product in products:
                name = await product.query_selector(".inventory_item_name")
                price = await product.query_selector(".inventory_item_price")

                if name and (await name.text_content()) == product_name:
                    return await price.text_content()
            return None
        except Exception as e:
            print(f"❌ Error during product search: {e}")
            return None

    async def run(self, product_to_search: str) -> None:
        """
        The main method that controls the entire automation sequence.
        It handles Playwright initialization and cleanup.
        """
        async with async_playwright() as p:
            try:
                print(f"Starting browser (headless={self.headless})...")
                self.__browser = await p.chromium.launch(headless=self.headless)
                self.__page = await self.__browser.new_page()

                await self.login()
                price = await self.find_product_details(product_to_search)
                if price:
                    print(f"✅ Success! Found '{product_to_search}' with price: {price}")
                else:
                    print(f"❌ Product '{product_to_search}' not found.")
            except Exception as e:
                print(f"❌ A critical error occurred: {e}")
            finally:
                if self.__browser:
                    print("Closing browser...")
                    await self.__browser.close()


async def main():
    product = "Sauce Labs Backpack"
    automator = SauceDemoAutomation(headless=False)
    await automator.run(product)


if __name__ == "__main__":
    asyncio.run(main())

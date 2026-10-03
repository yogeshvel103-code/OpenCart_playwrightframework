from playwright.sync_api import Page, Expect


class HomePage():


    def __init__(self, page):
        self.page=page
        self.lnk_my_account = page.locator('[title="My Account"]')
        self.lnk_register = page.locator('a[href*="account/register"]')
        self.lnk_login = page.locator('a:has-text("Login")')
        self.txt_search_box = page.locator('input[placeholder="Search"]')
        self.btn_search = page.locator('.input-group-btn button[type="button"]')  #   alternate #search button[type="button"]

    def get_home_page_title(self):
        """Return the title of the Home Page."""
        title = self.page.title()
        return title

    def click_my_account(self):
        """Click on the 'My Account' link."""
        try:
            self.lnk_my_account.click()
        except Exception as e:
            print(f" Exception while clicking 'My Account': {e}")
            raise

    def click_register(self):
        """Click on the 'Register' link under My Account."""
        try:
            self.lnk_register.click()
        except Exception as e:
            print(f" Exception while clicking 'Register': {e}")
            raise

    def click_login(self):
        """Click on the 'Login' link under My Account."""
        try:
            self.lnk_login.click()
        except Exception as e:
            print(f" Exception while clicking 'Login': {e}")
            raise

    def enter_product_name(self, product_name):
        """Enter the product name into the search input box."""
        try:
            self.txt_search_box.fill(product_name)
        except Exception as e:
            print(f" Exception while entering product name '{product_name}': {e}")
            raise

    def click_search(self):
        """Click on the search button to initiate the product search."""
        try:
            self.btn_search.click()
        except Exception as e:
            print(f" Exception while clicking 'Search' button: {e}")
            raise

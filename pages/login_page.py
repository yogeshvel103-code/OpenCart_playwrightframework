from playwright.sync_api import Page

class LoginPage:

   def __init__(self,page):
       self.page=page
       self.txt_email_address = page.locator('#input-email')
       self.txt_password = page.locator('#input-password')
       self.btn_login = page.locator('input[value="Login"]')

   def login(self, email: str, password: str):
       """
       Perform the complete login operation:
       1. Enter email
       2. Enter password
       3. Click the Login button
       """
       try:
           self.txt_email_address.fill(email)
           self.txt_password.fill(password)
           self.btn_login.click()
       except Exception as e:
           print(f"Exception during login: {e}")

           raise

   def get_login_error(self):
       return self.page.locator("div.alert:has-text('Warning: No match for E-Mail Address')")


from playwright.sync_api import Page,expect

from pages import registration_page
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from utilities.random_data_util import RandomDataUtil
import pytest

def test_registration_page(page):

    # --- Step 1: Create Page Object Instances ---
    home_page =HomePage(page)
    registration_page = RegistrationPage(page)

    # --- Step 2: Navigate to Registration Page ---
    home_page.click_my_account()
    home_page.click_register()
    random_data = RandomDataUtil()


    # --- Step 3: Generate Random Test Data ---
    # Using RandomDataUtil to generate random user details
    # --- Step 4: Fill Registration Form ---

    user_data = {
        "firstName": random_data.get_first_name(),
        "lastName": random_data.get_last_name(),
        "email": random_data.get_email(),
        "telephone": random_data.get_phone_number(),
        "password": random_data.get_password()
                }

    # --- Step 5: Accept Privacy Policy and Submit ---
    registration_page.set_privacy_policy()
    registration_page.click_continue()

    # --- Step 6: Verify Account Creation Confirmation ---
    confirmation_msg = registration_page.complete_registration(user_data)
    expect(confirmation_msg).to_have_text("Your Account Has Been Created!")

    """
    Test Case: User Registration Functionality

    ===========================================
    Test Steps
    ===========================================

    1. Open the application in the browser.
    2. Navigate to the "My Account" menu and click on "Register".
    3. Enter user details:
       - First Name
       - Last Name
       - Email
       - Telephone Number
       - Password and Confirm Password
    4. Accept the Privacy Policy checkbox.
    5. Click on the "Continue" button.
    6. Verify that the account creation confirmation message is displayed.

    Expected Result:
    ----------------
    After submitting valid details, the system should display the message:
    "Your Account Has Been Created!"
    """
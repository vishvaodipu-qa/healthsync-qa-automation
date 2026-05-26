from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AppointmentPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators for Healthcare Portal
    USERNAME_FIELD = (By.ID, "txt-username")
    PASSWORD_FIELD = (By.ID, "txt-password")
    LOGIN_BUTTON = (By.ID, "btn-login")
    BOOK_BUTTON = (By.ID, "btn-book-appointment")
    SUCCESS_MSG = (By.TAG_NAME, "h2")

    def login_to_portal(self, username, password):
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_FIELD)).send_keys(username)
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_FIELD)).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()

    def confirm_booking(self):
        self.wait.until(EC.element_to_be_clickable(self.BOOK_BUTTON)).click()

    def get_success_message(self):
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MSG)).text

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from page.appointment_page import AppointmentPage

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # Runs without UI in GitHub Actions pipeline
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get("https://katalon-demo-cura.herokuapp.com/")
    
    yield driver
    driver.quit()

def test_healthcare_appointment_booking(driver):
    appointment = AppointmentPage(driver)
    
    # Click Make Appointment Button on Homepage
    driver.find_element(By.ID, "btn-make-appointment").click()
    
    # Step 1: Login using Page Object Model
    appointment.login_to_portal("John Doe", "ThisIsNotAPassword")
    
    # Step 2: Book Appointment Slot
    appointment.confirm_booking()
    
    # Step 3: Verify Output (Zero Defect Validation)
    assert appointment.get_success_message() == "Appointment Confirmation", "Booking failed!"

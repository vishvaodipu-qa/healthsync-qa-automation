import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    # Chrome Options setup for GitHub Actions CI/CD headless execution
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)  # Max timeout fallback for elements
    yield driver
    driver.quit()

def test_healthcare_appointment_booking(driver):
    # 1. Navigate to the healthcare portal
    driver.get("https://katalon-demo-cura.herokuapp.com/")
    
    # 2. Click on 'Make Appointment' button
    driver.find_element(By.ID, "btn-make-appointment").click()
    
    # 3. Handle login authentication using demo credentials
    driver.find_element(By.ID, "txt-username").send_keys("John Doe")
    driver.find_element(By.ID, "txt-password").send_keys("ThisIsNotAPassword")
    driver.find_element(By.ID, "btn-login").click()
    
    # 4. Populate the Appointment Form fields
    # Select Facility dropdown option
    facility_dropdown = driver.find_element(By.ID, "combo_facility")
    facility_dropdown.find_element(By.XPATH, "//option[@value='Hongkong CURA Healthcare Center']").click()
    
    # Handle Checkbox and Radio buttons
    driver.find_element(By.ID, "chk_hospreadmission").click()
    driver.find_element(By.ID, "radio_program_medicaid").click()
    
    # Input Visit Date and Comments
    driver.find_element(By.ID, "txt_visit_date").send_keys("30/05/2026")
    driver.find_element(By.ID, "txt_comment").send_keys("Automated Healthcare QA Regression Test Booking.")
    
    # 5. Submit the appointment form
    driver.find_element(By.ID, "btn-book-appointment").click()
    
    # 6. Explicit Wait: Dynamically wait for the confirmation header to stabilize in DOM
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Confirmation')]"))
    )
    
    # Brief fallback sleep to ensure full text rendering under headless execution
    time.sleep(2)
    
    # 7. Final Validation assertion check
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Appointment Confirmation" in page_text, f"Assertion failed! Expected header not found. Current view: {page_text[:100]}"

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# !! IMPORTANT !! Please switch out this path for the path leading
#  to your Chrome driver.
driver_path = "/Users/Cary/Desktop/seleniumtest/chromedriver";

def init_driver():
    # Chrome is the browser driver for this test. Load the line below with
    # another browser driver, if desired
    driver = webdriver.Chrome(driver_path)
    driver.wait = WebDriverWait(driver, 5)
    return driver

def add_products_to_cart():
    try:
        # Adds 5 Health + Ancestry items to the cart
        for i in range(0, 5):
            button = driver.wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "js-add-kit")))
            # Wait for loading overlay to disappear
            driver.wait.until(EC.invisibility_of_element_located((By.ID, "loading-overlay")))
            button.click()
        name = driver.wait.until(EC.presence_of_element_located((By.NAME, "name")))
        driver.wait.until(EC.invisibility_of_element_located((By.ID, "loading-overlay")))
        boxes = driver.find_elements_by_class_name("js-kit-name")
        names = ['Bill Nye', 'Rob Nye', 'Cary Nye', 'Rachel Nye', 'Cindy Nye']
        for idx, box in enumerate(boxes):
            assert box.get_attribute("name") == "name"
            box.send_keys(names[idx])

        # Wait for the greyed-out button to become green
        driver.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "button-disabled")))
        button = driver.find_element_by_class_name("button-continue")
        assert button.get_attribute("value") == "continue"
        button.click()
    except TimeoutException:
        print("There was an error while adding products to the cart. Try running the test again.")

def confirm_payment_page():
    try:
        # if we see an element with the class 'payment-total', we can confirm we've reached the pmt page
        classname = "payment-total"
        driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
        print("Verification Complete: Payment page reached.")
    except TimeoutException:
        print("Could not locate the element with the '{}' class. Payment page verification failed.").format(classname)

def enter_shipping_info():
    try:
        driver.wait.until(EC.presence_of_element_located((By.ID,"id_first_name")))
        input_data = ['Bill', 'Nye', '23AndMe', '1010 Bush St', 'Suite A', 'San Francisco', 94109, 'fake@fake.com']

        name_fields = {
            'first_name': 'Bill',
            'last_name':'Nye',
            'company': '23AndMe',
            'address': '1010 Bush St',
            'address2': 'Suite A',
            'city': 'San Francisco',
            'postal_code': 94109,
            'email': 'fake@fake.com',
        }


        # Begin selecting input boxes but their name attributes and entering input data

        for idx, key in enumerate(name_fields):
            box = driver.find_element_by_name(key)
            box.send_keys(name_fields[key])

        driver.find_element_by_xpath("//select[@id='id_state']/option[text()='California']").click()
        driver.find_element_by_xpath("//select[@id='id_country']/option[text()='United States']").click()

        id_int_phone = driver.find_element_by_id("id_int_phone")
        id_int_phone.send_keys("(714) 333-3333")

        # Wait for greyed-out button to disappear
        driver.wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "button-disabled")))
        button = driver.find_element_by_class_name("button-continue")
        assert button.get_attribute("value") == "continue"
        button.click()
    except TimeoutException:
        print("There was an error processing the order on the shipping page.")

def run_test(driver, query):
    # Runs entire test. Opens up browser, visits site, and initiates helper fns
    site = "http://store.23andme.com/en-us/"
    driver.get(site)
    assert "23andMe" in driver.title, "Invalid URL. This is a test for the 23andMe store."
    try:
        add_products_to_cart()

        enter_shipping_info()

        verify_address()

        confirm_payment_page()

    except TimeoutException:
        print("There was an error processing the order on {}".format(site))

def verify_address():
    try:
        # if verified address is available, select that. Otherwise, go with unverified
        verified = driver.wait.until(EC.presence_of_element_located((By.NAME, "verified")))
        if verified:
            verified.click()
        else:
            driver.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button-continue")))
            unverified = driver.find_element_by_xpath("//input[@value='ship to unverified address']")
            unverified.click()

    except TimeoutException:
        print("There was an error while verifying the address.")


if __name__ == "__main__":
    driver = init_driver()
    run_test(driver, "Selenium")
    time.sleep(5)
    driver.quit()

# selenium_python_test

This general purpose test is designed to verify that the 23andMe Store is functioning correctly and allows a customer to reach the payment page as intended. The test will select 3 Health & Ancestry products and 2 Ancestry products to add to the cart and proceed to the next page to enter in shipping information. The customer then moves from the shipping information page to the verification page to confirm the verified address. Lastly, the customer arrives at the payment page to enter in credit card information.

## Dependencies
    1. Python 3 (This script was written with Python 3 syntax, so it will not run correctly with Python 2)
    2. Selenium (The easiest way to install Selenium is by running 'pip install -U selenium' in the terminal)
    3. Chrome Driver (Included)

## To Run:
    1. Navigate to the directory containing the file 'selenium_script.py'
    2. In terminal, type the following and hit enter: python selenium_script.py
    
## Results
    Upon execution, the chrome browser will launch and run it's automated tasks. If the test finds any errors, it will print them in the terminal. Likewise, at the end of the test, a success message will appear letting you know that he test has completed successfully.



"""Import and install appropriate modules below."""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

"""Need to install the appropriate browser driver and place .exe in accessible file."""
# Chrome driver path should reference the .exe browser driver.
chrome_driver_path = "NEED TO ADD YOUR OWN PATH TO YOUR BROWSER EXE DRIVER"

# Access the driver
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# Open the website.  In this case cookie clicker.
driver.get(url="https://orteil.dashnet.org/cookieclicker/")

# Sleep for 5 seconds to allow the language bar to pop up.
time.sleep(3)

# Click on english language button in the list.  Can change the XPATH to another language if desired.
english = driver.find_element(By.XPATH, "//*[@id='langSelect-EN']")
english.click()

# Sleep for another 5 seconds for game to load.
time.sleep(3)

# Set initial click for items in store (seconds).
amount_of_time_check_store = 1
timeout = time.time() + amount_of_time_check_store

cookies = True
# While statement to continuously loop through clicking the cookie and checking the store.
while cookies:
    # Locate the cookie element and click it.
    driver.find_element(By.XPATH, "//*[@id='bigCookie']").click()
# Check to see if the time between store checking has passed the set amount.
    if time.time() > timeout:
        # Find all the prices for items in the store.
        all_prices = driver.find_elements(By.CLASS_NAME, "price")
        # Designate empty list to add items from search above to.
        price_list = []
        # Loop through all the items above and add them to the empty price list.
        for x in all_prices:
            price_list.append(x.text)
        # Remove items in the list that have no corresponding value.
        rev_list = [n for n in price_list if n != ""]
        # New empty list to add actual price numbers to.
        r_list = []
        # Loop rev_list to remove symbols, remove text, and changes them to floats.
        for t in rev_list:
            # Any item located in the list above that is under 8 characters will be under a million dollars.
            # This means the numbers will only be separated by commas.  Statement below will remove all commas
            # and change string to float and add to r_list.  The website starts adding items to the store in decimal
            # increments.  Everything has been converted to a float to keep it simpler."""
            if len(t) < 8:
                r_list.append(float(t.replace(",", "")))
            # Any item located in the list that has a length greater than 7 characters is greater than a million.
            # The else statement below includes sub-statements that will remove the text and multiply by the appropriate
            # integer.  Last it will do is change it to a float and add it to the rev_list.
            else:
                n = t.split()
                if n[1].lower() == "million":
                    r_list.append(float(n[0]) * 1000000)
                elif n[1].lower() == "billion":
                    r_list.append(float(n[0]) * 1000000000)
                elif n[1].lower() == "trillion":
                    r_list.append(float(n[0]) * 1000000000000)
                elif n[1].lower() == "quadrillion":
                    r_list.append(float(n[0]) * 1000000000000000)
        # This obtains the min priced item in rev_list or what is in the store.
        min_price = min(r_list)
        # This obtains the index number of that item in the store.  This can be plugged back into the XPATH below to
        # obtain the correct item and click it.
        index_num = r_list.index(min_price)
        # This obtains the current amount of cookies the player has at this time.
        current_cookies = driver.find_element(By.XPATH, "//*[@id='cookies']").text
        # The variable above includes multiple elements not needed.  The statement below creates a list of all the
        # elements and keeps only the first one which is always the current amount of cookies.
        cooks = current_cookies.split()[0]
        # This removes the commas and changes the number to a float.
        available_cookies = float(cooks.replace(",", ""))
        # Statement below clicks the appropriate store item available based on the index number given above if one
        # the lowest priced item is less than available cookies.
        if available_cookies > min_price:
            driver.find_element(By.XPATH, f"//*[@id='product{index_num}']").click()
        # Passes if not enough cookies are available for any of the items in the store.
        else:
            pass
        # Set time between checking the store (seconds)
        timeout = time.time() + amount_of_time_check_store
    # Pass through statement if the allotted time hasn't occurred yet.
    else:
        pass

import time
import traceback

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

def scrape(driver):
    try:
        # Load SabongLive618 page
        load_sabong_live_618_page(driver, "https://sl618.net")
        
        # Load Barako Betting page
        load_barako_betting_page(driver, "https://barako-bet.netlify.app")

        while True:            
            # Wait until the new match will be opened
            WebDriverWait(driver, 1200).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "td.bettingStatus"), 'OPEN')
            )

            # Get match name
            match_name = driver.find_element_by_css_selector("h3.hero-unit__subtitle.text-primary").text
            print("Match Name: " + match_name)

            # Get match number
            match_number = driver.find_element_by_css_selector("h5.fightNoDisplay").text
            print("Match Number: " + match_number)

            # Input new open match
            input_new_match(driver, match_name, match_number)
            
            # Wait until the match is checking for last call
            WebDriverWait(driver, 1200).until(
                EC.text_to_be_present_in_element((By.ID, "announcement-holder"), 'LAST CALL - FIGHT # ' + match_number)
            )
            # LAST CALL - FIGHT #
            print(driver.find_element_by_id("announcement-holder").text)
            process_credits(driver, "LAST CALL")

            # Wait until the match status will be closed
            WebDriverWait(driver, 1200).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, "td.bettingStatus"), 'CLOSED')
            )
            print("Match # " + match_number + " is now closed.")
            process_credits(driver, "CLOSE")

            while True:
                # Check if the match result is CANCELLED
                try:
                    WebDriverWait(driver, 0.5).until(
                        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h3.meron-bg > small.winner-indicator", "h3.meron-bg > small.cancel-indicator"), 'CANCELLED')
                    )
                    print("Match # " + match_number + " - " + 'CANCELLED')
                    process_credits(driver, 'CANCEL')
                    break
                except:
                    pass

                # Check if the match result is MERON
                try:
                    WebDriverWait(driver, 0.5).until(
                        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h3.meron-bg > small.winner-indicator"), 'WINNER')
                    )
                    print("Match # " + match_number + " - " + 'MERON')
                    process_credits(driver, 'MERON')
                    break
                except:
                    pass

                # Check if the match result is WALA
                try:
                    WebDriverWait(driver, 0.5).until(
                        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h3.wala-bg > small.winner-indicator"), 'WINNER')
                    )
                    print("Match # " + match_number + " - " + 'WALA')
                    process_credits(driver, 'WALA')
                    break
                except:
                    pass

                # Check if the match result is DRAW
                try:
                    WebDriverWait(driver, 0.5).until(
                        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "h3.meron-bg > small.winner-indicator"), 'DRAW')
                    )
                    print("Match # " + match_number + " - " + 'DRAW')
                    process_credits(driver, 'DRAW')
                    break
                except:
                    pass

            print("------------------------------")
    except:
        print(traceback.format_exc())
    finally:
        driver.quit()

def load_sabong_live_618_page(driver, url):
    # Load primary tab for SabongLive618 page
    driver.get(url)
    # Open new tab for SabongLive618 page to bypass the Cloudflare protection for the primary tab
    driver.execute_script("window.open('" + url + "', '_blank');")
    
    # Wait until the SabongLive618 login page will be loaded
    WebDriverWait(driver, 1200).until(
        EC.presence_of_element_located((By.XPATH, "//body[@data-template='template-basketball']"))
    )
    
    # Close the other SabongLive618 tab
    driver.switch_to.window(driver.window_handles[1])
    driver.close()

    # Switch to the primary tab of SabongLive618
    driver.switch_to.window(driver.window_handles[0])

    time.sleep(5)

    # Input user credentials
    username_input = driver.find_element_by_name('username')
    username_input.send_keys('rferrer')
    password_input = driver.find_element_by_name('password')
    password_input.send_keys('fighterMaster95')
    driver.find_element_by_xpath('//button[normalize-space()="Sign in to your account"]').click()
    
    # Wait until the SabongLive618 dashboard page will be loaded
    WebDriverWait(driver, 1200).until(
        EC.presence_of_element_located((By.ID, "betting-dashboard"))
    )

    time.sleep(5)

def load_barako_betting_page(driver, url):
    # Open new tab for Barako Bet page
    driver.execute_script("window.open('" + url + "', '_blank');")
    driver.switch_to.window(driver.window_handles[1])

    # Wait until the Barako Betting login page will be loaded
    WebDriverWait(driver, 1200).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='login-container']"))
    )

    time.sleep(5)

    # Input user credentials
    email_input = driver.find_element_by_xpath('//input[@placeholder="Email"]')
    email_input.send_keys('web_admin@yopmail.com')
    password_input = driver.find_element_by_xpath('//input[@placeholder="Password"]')
    password_input.send_keys('P@ssw0rd')
    driver.find_element_by_xpath('//button[normalize-space()="Login"]').click()

    # Wait until the Barako Betting page will be loaded
    WebDriverWait(driver, 1200).until(
        EC.text_to_be_present_in_element((By.XPATH, "//div[@class='site-layout-background']"), 'Welcome To Barako Betting')
    )

    time.sleep(5)

    # Get menu items in the Barako Betting page
    side_menus = driver.find_elements_by_css_selector('ul.ant-menu > li.ant-menu-item')

    # Proceed to 'Manage Matches' menu item
    for menu in side_menus:
        if menu.text == "MANAGE MATCHES":
            menu.click()
            break

    # Hover match category dropdown
    match_category = driver.find_element_by_css_selector('ul.ant-menu > p.ant-dropdown-trigger')
    hover = ActionChains(driver).move_to_element(match_category)
    hover.perform()

    time.sleep(3)

    # Get dropdown menu items of match category
    match_category_menus = driver.find_elements_by_css_selector('ul.ant-dropdown-menu > li.ant-dropdown-menu-item')

    # Proceed to 'WPC' dropdown menu item
    for menu in match_category_menus:
        if menu.text == "WPC":
            menu.click()
            break

    time.sleep(3)

    # Switch back to the primary tab of SabongLive618
    driver.switch_to.window(driver.window_handles[0])

def input_new_match(driver, match_name, match_number):
    # Switch to the Barako Betting tab
    driver.switch_to.window(driver.window_handles[1])

    # Input match details
    match_name_input = driver.find_element_by_xpath('//input[@placeholder="Match Name"]')
    match_name_input.send_keys(match_name)
    match_number_input = driver.find_element_by_xpath('//input[@placeholder="Match Number"]')
    match_number_input.send_keys(match_number)
    driver.find_element_by_xpath('//button[normalize-space()="NEW MATCH"]').click()    
    time.sleep(3)
    driver.find_element_by_xpath('//button[normalize-space()="Yes"]').click()
    time.sleep(3)
    print("New Match # " + match_number + " is now open.")

    # Switch back to the primary tab of SabongLive618
    driver.switch_to.window(driver.window_handles[0])

def process_credits(driver, status):
    # Switch to the Barako Betting tab
    driver.switch_to.window(driver.window_handles[1])

    driver.find_element_by_xpath('//button[normalize-space()="' + status + '"]').click()
    driver.find_element_by_xpath('//button[normalize-space()="PROCESS CREDITS"]').click()
    time.sleep(3)

    # Switch back to the primary tab of SabongLive618
    driver.switch_to.window(driver.window_handles[0])

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    scrape(driver)
    driver.quit()
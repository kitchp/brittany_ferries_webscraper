import time
import datetime
import os
import pdfplumber
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

# Set the path to the download directory
download_dir = "/Users/kitchphil/Desktop/brittanyferriesdump"

# Function to delete all PDFs in the directory
def delete_pdfs_from_folder(directory_path):
    try:
        for filename in os.listdir(directory_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(directory_path, filename)
                os.remove(file_path)
                print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting files: {e}")

# Delete existing PDFs at the beginning
delete_pdfs_from_folder(download_dir)

# Function to calculate and display the next run time
def show_next_run_message(interval_hours):
    current_time = datetime.datetime.now()
    next_run_time = current_time + datetime.timedelta(hours=interval_hours)
    print(f"Script will run again at: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Your existing script logic...
# The rest of your web scraping and PDF processing code here.

count = 0

while count == 0:

    # Setup Firefox options with custom download settings
    def setup_firefox_driver():
        firefox_options = Options()
        firefox_options.set_preference("browser.download.folderList", 2)  # Use custom location (2)
        firefox_options.set_preference("browser.download.dir", download_dir)  # Set the download directory
        firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # Auto-download PDFs
        firefox_options.set_preference("pdfjs.disabled", True)  # Disable the PDF viewer to force download

        # Setup the Firefox WebDriver with the options
        service = Service(executable_path='/Users/kitchphil/Downloads/geckodriver')  # Adjust the path to geckodriver
        return webdriver.Firefox(service=service, options=firefox_options)
    
    # Function to handle cookie consent popup and remove the overlay
    def accept_cookies_and_remove_overlay(driver):
        try:
            # Accept the cookies first
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))
            )
            accept_button.click()
            print("Cookies accepted.")
            
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, 'onetrust-pc-dark-filter'))
            )
            print("Cookie overlay has disappeared.")
            
            # Use JavaScript to ensure any remaining overlay is removed
            driver.execute_script(
                "document.querySelector('.onetrust-pc-dark-filter').style.display = 'none';"
            )
            print("Overlay removed using JavaScript.")
            
        except Exception as e:
            print("No cookie consent popup found or another issue occurred:", e)

    # Function to click the chevron icon (dropdown) with retry mechanism
    def click_chevron_icon(driver):
        try:
            # Try to click the chevron icon with an explicit wait
            chevron_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//mat-icon[@data-mat-icon-name="baicon-chevron-down"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", chevron_icon)
            chevron_icon.click()
            print("Chevron icon clicked.")
        except Exception as e:
            print(f"Error occurred while clicking the chevron icon: {e}. Retrying...")
            # Retry clicking the chevron after ensuring overlay is removed
            accept_cookies_and_remove_overlay(driver)
            chevron_icon = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//mat-icon[@data-mat-icon-name="baicon-chevron-down"]'))
            )
            chevron_icon.click()
            print("Chevron icon clicked on retry.")

    # Function to select the 5th option using JavaScript
    def select_5th_option_with_js(driver):
        try:
            # Wait for the overlay to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cdk-overlay-container"))
            )
            print("Overlay appeared.")
            
            # Use JavaScript to select the 5th option
            driver.execute_script(
                "document.querySelector('#cdk-overlay-0 > div.ng-tns-c3113121375-6.bf-adaptive-field-panel-wrap.undefined.is-desktop.ng-trigger.ng-trigger-transformPanel.ng-star-inserted > bf-reactive-adaptive-field > div > div > mat-selection-list > mat-list-option:nth-child(5)').click();"
            )
            print("5th option selected via JavaScript.")
        except Exception as e:
            print(f"Error selecting the 5th option via JavaScript: {e}")

    # Function to select the 6th option using JavaScript
    def select_6th_option_with_js(driver):
        try:
            # Wait for the overlay to appear
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "cdk-overlay-container"))
            )
            print("Overlay appeared.")
            
            # Use JavaScript to select the 6th option
            driver.execute_script(
                "document.querySelector('#cdk-overlay-0 > div.ng-tns-c3113121375-6.bf-adaptive-field-panel-wrap.undefined.is-desktop.ng-trigger.ng-trigger-transformPanel.ng-star-inserted > bf-reactive-adaptive-field > div > div > mat-selection-list > mat-list-option:nth-child(6)').click();"
            )
            print("6th option selected via JavaScript.")
        except Exception as e:
            print(f"Error selecting the 6th option via JavaScript: {e}")

    # Function to click the button by XPath
    def click_button_by_xpath(driver):
        try:
            button_xpath = "/html/body/dd-root/mat-sidenav-container/mat-sidenav-content/main/dd-cabin-availability/mat-tab-group/div/mat-tab-body[1]/div/div/div/dd-cabin-availability-pdf-panel/section/div[2]/div/div/form/button/span[2]"
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath))
            )
            button.click()
            print("Button clicked successfully.")
        except Exception as e:
            print(f"Error clicking the button: {e}")

    # Function to click the download button in the PDF viewer
    def click_download_button_in_pdf_viewer(driver):
        try:
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='mat-tab-content-0-0']/div/div/div/dd-cabin-availability-pdf-panel/section/iframe"))
            )
            driver.switch_to.frame(iframe)
            
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='download']"))
            )
            download_button.click()
            print("Download button clicked.")
            
            driver.switch_to.default_content()
        except Exception as e:
            print(f"Error clicking the download button: {e}")

    # Phase 1: Select the 5th option and download PDF
    driver = setup_firefox_driver()
    driver.get('https://www.brittany-ferries.co.uk/cabin-availability?availabilityType=CABIN')
    
    # Accept cookies, remove overlay, and handle page
    accept_cookies_and_remove_overlay(driver)
    click_chevron_icon(driver)
    select_5th_option_with_js(driver)  # Select the 5th option
    click_button_by_xpath(driver)
    click_download_button_in_pdf_viewer(driver)
    
    # Close WebDriver after the first download
    driver.quit()
    
    # Phase 2: Reopen WebDriver, select the 6th option, and download PDF
    driver = setup_firefox_driver()
    driver.get('https://www.brittany-ferries.co.uk/cabin-availability?availabilityType=CABIN')
    
    # Accept cookies, remove overlay, and handle page again
    accept_cookies_and_remove_overlay(driver)
    click_chevron_icon(driver)  # Retry mechanism for chevron click
    select_6th_option_with_js(driver)  # Select the 6th option using JavaScript
    click_button_by_xpath(driver)
    click_download_button_in_pdf_viewer(driver)
    
    # Close WebDriver after the second download
    driver.quit()

    # Calculate and show the next run message (every 2 hours)
    show_next_run_message(interval_hours=2)
    
    # Sleep for 2 hours
    time.sleep(7200)

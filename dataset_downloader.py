import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from helpers import *
import coloredlogs, logging
from selenium.webdriver.common.keys import Keys

# Configure logging to a file
logging.basicConfig(filename='app.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the log level

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Set the log level for the console handler
# Create a formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)
def download_datasets():
    #Selenium Setup
    # ================================================================
    logger.info("Dataset downloading process started")

    chrome_options = webdriver.ChromeOptions() # Set up Chrome options
    raw_data_dir = os.path.join(os.getcwd(),
                                "raw_datasets")  # Downloads will go to a 'downloads' folder in the current working directory
    # Create the downloads directory if it does not exist
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)
    delete_files_and_folders(raw_data_dir) # Reset the download directory
    # Set Chrome preferences for downloading files
    prefs = {
        "download.default_directory": raw_data_dir,  # Set download directory
        "download.prompt_for_download": False,  # Disable download prompt
        "download.directory_upgrade": True,  # Automatically overwrite the target directory
        "safebrowsing.enabled": True,  # Allow downloads even if safe browsing warnings are triggered
        "profile.default_content_settings.popups": 0  # Disable popups
    }

    # Set up Chrome options to use a custom profile directory
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    # chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    # chrome_options.add_argument("--window-size=1920x1080")  # Set window size (optional)
    # chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (optional, for Linux)
    # chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems (optional, for Linux)

    chrome_options.add_argument("user-data-dir=C:/mychrome")  # Specify a new or different path
    chrome_options.add_experimental_option("prefs", prefs)
    logger.info("Selenium Setup done")
    # Initialize the Chrome WebDriver with the specified options
    try:
        driver = webdriver.Chrome(options=chrome_options)
        base_url = "https://www.tradingview.com/chart/pQoTYtAg/"
        driver.implicitly_wait(30)
        logger.info("Selenium Driver established")
    except Exception as e:
        logger.error(f"Failed to establish the chrome driver. Reason: {e}")


    #===================================================================
    if internet_check():
        logger.info("Internet connection is working")
        driver = driver
        driver.get(base_url)

        # check if logedin
        logger.info("Logging in to tradingview")
        logen_sign=driver.find_elements(By.XPATH, "//div[@id='drawing-toolbar']/div/div/div/div/div[4]/div/div/div/button/div")
        if logen_sign:
            logger.info("Logged successfully to tradingview")
            driver.get("https://www.tradingview.com/chart/pQoTYtAg/?symbol=TVC%3AGOLD")
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='All'])[1]/following::*[name()='svg'][1]").click()
            driver.find_element(By.NAME, "start-date-range").click()
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.BACKSPACE)
            driver.find_element(By.NAME, "start-date-range").send_keys("1990-01-01")
            driver.find_element(By.NAME, "end-date-range").click()
            driver.find_element(By.XPATH, "//*[@id='overlap-manager-root']/div[2]/div/div[1]/div/div[4]/div/span/button/span").click()
            time.sleep(2)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::div[2]").click()

            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()
            logger.info("Gold dataset downloaded")
            # Download DXY
            driver.get("https://www.tradingview.com/chart/pQoTYtAg/")
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("dxy")
            time.sleep(1)
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div[3]/div[2]/div").click()
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='All'])[1]/following::*[name()='svg'][1]").click()
            driver.find_element(By.NAME, "start-date-range").click()
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.BACKSPACE)
            driver.find_element(By.NAME, "start-date-range").send_keys("1990-01-01")
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[4]/div/span/button/span").click()
            time.sleep(2)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::div[2]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()

            logger.info("DXY dataset downloaded")
            # # #Effective Federal Funds Rate
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("Effective Federal Funds Rate")
            time.sleep(1)  # Wait for the search results to load
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div/div").click()
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='All'])[1]/following::*[name()='svg'][1]").click()
            driver.find_element(By.NAME, "start-date-range").click()
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.BACKSPACE)
            driver.find_element(By.NAME, "start-date-range").send_keys("1990-01-01")
            driver.find_element(By.NAME, "end-date-range").click()
            driver.find_element(By.XPATH, "//*[@id='overlap-manager-root']/div[2]/div/div[1]/div/div[4]/div/span/button/span").click()
            time.sleep(2)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::div[2]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()
            logger.info("Effective Federal Funds Rate dataset downloaded")
            # # United States Interest Rate
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("United State Interest Rate")
            time.sleep(1)  # Wait for the search results to load
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div/div").click()
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='All'])[1]/following::*[name()='svg'][1]").click()
            driver.find_element(By.NAME, "start-date-range").click()
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.BACKSPACE)
            driver.find_element(By.NAME, "start-date-range").send_keys("1990-01-01")
            driver.find_element(By.NAME, "end-date-range").click()
            driver.find_element(By.XPATH, "//*[@id='overlap-manager-root']/div[2]/div/div[1]/div/div[4]/div/span/button/span").click()
            time.sleep(2)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::div[2]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()
            logger.info("United States Interest Rate dataset downloaded")
            #United States Inflation Rate
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("United States Inflation Rate")
            time.sleep(1)  # Wait for the search results to load
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div/div").click()
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::div[2]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()
            logger.info("United States Inflation Rate dataset downloaded")
            #United States Consumer Confidence
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("United States Consumer Confidence")
            time.sleep(2)
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div/div").click()
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::*[name()='svg'][1]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()
            logger.info("United States Consumer Confidence dataset downloaded")
            # United States Unemployment Rate
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("United States Unemployment Rate")
            time.sleep(2)
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div/div").click()
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::*[name()='svg'][1]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()
            time.sleep(1)
            logger.info("United States Unemployment Rate dataset downloaded")
            #NASDAQ
            driver.get("https://www.tradingview.com/chart/pQoTYtAg/?symbol=TVC%3AGOLD")
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("ndx")
            time.sleep(1)
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div/div").click()
            time.sleep(3)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='All'])[1]/following::*[name()='svg'][1]").click()
            time.sleep(3)
            driver.find_element(By.NAME, "start-date-range").click()
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.BACKSPACE)
            driver.find_element(By.NAME, "start-date-range").send_keys("1990-01-01")
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]").click()
            driver.find_element(By.XPATH, "//*[@id='overlap-manager-root']/div[2]/div/div[1]/div/div[4]/div/span/button/span").click()
            time.sleep(3)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::*[name()='svg'][1]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()
            time.sleep(1)
            logger.info("NASDAQ dataset downloaded")
            #SPX
            driver.get("https://www.tradingview.com/chart/pQoTYtAg/?symbol=TVC%3AGOLD")
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("spx")
            time.sleep(1)
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[2]/div").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div/div").click()
            time.sleep(3)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='All'])[1]/following::*[name()='svg'][1]").click()
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/div/div").click()
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.BACKSPACE)
            driver.find_element(By.NAME, "start-date-range").send_keys("1990-01-01")
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]").click()
            driver.find_element(By.XPATH, "//*[@id='overlap-manager-root']/div[2]/div/div[1]/div/div[4]/div/span/button/span").click()
            time.sleep(3)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::div[2]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()
            time.sleep(1)
            logger.info("SPX dataset downloaded")
            #NYA
            driver.get("https://www.tradingview.com/chart/pQoTYtAg/?symbol=TVC%3AGOLD")
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("NYA")
            time.sleep(1)
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[2]/div").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div/div").click()
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='All'])[1]/following::*[name()='svg'][1]").click()
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/div/div").click()
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.BACKSPACE)
            driver.find_element(By.NAME, "start-date-range").send_keys("1990-01-01")
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]").click()
            driver.find_element(By.XPATH, "//*[@id='overlap-manager-root']/div[2]/div/div[1]/div/div[4]/div/span/button/span").click()
            time.sleep(3)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::div[2]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()
            time.sleep(1)
            logger.info("NYA dataset downloaded")
            #Light Crude Oil Futuires
            driver.get("https://www.tradingview.com/chart/pQoTYtAg/?symbol=TVC%3AGOLD")
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("cl1!")
            time.sleep(1)
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[2]/div").click()
            time.sleep(1)
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div/div").click()
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='All'])[1]/following::*[name()='svg'][1]").click()
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/div/div").click()
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.BACKSPACE)
            driver.find_element(By.NAME, "start-date-range").send_keys("1990-01-01")
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]").click()
            driver.find_element(By.XPATH, "//*[@id='overlap-manager-root']/div[2]/div/div[1]/div/div[4]/div/span/button/span").click()
            time.sleep(5)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::div[2]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()
            time.sleep(1)
            logger.info("Light Crude Oil Futures dataset downloaded")
            #bitcoin all time history
            driver.get("https://www.tradingview.com/chart/pQoTYtAg/?symbol=TVC%3AGOLD")
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("bitcoin all time history")
            time.sleep(1)
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[2]/div").click()
            time.sleep(1)
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div/div").click()
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='All'])[1]/following::*[name()='svg'][1]").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/div/div").click()
            time.sleep(1)
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.BACKSPACE)
            driver.find_element(By.NAME, "start-date-range").send_keys("1990-01-01")
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]").click()
            driver.find_element(By.XPATH, "//*[@id='overlap-manager-root']/div[2]/div/div[1]/div/div[4]/div/span/button/span").click()
            time.sleep(5)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::div[2]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()

            time.sleep(1)
            logger.info("BTCUSD dataset downloaded")
            #crypto total market cap
            driver.get("https://www.tradingview.com/chart/pQoTYtAg/?symbol=TVC%3AGOLD")
            driver.find_element(By.XPATH, "//button[@id='header-toolbar-symbol-search']/div").click()
            driver.find_element(By.XPATH, "//input[@value='']").click()
            driver.find_element(By.XPATH, "//input[@value='']").clear()
            driver.find_element(By.XPATH, "//input[@value='']").send_keys("crypto total market")
            time.sleep(1)
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[2]/div").click()
            time.sleep(1)
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div[2]/div/div[5]/div/div/div/div").click()
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='All'])[1]/following::*[name()='svg'][1]").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/div/div").click()
            time.sleep(1)
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.CONTROL + "a")
            driver.find_element(By.NAME, "start-date-range").send_keys(Keys.BACKSPACE)
            driver.find_element(By.NAME, "start-date-range").send_keys("1990-01-01")
            driver.find_element(By.XPATH, "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]").click()
            driver.find_element(By.XPATH, "//*[@id='overlap-manager-root']/div[2]/div/div[1]/div/div[4]/div/span/button/span").click()
            time.sleep(5)
            driver.find_element(By.XPATH,
                                "(.//*[normalize-space(text()) and normalize-space(.)='Save'])[3]/following::div[2]").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/span/div/div/div/div[4]/span[2]/span").click()
            driver.find_element(By.XPATH,
                                "//div[@id='overlap-manager-root']/div[2]/div/div/div/div[3]/div/span/button/span").click()
            logger.info("Crypto total market capdataset downloaded")
            time.sleep(5)
            # Clean up
            driver.quit()
            logger.info("Driver cleaned up")


        else:
            print("LogedOut")
            logger.warning("TradingView not logged in")
            driver.quit()

download_datasets()


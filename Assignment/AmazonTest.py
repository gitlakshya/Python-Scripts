from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from collections import namedtuple


search_term = "lg soundbar"

# Function to extract product details (name and price)
def get_product_details(driver):
    product_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='s-main-slot s-result-list s-search-results sg-row']"))
    )

    
    products = []
    for product in product_elements.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']"):
        try:
            # Locate elements within each product element
            name_element = product.find_element(By.XPATH, ".//span[@class='a-size-medium a-color-base a-text-normal']")
            name = name_element.text.strip()

            price_element = product.find_element(By.XPATH, ".//span[@class='a-price-whole']")
            price = int(price_element.text.replace(",", ""))  # Handle comma-separated prices
        except (NoSuchElementException, ValueError):
            name = "NA"
            price = 0  # Considered missing price as zero

        product_data = Product(name, price)
        products.append(product_data)
    return products


Product = namedtuple("Product", ["name", "price"])

def main():
    # Driver path for chrome driver
    driver_path = "./driver/chromedriver.exe"  # Adjust for your system


    service = webdriver.ChromeService(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get("https://www.amazon.in/")

        
        search_box = driver.find_element(By.ID, "twotabsearchtextbox")
        search_box.send_keys(search_term)
        search_button = driver.find_element(By.ID, "nav-search-submit-button")
        search_button.click()

        
        products = get_product_details(driver)

       
        sorted_products = sorted(products, key=lambda product: product.price)

        # Print results
        for product in sorted_products:
            print(f"{product.price} {product.name}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
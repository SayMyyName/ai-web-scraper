from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_website(website):
    print('Launching chrome browser...')

    
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        "--headless=new"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(website)

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'body'))
        )

        print('Page Loaded...')
        html = driver.page_source
        return html
    
    except Exception as e:
        print(f"An error occured: {e}")
        return None
    
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(['script', 'style']):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator='\n')
    cleaned_content = '\n'.join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]


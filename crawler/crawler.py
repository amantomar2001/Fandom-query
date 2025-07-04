from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
from bs4 import BeautifulSoup

# Hardcoded path
RAW_DATA_DIR = "C:/Users/dell/New folder (4)/Project/project/data/raw"

def navigate_to_target(query, query2):
    print(f"Line {__line__()}: Starting navigate_to_target with query={query}, query2={query2}")
    options = Options()
    print(f"Line {__line__()}: Setting Chrome options")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--enable-unsafe-swiftshader')
    options.add_argument('--disable-dev-shm-usage')
    print(f"Line {__line__()}: Initializing Chrome driver")
    driver = webdriver.Chrome(options=options)
    try:
        print(f"Line {__line__()}: Navigating to Fandom")
        driver.get('https://www.fandom.com')
        print(f"Line {__line__()}: Waiting for search box")
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search'][type='text']"))
        )
        print(f"Line {__line__()}: Sending query to search box")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        print(f"Line {__line__()}: Waiting for wiki links")
        wiki_links = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.unified-search__result__title[href*='.fandom.com']"))
        )
        print(wiki_links)
        print(f"Line {__line__()}: Selecting wiki link")
        target_url = None
        query_lower = query.lower().replace(" ", "")
        for link in wiki_links:
            href = link.get_attribute('href')
            text = link.text.lower()
            if re.search(query_lower, href.lower()) or 'wiki' in text:
                target_url = href
                break
        if not target_url and wiki_links:
            target_url = wiki_links[0].get_attribute('href')
        if not target_url:
            raise Exception("No relevant wiki found")
        print(f"Line {__line__()}: Target URL: {target_url}")
        driver.get(target_url)
        time.sleep(1)
        print(f"Line {__line__()}: Waiting for wiki search box")
        try:
            wiki_search_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input.search-app__input"))
            )
        except:
            print(f"Line {__line__()}: Fallback to generic text input")
            wiki_search_box = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
            )
        print(f"Line {__line__()}: Sending query2 to wiki search box")
        wiki_search_box.send_keys(query2)
        wiki_search_box.send_keys(Keys.RETURN)
        time.sleep(1)
        print(f"Line {__line__()}: Waiting for first search result")
        try:
            first_result = WebDriverWait(driver, 7).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.unified-search__result__title"))
            )
        except:
            print(f"Line {__line__()}: Fallback to generic wiki link")
            first_result = WebDriverWait(driver, 7).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "main a[href*='/wiki/']"))
            )
        result_url = first_result.get_attribute('href')
        print(f"Line {__line__()}: Navigating to result URL: {result_url}")
        driver.get(result_url)
        print(f"Line {__line__()}: Expanding buttons")
        expandable_elements = driver.find_elements(By.CSS_SELECTOR, 'main button, main [role="button"], main a[data-tracking-label="expand"], main .mw-collapsible-toggle, main .navbox-title, main [data-expandtext], main [data-toggle]')
        if expandable_elements:
            for element in expandable_elements:
                try:
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(0.1)
                except:
                    pass
        print(f"Line {__line__()}: Extracting main content")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        main_content = soup.find('main')
        content_html = str(main_content) if main_content else html
        title_elem = soup.find('h1') or soup.find('title')
        title = title_elem.get_text().strip() if title_elem else 'page'
        title = re.sub(r'[^\w\s-]', '_', title)
        title = re.sub(r'\s+', '_', title).strip('_')
        print(f"Line {__line__()}: Saving HTML with title: {title}")
        # Create game-specific subfolder
        game_folder = re.sub(r'[^\w\s-]', '_', query).strip()
        game_folder = re.sub(r'\s+', '_', game_folder).strip('_')
        game_dir = os.path.join(RAW_DATA_DIR, game_folder)
        os.makedirs(game_dir, exist_ok=True)
        file_path = os.path.join(game_dir, f'{title}.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content_html)
        print(f"Line {__line__()}: HTML saved at {file_path}")
        return result_url, content_html, file_path
    except Exception as e:
        print(f"Line {__line__()}: Error: {e}")
        return None, None, None
    finally:
        print(f"Line {__line__()}: Closing driver")
        driver.quit()

def __line__():
    import inspect
    return inspect.currentframe().f_back.f_lineno
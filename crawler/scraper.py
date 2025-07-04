import os
from bs4 import BeautifulSoup
import re
import uuid


RAW_DATA_DIR = "C:/Users/dell/New folder (4)/Project/project/data/raw"
PROCESSED_DATA_DIR = "C:/Users/dell/New folder (4)/Project/project/data/processed"

def scrape_html(html_file_path, game_name):
    
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    scraped_data = {}
    current_heading = "Introduction"
    scraped_data[current_heading] = []

    main_content = soup.find('main') or soup.find('body')
    if not main_content:
        return {}

    for element in main_content.find_all(['h1', 'h2', 'h3', 'p', 'table', 'ul', 'ol']):
        if element.name in ['h1', 'h2', 'h3']:
            current_heading = element.get_text(strip=True)
            scraped_data[current_heading] = []
        elif element.name == 'p':
            text = element.get_text(strip=True)
            if text:
                scraped_data[current_heading].append({"type": "text", "content": text})
        elif element.name == 'table':
            table_content = []
            rows = element.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                row_data = [cell.get_text(strip=True) for cell in cells]
                table_content.append("| " + " | ".join(row_data) + " |")
            if table_content:
                if rows and rows[0].find('th'):
                    headers = rows[0].find_all('th')
                    table_content.insert(1, "| " + " | ".join(["---"] * len(headers)) + " |")
                scraped_data[current_heading].append({"type": "table", "content": table_content})
        elif element.name in ['ul', 'ol']:
            list_items = [li.get_text(strip=True) for li in element.find_all('li') if li.get_text(strip=True)]
            if list_items:
                scraped_data[current_heading].append({"type": "list", "content": list_items})

    base_name = os.path.splitext(os.path.basename(html_file_path))[0]
    game_folder = re.sub(r'[^\w\s-]', '_', game_name).strip()
    game_folder = re.sub(r'\s+', '_', game_folder).strip('_')
    game_dir = os.path.join(PROCESSED_DATA_DIR, game_folder)
    os.makedirs(game_dir, exist_ok=True)
    output_file = os.path.join(game_dir, f"{base_name}.md")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# {base_name.replace('_', ' ')}\n\n")
        for heading, items in scraped_data.items():
            f.write(f"## {heading}\n\n")
            for item in items:
                if item['type'] == 'text':
                    f.write(f"{item['content']}\n\n")
                elif item['type'] == 'table':
                    for row in item['content']:
                        f.write(f"{row}\n")
                    f.write("\n")
                elif item['type'] == 'list':
                    for li in item['content']:
                        f.write(f"- {li}\n")
                    f.write("\n")

    return scraped_data
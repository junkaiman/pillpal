import time
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import requests
import json
import os



def process_string(input_string):
    stripped_string = input_string.strip()
    if not re.match("^[A-Za-z0-9]*$", stripped_string):
        raise ValueError("String contains invalid characters. Only digits and English letters are allowed.")
    lowercase_string = stripped_string.lower()    
    return lowercase_string


def parse_pill_page_from_query_url(query_url, base_url="https://www.drugs.com"):
    response = requests.get(query_url)
    response.raise_for_status() 
    
    soup = BeautifulSoup(response.content, "html.parser")    
    a_tag = soup.find("a", class_="ddc-btn ddc-btn-small")
    
    if a_tag:
        relative_href = a_tag.get("href")
        absolute_href = urljoin(base_url, relative_href)
    
        first_card = soup.find("div", class_="ddc-pid-list").find("div", class_="ddc-card")
    
        if first_card:
            img_tag = first_card.find("div", class_="ddc-pid-img pid-img-fit-133")
            if img_tag and img_tag.get("data-image-src"):
                img_url = img_tag["data-image-src"]
                return absolute_href, img_url
            else:
                print("No image source found in the first card.")
                return absolute_href, None
        else:
            print("No card found in the pid-list.")
            return absolute_href, None
    
    else:
        print("No matching <a> tag found.")
        return None, None

def parse_pill_page(pill_url):
    response = requests.get(pill_url)
    response.raise_for_status() 
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 1. Extract the general description of the pill
    description = ""
    content_head = soup.find("div", class_="ddc-main-content-head")
    if content_head:
        for sibling in content_head.find_next_siblings():
            if sibling.name == "h2":
                break
            if sibling.name == "p":
                description += sibling.get_text(strip=True) + "\n"
    
    interactions_link = soup.find("a", string="Check interactions")
    interactions_href = urljoin("https://www.drugs.com", interactions_link["href"]) if interactions_link else None
    
    side_effects_link = soup.find("a", string="Side effects")
    side_effects_href = urljoin("https://www.drugs.com", side_effects_link["href"]) if side_effects_link else None
    
    return description.strip(), interactions_href, side_effects_href


def parse_interactions_page(interactions_url):
    response = requests.get(interactions_url)
    response.raise_for_status() 

    soup = BeautifulSoup(response.text, 'html.parser')

    interactions_list = soup.find('ul', class_='interactions ddc-mgt-0 ddc-list-unstyled')

    major_items = interactions_list.find_all('li', class_='int_3')
    moderate_items = interactions_list.find_all('li', class_='int_2')

    interaction_dict = {"major interactions":[], "moderate interactions":[]}

    for item in major_items:
        drug_name = item.find('a')
        if drug_name:
            interaction_dict["major interactions"].append(drug_name.text.strip())

    for item in moderate_items:
        drug_name = item.find('a')
        if drug_name:
            interaction_dict["moderate interactions"].append(drug_name.text.strip())

    return interaction_dict



def parse_side_effects_page(side_effects_url):
    response = requests.get(side_effects_url)
    response.raise_for_status()  

    soup = BeautifulSoup(response.text, 'html.parser')
    side_effects_dict = {}

    details_elements = soup.find_all('details', class_='ddc-accordion ddc-accordion-single')

    for details in details_elements:
        h3_tag = details.find('h3')
        if h3_tag:
            category = h3_tag.get_text(strip=True)

            ul_tag = details.find('ul')
            if ul_tag:
                side_effects = [li.get_text(strip=True) for li in ul_tag.find_all('li')]
                side_effects_dict[category] = side_effects

    return side_effects_dict

def query(query_url, save_dir):
    try:
        pill_page, img_url = parse_pill_page_from_query_url(query_url)
        
        if pill_page:            
            description, interactions_page, side_effects_page = parse_pill_page(pill_page)            
            interaction_dict = parse_interactions_page(interactions_page)
            side_effects_dict = parse_side_effects_page(side_effects_page)

            description = " ".join(description.split())  # This removes extra spaces and normalizes the string

            combined_dict = {
                "imgUrl": img_url,
                "description": description,
                "interactions": interaction_dict,
                "sideEffects": side_effects_dict
            }
            save_path = os.path.join(save_dir,"pill_info.json")
            with open(save_path, "w") as json_file:
                json.dump(combined_dict, json_file, indent=4)   

        return save_path 
        
    except ValueError as ve:
        print("Value error:", ve)
    except Exception as e:
        print("Exception:", e)



if __name__ == "__main__":
    query_url = "https://www.drugs.com/imprints.php?imprint=93551&color=&shape=0" 
    query(query_url, "./")
    
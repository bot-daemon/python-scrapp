import requests
from bs4 import BeautifulSoup
import json

def scrape_data():
    url = "https://github.com/lukilme?tab=repositories"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.string if soup.title else "No title found"
    
    description_tag = soup.find('meta', attrs={"name": "description"})
    description = description_tag.get('content') if description_tag else "No description found"
    print(title)
    print(description)
    
    repositories = []
    repo_elements = soup.find_all('a', attrs={"itemprop": "name codeRepository"})
    for repo in repo_elements:
        repositories.append(repo.get('href'))  
        print(repo.get('href'))

    data = {
        "title": title,
        "description": description,
        "repositories": repositories
    }
    
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    scrape_data()

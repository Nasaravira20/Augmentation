
import requests

def fetch_wikipedia_page(title):
    url = f"https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "titles": title
    }
    response = requests.get(url, params=params)
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    if 'extract' in page:
        return page['extract'] 
    else:
        print(page.keys())
        return ''

# Fetch the content of a Wikipedia page
# content = fetch_wikipedia_page("Graph theory")
# print(content)

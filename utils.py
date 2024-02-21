from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Access environment variables
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
gsearch_api_key = os.getenv('GSEARCH_API_KEY')
cse_id = os.getenv('CSE_ID')


# Function to get completion from OpenAI
def get_completion(prompt, model="gpt-3.5-turbo"):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model=model,
    )
    return chat_completion.choices[0].message.content


# Function to perform a Google search using the Custom Search JSON API
def google_search(query):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": gsearch_api_key,
        "cx": cse_id,
        "q": query
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None


# Function to grab specified number of URLs from a Google search
def grab_urls(query, num_link=3):
    search_results = google_search(query)
    urls = []
    if search_results:
        for item in search_results.get("items", []):
            urls.append(item["link"])

    return urls[:num_link]


# Function to download the content of a given URL
def download_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        return response.text  # Assuming the content is text-based, you can access it using response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading the URL: {e}")
        return None


# Function to extract visible text from HTML content
def extract_visible_text(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        visible_text = soup.get_text()  # Get the visible text content using .get_text() method of BeautifulSoup
        return visible_text

    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        return None


# Function to aggregate visible text from multiple URLs
def url_aggregated(urls, num_link):
    visible_text = ""
    for url in urls[:num_link]:
        html_content = download_url(url)
        if html_content:
            visible_text += extract_visible_text(html_content) + "\n\n" + "------"

    return visible_text


# Function to get a citation from a list of URLs
def get_citation(urls):
    source_urls = "\n".join(urls)
    return source_urls


# Function to perform a smart search using Google, aggregate content, and generate a completion prompt
def smart_search(query):
    urls = grab_urls(query, num_link=3)
    articles = url_aggregated(urls, num_link=3)
    prompt = f"""
    From the list of articles: {articles[:16000]}\n
    Use the given articles and your common knowledge to answer the question in a minimum of 3 sentences: {query}
    """
    response = get_completion(prompt)
    return response

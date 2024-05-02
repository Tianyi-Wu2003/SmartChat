from wikipage import Wikipage
from chatclient import Chatclient
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPEN_AI_API")

client = OpenAI(api_key=API_KEY)

def extract_keywords(user_input: str) -> list[str]:
    """
    Extract keywords based on user input
        
    :param user_input: user input (String)
    :return: keywords extracted (List(String))
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
            {"role": "user", "content": f"Extract one or more keywords or phrases directly included to this information."},
        ]
    )
    keywords = response.choices[0].message.content
    keyword_list = keywords.split(',')
    return keyword_list

def helper_get_similarity(user_input: str, keyword: str) -> float:
    """
    Helper function to return similarity score between user_input and keyword.
        
    :param : sentence that user input (string)
    :param : keyword for testing (string)
    :return: similarity score (float)
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Compare the similarity between the following texts:"},
            {"role": "user", "content": f"Question: {user_input}"},
            {"role": "user", "content": f"Title: {keyword}"},
            {"role": "user", "content": "Provide a similarity score between 0 and 1, where 1 indicates very similar and 0 indicates very different."},
        ]
    )
    similarity_text = response.choices[0].message.content
    try:
        similarity = float(similarity_text)
    except ValueError:
        similarity = 0.0  # Default to 0 if parsing fails
    return similarity

def find_most_similar_keyword(user_input: str, keywords: list[str]) -> str:
    """
    Find most related keyword of the list to user input
        
    :param user_input: sentence that user input (string)
    :param keywords: a list of keywords (List(String))
    :return keyword: the most related keyword to user input(String)
    """   
    similarities = [(title, helper_get_similarity(user_input, title)) for title in keywords]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[0][0] if similarities else None

def new_title(user_input: str) -> str:
    """
    Find best keyword based on user input to access as Wikipedia title
        
    :param user_inpu: sentence that user input (string)
    :return title: best keyword (String)
    """   
    keywords = extract_keywords(user_input)
    title = find_most_similar_keyword(user_input, keywords)
    return title

def new_chat(title:str) -> Chatclient:
    """
    Get a chat client based on a title, with corresponding wikipedia page.
        
    :param title: title (string)
    :return client: chat client(Chatclient)
    """   
    
    client = Chatclient(API_KEY, title)
    mainpage = Wikipage(title)
    mainpage.get_text()
    mainpage.remove_extra()
    client.set_page(mainpage)
    return client

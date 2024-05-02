import wikipage
from openai import OpenAI

"""
Chatclient class that creates a client for openai and keeps track of title(keyword) and Wikipage
"""
class Chatclient:
    def __init__(self, api_key: str, title: str):
        self.title = title
        self.client = OpenAI(api_key=api_key)
        self.page: wikipage.Wikipage
        self.has_page = False
    
    def set_page(self, page:wikipage.Wikipage):
        self.page = page
        self.has_page = True
    
    """
    Helper function to find top 3 section titles from all titles based on question
    """
    def find_best_sections(self, question:str, titles):
        response = self.client.chat.completions.create(
			model="gpt-3.5-turbo-0125",
			messages=[
				{"role": "system", "content": "You are a helpful and efficient assistant."},
				{"role": "user", "content": f"This is my question:{question}"},
				{"role": "user", "content": f"With articles of the following titles,  which one do you think is most likely to give the answer?"},
				{"role": "user", "content": f"With articles of the following titles,  which one do you think is most likely to give the answer?"},
				{"role": "user", "content": f"These are the titles:{titles}"},
				{"role": "user", "content": f"Respond with the top three titles only, they should be separated by commas, don't quote them. don't say anything else."},
			    {"role": "user", "content": f"You should follow the format of this sample answer: title1, title2, title3"},
            ]
        )
        return response.choices[0].message.content
      
    """
    Response generator if there is extra information given to openai api
    """
    def generate_with_prompt(self, question: str):
        page = self.page
        section_titles = self.find_best_sections(question, list(page.text_dict.keys())).split(', ')
        promp_text = ''
        for s in section_titles:
            if s in page.text_dict:
              promp_text += page.text_dict[s]
        promp_text +=''
        response = self.client.chat.completions.create(
			model="gpt-3.5-turbo-0125",
			messages=[
				{"role": "system", "content": "You are a helpful assistant."},
				{"role": "user", "content": promp_text},
				{"role": "user", "content": f"Based on the text above, answer the question: {question}"},
			]
		)
        return response.choices[0].message.content
    
    """
    Response generator if there is no other information given to openai api
    """
    def generate_without_prompt(self, question:str):
        response = self.client.chat.completions.create(
			model="gpt-3.5-turbo-0125",
			messages=[
				{"role": "system", "content": "You are a helpful assistant."},
				{"role": "user", "content": f"Answer the question: {question}"},
    			{"role": "user", "content": f"Start your answer with: I can't find any wikipedia page titled {self.title}"},
			]
		)
        return response.choices[0].message.content

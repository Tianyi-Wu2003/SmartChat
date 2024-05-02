import wikipediaapi


wiki_wiki = wikipediaapi.Wikipedia('SmartChat (isabella)','en')

class Wikipage:
    def __init__(self, title: str):
        self.title = title
        self.sections = []
        self.found_page = False
        self.text_dict = {}

    """
    Set all fields for a Wikipage based on available information 
    """
    def get_text(self):
        page_py = wiki_wiki.page(self.title)
        
        """
        Helper function to divide the wikisections into a dictionary
            
        :param sections: Wikipage sections from wiki api
        :return section_dict: Dictionary of (section title - content) pairings
        """
        def get_section_dict(sections, level=0, prefix=""):
            section_dict = {}
            for s in sections:
                # Create the key with the current section title
                key = prefix + s.title
                # Store the current section's text in the dictionary
                section_dict[key] = s.text
                # Get child sections' data recursively
                child_dict = get_section_dict(s.sections, level + 1, prefix=key + "-")
                # Merge child dictionary into the current dictionary
                section_dict.update(child_dict)
            return section_dict
        
        if (page_py.exists()):
            self.found_page = True
            self.sections = page_py.sections
            self.text_dict = get_section_dict(self.sections)
    """
    Remove extra sections from dictionary
    """
    def remove_extra(self):
        self.text_dict.pop('See also', None)
        self.text_dict.pop('References', None)
        self.text_dict.pop('Bibliography', None)
        self.text_dict.pop('External links', None)

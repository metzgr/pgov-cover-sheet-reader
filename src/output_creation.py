"""
Maps keywords imbedded in template document (keys) to what they will be replaced with in the rendered output document (values). Note that each keyword is identified as "{{keyword_name}}" within the template document.
"""

import utility


# Maps keywords within the template document to the values that they will be replaced by.
REPLACEMENT_MAP = {
    "example string adjective": "incredibly",
    "blocking text": "These are some blockers that were custom-placed into the document. Nice job!"
}


def get_keywords(paragraph):
    """
    Given a paragraph, returns a list of the keywords held within it. NOTE: Keywords are contained within {{double curly brackets}} in the template document.

    :param paragraph: A string of text that may contain keywords contained within double curly brackets (ex: {{keyword}}).
    :return: A list of the keywords contained within the passed text.
    """
    paragraph_copy = paragraph  # Preserves the state of the original text
    keywords = []
    
    while "{{" in paragraph_copy and "}}" in paragraph_copy:
        keyword = paragraph_copy[paragraph_copy.index("{{") + 2:paragraph_copy.index("}}")]
        
        # Removes keyword indicators from the text after the keyword has been stored
        paragraph_copy = paragraph_copy.replace("{{", "", 1)
        paragraph_copy = paragraph_copy.replace("}}", "", 1)

        keywords.append(keyword)
        
    return keywords

def replace_keywords(paragraph): 
    """
    Replaces the keywords in the passed paragraphs within their corresponding values in the replacement map.

    :param paragraph: A string of text that may contain keywords.
    """   
    for keyword in get_keywords(paragraph.text):
        if keyword in REPLACEMENT_MAP.keys():
            paragraph.text = paragraph.text.replace(f"{{{{{keyword}}}}}", REPLACEMENT_MAP[keyword])

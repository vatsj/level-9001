# getter methods for question, description, answer
# takes in BeautifulSoup for html page
def get_question(soup):

    question_elt = soup.find('h1')
    return question_elt.get_text().strip()
    

def get_description(soup):

    # gets elements
    question_elt = soup.find(id="ya-question-detail")
    description_elts = question_elt.find_all("span", class_ = "ya-q-full-text")

    # returns text of each element
    return [description_elt.get_text() for description_elt in description_elts]

def get_answer(soup):

    # gets elements
    answer_elt = soup.find(id="ya-best-answer")
    description_elts = answer_elt.find_all("span", class_ = "ya-q-full-text")

    # returns text of each element
    return [description_elt.get_text() for description_elt in description_elts]

# formats question, description, answer
def get_info(soup): return f"""
QUESTION: {get_question(soup)}
DESCRIPTION: {get_description(soup)}
ANSWER: {get_answer(soup)}
"""
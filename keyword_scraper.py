import requests
import string

def get_keywords(keywords, depth):
    market_id = 'ATVPDKIKX0DER' # Amazon US

    # Get extra keywords by attaching a-z and aa-zz to front and back of keyword
    alphabet = list(string.ascii_lowercase)
    alphabet += [letter*2 for letter in alphabet]

    for keyword in list(dict.fromkeys(keywords[:])):
        keyword_base = keyword.replace(' ', '%20')
        for letter in alphabet:
            keyword_front = (letter + ' ' + keyword_base).replace(' ', '%20')
            keyword_back = (keyword_base + ' ' + letter).replace(' ', '%20')

            for keyword_new in [keyword_base, keyword_front, keyword_back]:
                url = f'https://completion.amazon.com/api/2017/suggestions?mid={market_id}&alias=aps&prefix={keyword_new}&suggestion-type=KEYWORD'
                response = requests.get(url)
                data = response.json()

                suggestions = data['suggestions']
                keywords += [suggestion['value'] for suggestion in suggestions]

    while depth > 1:
        return get_keywords(keywords, depth-1)
    return list(dict.fromkeys(keywords))

keywords = get_keywords(['head torch'], depth=1)

from bs4 import BeautifulSoup
from requests import get
from urllib.parse import urlencode


def google_search(query):
    """
    Function to get Google search results
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }

    query = urlencode({"q": query})

    # Get 20 results in case some of them are None
    resp = get("https://www.google.com/search?{}&num=20&hl=en".format(query), headers=headers)

    if resp.status_code != 200:
        return None, resp.status_code

    bs = BeautifulSoup(resp.text, "html.parser")

    def getContent(element):
        """
        Function to find links & titles in the HTML of a <div> element
        """
        link = element.find("a", href=True)
        title = element.find("h3")

        if link is None or title is None:
            return None

        return link["href"], title.text

    divs = bs.find_all("div", attrs={"class": "g"})

    return list(getContent(d) for d in divs), 200

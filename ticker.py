from bs4 import BeautifulSoup
import requests

def tickerDataScrapper(prod_type) :

    def get_title_ticker(soup) :
        try:
            # Outer Tag Object
            title = soup.find("span", attrs={"id":'mainContent_ltrlCompName'})
            # print(title.text)
            # Inner NavigatableString Object
            title_value = title.text

            # Title as a string value
            title_string = title_value.strip()
            print(title_string)
            
        except AttributeError:
            title_string = ""	
            
        return title_string


    # Code calling begins here.....	
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language' : 'en-US'
    }

    # The webpage URL
    url = f"https://ticker.finology.in/company/{prod_type}"

    # HTTP Request
    webpage = requests.get(url, headers=headers)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    title=get_title_ticker(soup)

    product_details_ticker = []

    # Extract product details
    title = get_title_ticker(soup)
    price = get_title_ticker(soup)
    rating = get_title_ticker(soup)
    review_count = get_title_ticker(soup)
    availability = get_title_ticker(soup)

    # Append details to the list
    product_details_ticker.append({
        "title": title,
        "price": price,
        "rating": rating,
        "review_count": review_count,
        "availability": availability
    })

    return product_details_ticker

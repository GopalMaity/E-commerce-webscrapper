from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import random
from utils import userAgent


app = Flask(__name__)


def get_title(soup):
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})
		# Inner NavigatableString Object
		title_value = title.string
		# Title as a string value
		title_string = title_value.strip()
		
	except AttributeError:
		title_string = ""	
		
	return title_string



# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={"class": "a-price aok-align-center"}).find(
                "span", attrs={"class": "a-offscreen"}
            ).text.strip()
        if len(price) >= 10 :
            price = "NA"
    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={"class": "a-offscreen"}).string.strip()
            if len(price) >= 10 :
                price = "NA"
        except:
            price = ""

    return price


# Function to extract Product Rating
def get_rating(soup):
	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating


# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("span", 
			   attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count


# Function to extract Availability Status
def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = "Not Available"	

	return available	


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_type = request.form['productType']
        count = int(request.form['count'])

        # Headers for request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US'
        }

        # The webpage URL
        url = f"https://www.amazon.com/s?k={product_type}"

        # HTTP Request
        webpage = requests.get(url, headers=headers)

        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "lxml")

        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})

        # Store the links
        links_list = []

        # Loop for extracting links from Tag Objects
        for link in links:
            links_list.append(link.get('href'))

        product_details = []

        # Loop for extracting product details from each link
        for link in links_list[:count]:
            new_webpage = requests.get("https://www.amazon.com" + link, headers=headers)
            new_soup = BeautifulSoup(new_webpage.content, "lxml")

            # Extract product details
            title = get_title(new_soup)
            price = get_price(new_soup)
            rating = get_rating(new_soup)
            review_count = get_review_count(new_soup)
            availability = get_availability(new_soup)

            # Append details to the list
            product_details.append({
                "title": title,
                "price": price,
                "rating": rating,
                "review_count": review_count,
                "availability": availability
            })

        return render_template('product.html', product_details=product_details)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

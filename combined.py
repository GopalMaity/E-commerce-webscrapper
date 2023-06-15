from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
import requests
import random
from utils import userAgent
from amazon import *
from flipkart import *
from ticker import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index() :
    if request.method == "POST" :
        product_type = request.form["productType"]
        count = int(request.form['count'])
        website_choice = request.form["websiteChoice"]
        
        if website_choice == "Amazon" :
            amazon_data_json = amazonDataScrapper(product_type, count)
            if amazon_data_json is not None :
                return render_template('product.html', product_details=amazon_data_json)
        elif website_choice == "Flipkart" :
            flipkart_data_json = flipkartDataScrapper(product_type, count)
            if flipkart_data_json is not None :
                return render_template('product.html', product_details=flipkart_data_json)
        
        elif website_choice == "Ticker" :
            ticker_data_json = tickerDataScrapper(product_type)
            if ticker_data_json is not None :
                return render_template('productTicker.html', product_details=ticker_data_json)
            
    return render_template("login.html")


if __name__ == "__main__" :
    app.run(debug=True)
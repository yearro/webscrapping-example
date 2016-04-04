# -*- coding: utf-8 -*-
from flask import Flask, request
from lxml import html
from urlparse import urlparse
import json, requests

app = Flask(__name__)

@app.route("/sendUrl",methods=['POST'])
def webscraping():
    values = request.get_json()
    urlVisit = values['urlVisit']
    parsed_uri = urlparse(urlVisit)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    if domain == "http://www.vivanuncios.com.mx/":
        page = requests.get(urlVisit)
        tree = html.fromstring(page.content)

        adInformation = {}

        adTitle = tree.xpath('//span[@class="myAdTitle"]/text()')
        price = tree.xpath('//span[@class="amount"][1]/text()')
        category = tree.xpath('//a[@class="category"]//span[@itemprop="title"]/text()')
        locality = tree.xpath('//a[@itemprop="addressLocality"]/text()')
        region = tree.xpath('//a[@itemprop="addressRegion"]/text()')
        manufacturer = tree.xpath('//meta[@itemprop="manufacturer"]/@content')
        model = tree.xpath('//meta[@itemprop="model"]/@content')
        description = tree.xpath('//div[@class="description"]//span[@class="pre"]/text()');
        image = tree.xpath('//div[@class="main-bg"]//img/@src')
    
        if len(adTitle) == 1:
            adInformation["title"] = adTitle[0].strip()
        if len(price) == 1:
            adInformation["price"] = price[0].strip()
        if len(category) == 1:
            adInformation["category"] = category[0].strip()
        elif len(category) > 1:
            #One or more categories
            listCategories = list()
            temp_var = None
            if len(category) > 0:
                for item in category:
                    tempvar = " ".join(item.split())
                    listCategories.append(tempvar.strip())
            adInformation["category"] = listCategories

        if len(locality) == 1:
            adInformation["locality"] = locality[0].strip()
        if len(region) == 1:
            adInformation["region"] = region[0].strip()
        if len(manufacturer) == 1:
            adInformation["manufacturer"] = manufacturer[0].strip()
        if len(model) == 1:
            adInformation["model"] = model[0].strip()
        if len(description) == 1:
            adInformation["description"] = description[0].strip()
        if len(image) == 1:
            adInformation["image"] = image[0].strip()
    else:
        adInformation = {'error':False,'messaje':'Domain not found'}
    return json.dumps(adInformation)

if __name__ == "__main__":
    app.run(debug=True,port=5000)

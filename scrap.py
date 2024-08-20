import scrapy
import json
from scrapy.crawler import CrawlerProcess

class NoberoSpider(scrapy.Spider):
    name = "cloth_products"
    start_urls = ["https://nobero.com/pages/men/"]

    def parse(self, response):
        # Extract product links
        product_links = response.css("div.custom-page-season-grid-item a::attr(href)").getall()
        for link in product_links:
            abs_url = "https://nobero.com" + link[1:]
            self.logger.info(f"Following link: {abs_url}")
            yield response.follow(abs_url, self.parse_link1)

    
    def parse_link1(self, response):
        if response.status == 200:
            self.logger.info(f"Parsing link1: {response.url}")
            product_links = response.css("div.flex.flex-col.justify-between.h-full.relative a::attr(href)").getall()
            for link in product_links:
                abs_url = "https://nobero.com" + link
                category=response.url.split("/")[-1]
                self.logger.info(f"Following link: {abs_url}")
                yield response.follow(abs_url, self.parse_link2,meta={"category":category})
        else:
            self.logger.warning(f"Failed to retrieve link1: {response.url} with status {response.status}")

    def parse_link2(self, response):
        if response.status == 200:
            self.logger.info(f"Parsing link2: {response.url}")
            title = response.css("div.flex.justify-between.gap-2 h1::text").get()
            nav = response.css("nav.breadcrumb")
            category = response.meta['category']
            price = response.css("#variant-price ::text").get()
            mrp = response.css("#variant-compare-at-price ::text").get()
            features = response.css("#product-metafields-container div.product-metafields-values p")
            feature=[];text=[]
            description=response.css("#description_content ::text").getall()
            # for div in description:
            #     text.append(div.css("::text").get())
            
            for div in features:
                feature.append(div.css("::text").get())
            url=response.url
            color_ind=1
            colors=[]
            while True:
                color_id = f"color-{color_ind}"
                color_value = response.css(f"input#{color_id}::attr(value)").get()
            
                if color_value:
                    self.logger.info(f"Found color {color_ind}: {color_value}")
                    colors.append(color_value)
                    color_ind += 1
                else:
                    break
            script = response.css("script.product-json ::text").get()
            product_data = json.loads(script)

            available_skus = []
            skucolor = []
            skusize = []
            skuavailable=[]
            opt1='option1'
            opt2='option2'
            if product_data[0]["option1"] in ["S","M","L","XL","XXL","XXXL"]:
                opt1='option2'
                opt2='option1'
            for item in product_data:
                skucolor.append(item[opt1])
                skusize.append(item[opt2])
                skuavailable.append(item['available'])
            for ind, n in enumerate(skucolor):
                if available_skus:
                    found = False
                    for sku in available_skus:
                        if sku["color"] == n:
                            if skuavailable[ind]==True:
                                sku["size"].append(skusize[ind])
                                found = True
                                break
                    if not found:
                       if skuavailable[ind]==True: 
                        available_skus.append({"color": n, "size": [skusize[ind]]})
                       
                         
                else:
                       if skuavailable[ind]==True: 
                        available_skus.append({"color": n, "size": [skusize[ind]]})
                       

            # for ind,sku in enumerate(skucolor):
            #     for i in available_skus:
            #         if i["color"]==sku:
            #             i["size"].append(skusize[ind])
            #             i["size"]=list(set(i["size"]))
            


            if title:
                clean_title = " ".join(title.split())
                self.logger.info(f"Found title: {clean_title}")
            else:
                self.logger.warning(f"Title not found on page: {response.url}")
            yield {
                "Category":category,
                "url":url,
                "title": clean_title,
               "price": price,
            "MRP": mrp,
            "available_skus":available_skus,
            "fit":feature[0],
            "fabric":feature[1],
            "neck":feature[2],
            "sleeve":feature[3],
            "pattern":feature[4],
            "length":feature[5],
            "description":description

                
            }
        else:
            self.logger.warning(f"Failed to retrieve link2: {response.url} with status {response.status}")
process = CrawlerProcess(settings={
    "FEEDS": {
        "products.json": {"format": "json"},
    },
})

process.crawl(NoberoSpider)
process.start()

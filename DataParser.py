import re
from urllib.request import Request, urlopen
import pandas as pd
import time

class DataParser:
    def extractListings(self, pageNum):
        link = "https://www.rew.ca/properties/areas/vancouver-bc/page/{0}?ajax=true".format(pageNum)
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        
        contents = html.decode().split("""</a>\n</span>\n</div>\n</footer>\n</div>\n</div>\n</article>""")[2:-1]
        data = map(self.formatter, contents)
        return data
    
    def formatter(self, string):
        string = re.split("<|>", string.replace("\n", ""))
        data = {
            "price": string[string.index("div class=\"displaypanel-title hidden-xs\"")+1].replace(",", "")[1:],
            "address": string[string.index("ul class=\"l-pipedlist displaypanel-info\"")-1],
            "region": string[string.index("ul class=\"l-pipedlist displaypanel-info\"")+3].replace("li", ""),
            "city": string[string.index("ul class=\"l-pipedlist displaypanel-info\"")+7].replace("li", ""),
            "bedrooms": string[string.index("ul class=\"l-pipedlist\"")+3].replace(" bd", ""),
            "bathrooms": string[string.index("ul class=\"l-pipedlist\"")+7].replace(" ba", ""),
            "sqft": string[string.index("ul class=\"l-pipedlist\"")+11].replace(" sf", ""),
            "type": string[string.index("div class=\"displaypanel-info\"")+1]
        }
        return data

    def parsePages(self, pageRange):
        output = []
        for i in pageRange:
            output += self.extractListings(i)
            time.sleep(3)
        return output

    def readData(self):
        for i in range(5):
            start, end = 1+i*5, 6+i*5
            print("sending request for pages {0} to {1}\n".format(start, end-1))
            listings = self.parsePages(range(start, end))
            df = pd.DataFrame(columns=["price", "sqft", "bathrooms", "bedrooms", "type", "region", "address", "city"])
            for listing in listings:
                df = df.append(listing, ignore_index=True)
            df.to_csv("data/vancouver_data_{0}.csv".format(i), sep='\t', index=None)
            print("collected data from pages {0} to {1}\n".format(start, end-1))
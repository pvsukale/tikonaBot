import scrapy
import json,ast
import pandas,numpy
import re


p = re.compile('[A-Z]*: [0-9]GB')

def getLimit(x):
    x = x.strip()

    if('Post' in x and 'GB' in x):
        return x
    elif(p.match(x)):
        return x

def getGBs(x):
    temp = []
    for i in x:
        if i.isdigit():
            temp.append(i)
    return int(''.join(temp))


def getAllPlans(x):
    x = x.strip()

    if('Mbps' in x):
        return x

def getTypeOfPlan(x):
    x = x.strip()
   # x = x.split()

    if((', UL' in x )or (', DUL' in x)):
        x = x.split()
        return x[1]

class tikonaSpider(scrapy.spiders.Spider):
    name = "tikonaset_spider"
    start_urls = ['http://www.tikona.in/for-home/broadband-plans/plans/Pune/tariff-plans']

    def parse(self,response):
        SET_SELECTOR = '.slides'

        for tikonaPlans in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'div.views-field div ::text'
            PRICE_SELECTOR = 'div.views-field-field-price span.field-content ::text'

            planDetails = ast.literal_eval(json.dumps(tikonaPlans.css(NAME_SELECTOR).extract()))
            priceDetails = ast.literal_eval(json.dumps(tikonaPlans.css(PRICE_SELECTOR).extract()))

            #For name of plan
            eachPlan = map(getAllPlans,planDetails)
            plans = list( filter((lambda x: (x!=None) and ('@' not in x)) , eachPlan) )

            #For type of plan
            typeList = map(getTypeOfPlan,planDetails)
            finalType = list(filter((lambda x:x!=None),typeList))

            #For limit:
            limitType = map(getLimit,planDetails)
            finalLimit = list( filter((lambda x:x!=None),limitType) )
            limit = map(getGBs,finalLimit)
            limit.insert(0,'Unlimited')

            #defining dataframe
            result = {
                'Plan_Name':pandas.Series(plans),
                'Plan_type':pandas.Series(finalType),
                'Price':pandas.Series(priceDetails)
            }

            df = pandas.DataFrame(result)
            df = df.fillna('Post Limit')
            df['Limit [GBs]'] = pandas.Series(limit)

            df.to_csv('out_data.csv',index=False)
            print df
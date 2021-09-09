import pymongo
from pymongo import MongoClient
import pandas as pd
import json
from urllib.parse import unquote

class dis_pharma_db():
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client.dis_pharma
   
    def insertDatatoNewProductfromTamperMonkey(self, record):
        db = self.client.dcs_cosmetics_fda.new_products_from_tampermonkey
        if (len(record) % 5 == 0) and (len(record) != 0) :
            for i in range(int(len(record)/5)):
                # if db.count_documents({'applySn':record.get('applySn'), 'url':record.get('url'), 'enterpriseName':record.get('enterpriseName'), 'date':record.get('date'), 'productname': record.get('productname')}) > 0:
                if db.count_documents({'applySn':record.get('records[' + str(i) + '][applySn]'), 'url':record.get('records[' + str(i) + '][url]'), 'enterpriseName':record.get('records[' + str(i) + '][enterpriseName]'), 'date':record.get('records[' + str(i) + '][date]'), 'productname': record.get('records[' + str(i) + '][productname]')}) > 0:
                    print(record.get('records[' + str(i) + '][url]'), 'already in new product')
                else:
                    # db.insert_one({'applySn':record.get('applySn'), 'url':record.get('url'), 'enterpriseName':record.get('enterpriseName'), 'date':record.get('date'), 'productname': record.get('productname')})
                    db.insert_one({'applySn':record.get('records[' + str(i) + '][applySn]'), 'url':record.get('records[' + str(i) + '][url]'), 'enterpriseName':record.get('records[' + str(i) + '][enterpriseName]'), 'date':record.get('records[' + str(i) + '][date]'), 'productname': record.get('records[' + str(i) + '][productname]')})
            return ''
        else:
            return ''
    
    def insertDatatoIngredientsfromTamperMonkey(self, record):
        db = self.client.dcs_cosmetics_fda.ingredients_from_tampermonkey
        manufacture = record.get('manufactures').replace('"', '').replace('[', '').replace(']', '')
        if db.count_documents({'processid': record.get('processid'), 'productname': record.get('productname'), 'ingredients_lt': record.get('ingredients_lt'), 'brandowner': record.get('brandowner'), 'manufactures': manufacture, 'cancellation': record.get('cancellation')}) > 0:
            print(record.get(''))
        else:
            db.insert_one({'processid': record.get('processid'), 'productname': record.get('productname'), 'ingredients_lt': record.get('ingredients_lt'), 'brandowner': record.get('brandowner'), 'manufactures': manufacture, 'cancellation': record.get('cancellation')})
        print(record)
    
    def deleteDatafromnewproducts(self, record):
        db = self.client.dcs_cosmetics_fda.new_products
        result = db.delete_one({'url':{'$regex':record.get('processid')}})
        print(result.deleted_count)

    def insertDatatoPEGUSCHNfromTamperMonkey(self, record):
        data = json.loads([a for a in record.keys()][0])
        if data.get('drug') != "":
            drug = unquote(data .get('drug'))
            data['drug'] = drug
            if self.db['PEG_US_CHN_from_tampermonkey'].count_documents({'registration': data.get('registration'), 'drug': data.get('drug')}) > 0:
            # if self.db['PEG_US_PEG_US_CHN_from_tampermonkey'].count_documents({'registration': data.get('registration'), 'drug': data.get('drug')}) > 0:
                pass
            else:
                self.db['PEG_US_CHN_from_tampermonkey'].insert_one(data)
                # self.db['PEG_US_PEG_US_CHN_from_tampermonkey'].insert_one(data)
                print(record)

    def insertqichacha(self, record, databasename):
        data = json.loads(record.replace('\\', ','), strict=False)
        # if self.client.dcs_scrm.company_info_qichacha.count_documents({'公司名称':data.get('公司名称')}) > 0:
        #     pass
        # else:
        #     self.client.dcs_scrm.company_info_qichacha.insert_one(data)
        if self.client[databasename].company_info_qichacha.count_documents({'公司名称':data.get('公司名称')}) > 0:
            pass
        else:
            self.client[databasename].company_info_qichacha.insert_one(data)
        print(databasename, data)

    def insertDatatoLazadaProductfromTamperMonkeyNew(self, record):
        db = self.client.dcs_phl_sealant.lazada_products_202109
        print(record)
        # json.loads(record.get('data'))
        url = record.get('url')
        if db.count_documents({'url':url}) > 0:
            print('already exists')
            pass
        else:
            db.insert_one({'url':url, 'data':json.loads(record.get('data'))})
            print(url, 'done')

    
    def insertDatatoLazadaProductfromTamperMonkey(self, record):
        db = self.client.dcs_phl_sealant.lazada_products
        if (len(record) % 10 == 0) and (len(record) != 0) :
            for i in range(int(len(record)/10)):
                if record.get('records[' + str(i) + '][brand]') != '':
                    if db.count_documents({'brand':record.get('records[' + str(i) + '][brand]'), 
                                        'productname': record.get('records[' + str(i) + '][productname]'),
                                        'icon_shop': record.get('records[' + str(i) + '][icon_shop]'),
                                        'url':record.get('records[' + str(i) + '][url]'),
                                        'price_cur':record.get('records[' + str(i) + '][price_cur]'), 
                                        'price_org':record.get('records[' + str(i) + '][price_org]'), 
                                        'icon_ship':record.get('records[' + str(i) + '][icon_ship]'), 
                                        'comment_cnt':record.get('records[' + str(i) + '][comment_cnt]'), 
                                        'country':record.get('records[' + str(i) + '][country]'), 
                                        'stars':record.get('records[' + str(i) + '][stars]')
                                        }) > 0:
                        print(record.get('records[' + str(i) + '][url]'), 'already in new product')
                    else:
                        db.insert_one({'brand':record.get('records[' + str(i) + '][brand]'), 
                                        'productname': record.get('records[' + str(i) + '][productname]'),
                                        'icon_shop': record.get('records[' + str(i) + '][icon_shop]'),
                                        'url':record.get('records[' + str(i) + '][url]'),
                                        'price_cur':record.get('records[' + str(i) + '][price_cur]'), 
                                        'price_org':record.get('records[' + str(i) + '][price_org]'), 
                                        'icon_ship':record.get('records[' + str(i) + '][icon_ship]'), 
                                        'comment_cnt':record.get('records[' + str(i) + '][comment_cnt]'), 
                                        'country':record.get('records[' + str(i) + '][country]'), 
                                        'stars':record.get('records[' + str(i) + '][stars]')
                        })
                else:
                    if db.count_documents({ 
                                        'url':record.get('records[' + str(i) + '][url]'),
                                        }) > 0:
                        print(record.get('records[' + str(i) + '][url]'), 'already in new product')
                    else:
                        db.insert_one({'brand':record.get('records[' + str(i) + '][brand]'), 
                                        'productname': record.get('records[' + str(i) + '][productname]'),
                                        'icon_shop': record.get('records[' + str(i) + '][icon_shop]'),
                                        'url':record.get('records[' + str(i) + '][url]'),
                                        'price_cur':record.get('records[' + str(i) + '][price_cur]'), 
                                        'price_org':record.get('records[' + str(i) + '][price_org]'), 
                                        'icon_ship':record.get('records[' + str(i) + '][icon_ship]'), 
                                        'comment_cnt':record.get('records[' + str(i) + '][comment_cnt]'), 
                                        'country':record.get('records[' + str(i) + '][country]'), 
                                        'stars':record.get('records[' + str(i) + '][stars]')
                                        })
            return ''
        else:
            return ''
    
    def insertDatatoLazadaProductDetailfromTamperMonkey(self, record):
        db = self.client.dcs_phl_sealant.lazada_products_detail_raw
        url = record.get('url')
        url = url[0:url.find('.html?')+6] + 'search=1'
        extract_date = record.get('extract_date')
        if db.count_documents({'url':url, 'extract_date': extract_date}) > 0:
            print('already exists')
            pass
        else:
            db.insert_one(record)
            print(url, 'done')
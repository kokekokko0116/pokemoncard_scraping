# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector


class PokemoncardPipeline:
    def process_item(self, item, spider):
        return item

class MYSQLPipeline:
    
    def process_item(self, item, spider):
        self.conn = mysql.connector.connect(host='localhost',database='scraping',user='scraper',password='root')
        self.c = self.conn.cursor(prepared =True)
        
        series_number = item.get('series_number')
        series_name = item.get('series_name')
        number = item.get('number')
        name = item.get('name')
        price = item.get('price')
        rarerity = item.get('rarerity')

        self.c.execute("SELECT * FROM pokemoncard_test WHERE series_name = %s AND number = %s", (series_name,number,))
        result = self.c.fetchone()
        if result is not None:
            data=list(result)
            mysql_id =data[0]
            x =data[5].split(',')
            x.insert(0,price)
            update_price = ','.join(x)
            
            self.c.execute("UPDATE pokemoncard_test SET price = %s WHERE id = %s", (update_price,data[0],))
            self.conn.commit()

        else:
            self.query = "insert into pokemoncard_test(series_number, series_name, number, name, price, rarerity)values(%s,%s,%s,%s,%s,%s)"
            self.item =(series_number,series_name,number,name, price,rarerity)
            self.c.execute(self.query, self.item)
            self.conn.commit()
            
    def close_spider(self, spider):
        self.conn.close()
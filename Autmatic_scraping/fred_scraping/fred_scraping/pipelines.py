# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='At070077&',  # add your password here if you have one set
            database='fredDatabase'
        )

        # Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        # create fredData table if none exists
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS freddata(
                id int NOT NULL auto_increment, 
                DATE VARCHAR(255),
                company_name VARCHAR(255),
                value FLOAT,
                PRIMARY KEY (id)
            )
        """)

    def process_item(self, item, spider):
        # Assuming the keys in your data are "DATE" and "CORESTICKM159SFRBATL"
        self.cur.execute("""
            INSERT INTO freddata (
                DATE,
                company_name,
                value
            ) VALUES (%s, %s, %s)
        """, (
            item.get('DATE'),
            item.get('company_name'),  # Adjust based on your actual data
            item.get('value')  # Adjust based on your actual data
        ))

        # Execute insert of data into the database
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # Close cursor & connection to the database
        self.cur.close()
        self.conn.close()


from lxml import etree
import os
import sqlite3

def xml_to_db():
        
    database = "/home/phil/Documents/DevOps/SQLiteAI/azureVersion/backend/zap.db"
    connection = None
    tree = etree.parse(os.getcwd() + '/azureVersion/output/report.xml')
    root = tree.getroot()
    alerts = root.xpath("//alertitem/alert")
    riskcode = root.xpath("//alertitem/riskcode")
    affected_url = root.xpath("//alertitem/instances/instance/uri")
    site=root.find(".//site")

    try:
        connection = sqlite3.connect(database)
        print("Connection to SQLite3 database established")
        cursor = connection.cursor()

        for alerts, riskcode, affected_url in zip(alerts, riskcode, affected_url):
            # print(f"Alert: {alerts.text}")
            # print(f"RiskCode: {riskcode.text}")
            # print(f"Url: {affected_url.text}")
            alert_text=alerts.text
            riskcode_text=riskcode.text
            affected_url_text=affected_url.text
            site_url=site.get("name")    
            # print(site_url)
            site_url_str = str(site_url)
            # print(site_url_str)
            insert_query = "INSERT INTO alerts (site_name, alerts, riskcode, affected_url) VALUES (?, ?, ?, ?)"
            cursor.execute(insert_query, (site_url_str, alert_text, riskcode_text, affected_url_text))
            connection.commit()
            # print('XMLtoDB.py worked')
    except sqlite3.Error as error:
        print(f"Error: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed")
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:18:25 2020

@author: piphi
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import urllib


class Worldometer_Scraper:
    def __init__(self, output_path):
        self.path = output_path
        world_o_meter_url = "https://www.worldometers.info/coronavirus/"
        self.table_list = []
        req = urllib.request.Request(
            world_o_meter_url, headers={"User-Agent": "Magic Browser"}
        )
        world_o_meter_page = urllib.request.urlopen(req).read()
        self.world_o_meter_soup = BeautifulSoup(world_o_meter_page, "html.parser")

    def run_scraper(self):
        first_row = self.world_o_meter_soup.find("thead")
        categories = [a.text for a in first_row.find_all("th")]
        self.table_list.append(categories)

        table = self.world_o_meter_soup.find("tbody")
        rows = table.find_all("tr", {"style": ""})

        for row in rows:

            temp_list = [a.text for a in row.find_all("td")]

            # clean a bit of the data
            for i in range(0, len(temp_list)):
                temp = temp_list[i]
                if temp:
                    temp_list[i] = temp.rstrip()

            self.table_list.append(temp_list)

        self._to_csv()

    def _to_csv(self):
        with open(self.path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.table_list)
        print("completed!")


if __name__ == "__main__":
    scraper = Worldometer_Scraper("worldometer.csv")
    scraper.run_scraper()

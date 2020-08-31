# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 12:05:02 2020

This is a web scraper for CNN's search site to find articles
about Covid-19

@author: piphi
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import csv
import pickle
import re
import time
import threading
import zipfile
import os
import pathlib


class Article:
    def __init__(self, name, date, url, content):
        if type(name) is not str:
            raise ValueError("The name passed is not a string")
        self.name = name

        if type(date) is not str:
            raise ValueError("Please pass the date as a string")
        self.date = date

        if type(url) is not str:
            raise ValueError("Please pass the URL as a string")
        self.url = url

        if type(content) is not str:
            raise ValueError("Please pass the content of the article as a string")
        self.content = content

    def __str__(self):
        return (
            "Article Title: "
            + self.name
            + ", Posted On: "
            + self.date
            + ", At: "
            + self.url
        )

    def __eq__(self, obj):
        return (
            isinstance(obj, Article) and self.name == obj.name and obj.url == self.url
        )

    def to_txt(self, path: str):
        filename = path + re.sub(r"[\s?\"\\/\*\:\<\>|]", "", self.name) + ".txt"
        # print(filename)
        with open(filename, "wb") as file:
            file.write(self.__str__().encode("utf8"))
            file.write(("\n" + self.content).encode("utf8"))


class CNN_Scraper:
    timeout = 10  # should give up trying to load page after 10 seconds

    def __init__(self, output_path):
        if type(output_path) is not str:
            raise TypeError("Please input a string")
        self.url = (
            "https://edition.cnn.com/search/?size=10&q=coronavirus%20measures&page=1"
        )
        self.path = output_path

    def _load_CNN_page(self, url, driver):

        driver.get(url)
        loaded_frame = driver.find_elements_by_xpath("html[@data-triggered='true']")

        while len(loaded_frame) < 1:
            time.sleep(0.5)
            loaded_frame = driver.find_elements_by_xpath("html[@data-triggered='true']")

    def _get_CNN_soup(self, url):

        path = os.path.dirname(os.path.abspath(__file__)) + "\\chromedriver.exe"

        driver = webdriver.Chrome(executable_path=path)
        try:
            threading.Timer(self.timeout, self._load_CNN_page(url, driver))
        except Exception:
            print("Initial load failed... trying again")
            self._load_CNN_page(url, driver)

        page = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
        return page

    def _get_total_results(self):
        CNN_soup = self._get_CNN_soup(self.url)

        results = CNN_soup.find("div", {"class": "cnn-search__results-count"})
        total = re.search(r"\d+(?= for)", results.text)
        return int(total.group())

    def run(self):
        try:

            total_results = self._get_total_results()
        except Exception:
            print("Total results didn't show.. trying again")
            total_results = self._get_total_results()
        pagenum = 1

        while (pagenum * 10) <= int(total_results):
            url = (
                "https://edition.cnn.com/search/?size=10&q=coronavirus%20measures&page="
                + str(pagenum)
                + "&from="
                + str(10 * (pagenum - 1))
            )
            print("Moving to next page:")
            print(url)
            CNN_soup = self._get_CNN_soup(url)

            articles = CNN_soup.find_all(
                "div", {"class": "cnn-search__result cnn-search__result--article"}
            )

            for article in articles:
                title = article.find("h3", {"class": "cnn-search__result-headline"})
                article_url = "https:" + title.find_all("a", href=True)[0]["href"]

                if "live-news" in article_url:
                    self._CNN_live_news(article_url)
                else:
                    content = article.find("div", {"class": "cnn-search__result-body"})
                    date = article.find(
                        "div", {"class": "cnn-search__result-publish-date"}
                    )
                    date = re.search(r".+(?=\n)", date.text).group()
                    update = Article(
                        title.text.lstrip(), date, article_url, content.text
                    )
                    self._update_list(update)

            pagenum += 1
        self._to_output()

    def _CNN_live_news(self, url):
        if type(url) is not str and "live-news" not in url:
            raise ValueError("Please enter a proper live-news url")
        try:
            CNN_page = urlopen(url).read()
        except Exception:
            print("failed to load live news ... trying again")
            CNN_page = urlopen(url).read()
        CNN_soup = BeautifulSoup(CNN_page, "html.parser")
        tags = CNN_soup.find_all(
            "article",
            {
                "class": "Box-sc-1fet97o-0-article poststyles__PostBox-sc-1egoi1-0 iNLWiE"
            },
        )

        date = re.search(r"\d{2}-\d{2}-\d{2}", url)

        for post in tags:

            name = post.find(
                "h2", {"class": "post-headlinestyles__Headline-sc-2ts3cz-1 gzgZOi"}
            )
            content = post.find(
                "div",
                {
                    "class": "Box-sc-1fet97o-0 render-stellar-contentstyles__Content-sc-9v7nwy-0 ivqjEu"
                },
            )
            if date and name and content and name.text and content.text:

                update = Article(name.text, date.group(), url, content.text)
                self._update_list(update)

    def _to_output(self):
        article_list = []
        i = 1
        with open("article.pickle", "rb") as pickle_in:
            articles = pickle.load(pickle_in)
        for article in articles:
            article_list.append([i, article.name, article.url])
            try:
                article.to_txt(self.path + str(i) + " ")

            except OSError:
                print(article.name + " failed to output")
            i += 1

        csv_path = self.path + "articles.csv"
        if not os.path.exists(csv_path):
            with open(csv_path, "w+") as file:
                writer = csv.writer(file)
                writer.writerows(["Number", "Name", "URL"])

        with open(csv_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(article_list)

    def _update_list(self, article):

        # loads in previous articles
        path = os.path.dirname(os.path.abspath(__file__)) + "\\article.pickle"
        pickle_in = open(path, "rb")
        article_list = pickle.load(pickle_in)
        pickle_in.close()

        if article not in article_list:
            article_list.append(article)
            print(article)

        pickle_out = open("article.pickle", "wb")
        pickle.dump(article_list, pickle_out)
        pickle_out.close()

    def get_name(self):
        return "CNN Scraper"


if __name__ == "__main__":
    CNN_scraper = CNN_Scraper(
        "C:\\Users\\piphi\\Documents\\CoronaVirusScraper\\CoronaVirusScraper\\articles\\"
    )
    CNN_scraper.run()

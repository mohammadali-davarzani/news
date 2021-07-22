import re
import csv
import time
import requests
import schedule
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse as change_url
from elasticsearch import Elasticsearch

from news_scraping.irna import irna_class
from news_scraping.sena import sena_class
from news_scraping.boursepress import bourse_press



es = Elasticsearch()

active_sources = list()
source_id_take = es.search(index="news_sources", body=
    {
    "query": {"match": {
        "is_active": True
    }}
    }
)

if len(source_id_take['hits']['hits']) > 0:
    for hit in source_id_take['hits']['hits']:
        active_sources.append(int(hit["_id"]))

test_news_urls = list()

news_url_take = es.search(index="news_contents", body=
    {
    "query": {"match_all": {}}
    }
)

if len(news_url_take['hits']['hits']) > 0:
    for hit in news_url_take['hits']['hits']:
        test_news_urls.append("%(news_url)s" % hit["_source"])

old_news_urls = list()

for old_url in test_news_urls:
    old_news_urls.append(change_url.unquote(old_url))



boursepress = bourse_press.output()
irna = irna_class.output()
sena = sena_class.output()


confirmed_date_times = list()
confirmed_titles = list()
confirmed_images = list()
confirmed_leads = list()
confirmed_contents = list()
confirmed_urls = list()
confirmed_sources = list()


if 1 in active_sources:
    for accepted in range(len(boursepress[-1])):
        if change_url.unquote(boursepress[-1][accepted]) not in old_news_urls:
            confirmed_date_times.append(boursepress[0][accepted])
            confirmed_titles.append(boursepress[1][accepted])
            confirmed_images.append(boursepress[2][accepted])
            confirmed_leads.append(boursepress[3][accepted])
            confirmed_contents.append(boursepress[4][accepted])
            confirmed_urls.append(change_url.unquote(boursepress[-1][accepted]))
            confirmed_sources.append("بورس پرس")



if 2 in active_sources:
    for accepted in range(len(irna[-1])):
        if change_url.unquote(irna[-1][accepted]) not in old_news_urls:
            confirmed_date_times.append(irna[0][accepted])
            confirmed_titles.append(irna[1][accepted])
            confirmed_images.append(irna[2][accepted])
            confirmed_leads.append(irna[3][accepted])
            confirmed_contents.append(irna[4][accepted])
            confirmed_urls.append(change_url.unquote(irna[-1][accepted]))
            confirmed_sources.append("ایرنا")


if 3 in active_sources:
    for accepted in range(len(sena[-1])):
        if change_url.unquote(sena[-1][accepted]) not in old_news_urls:
            confirmed_date_times.append(sena[0][accepted])
            confirmed_titles.append(sena[1][accepted])
            confirmed_images.append(sena[2][accepted])
            confirmed_leads.append(sena[3][accepted])
            confirmed_contents.append(sena[4][accepted])
            confirmed_urls.append(change_url.unquote(sena[-1][accepted]))
            confirmed_sources.append("سنا")


for i in range(len(confirmed_titles)):

    data = {
        "news_source":str(confirmed_sources[i]),
        "news_url":str(confirmed_urls[i]),
        "news_date_time":str(confirmed_date_times[i]),
        "news_title":str(confirmed_titles[i]),
        "news_image":str(confirmed_images[i]),
        "news_lead":str(confirmed_leads[i]),
        "news_contents":str(confirmed_contents[i]),
        "is_duplicate":False,
        "is_disable":False
    }

    add_data = es.index(index="news_contents", body=data)


res = es.search(index="news_contents", body=
    {
    "query": {"match_all": {}}
    }
)

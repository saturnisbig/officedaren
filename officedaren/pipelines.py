# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import sqlite3
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class JsonPipeline(object):

    def __init__(self):
        self.file = codecs.open('examwd.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class SQLiteStorePipeline(object):
    filename = 'data.sqlite'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        self.conn.execute("""insert into office_article(aid, category, title,
                          content) values(?, ?, ?, ?)""",
                          (item['aid'], item['category'], item['title'],
                           item['content']))
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        #conn.execute("""create table article
        #             (aid varchar(50) primary key, title varchar(255),
        #             content text, pub_date datetime)""")
        #self.create_category(conn)
        self.create_article(conn)
        return conn

    def create_category(self, conn):
        sql = """CREATE TABLE "office_category" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "name" varchar(200) NOT NULL,
        "slug" varchar(50) NOT NULL UNIQUE,
        "description" text NOT NULL
        )"""
        conn.execute(sql)

    def create_article(self, conn):
        rel_sql = """CREATE TABLE "office_article_categories" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "article_id" integer NOT NULL,
        "category_id" integer NOT NULL REFERENCES "office_category"("id"),
        UNIQUE ("article_id", "category_id")
        )"""
        a_sql = """CREATE TABLE "office_article" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "aid" varchar(50) NOT NULL UNIQUE,
        "category" varchar(100) NOT NULL,
        "title" varchar(255) NOT NULL,
        "content" text NOT NULL,
        "pub_date" timestamp NOT NULL DEFAULT(datetime('now', '+8 hour'))
        )"""
        conn.execute(a_sql)
        #conn.execute(rel_sql)



import json
import mysql.connector
import ast
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_cors import CORS

from flaskext.mysql import MySQL
import mysql.connector
import ast
from webscraper_FINAL_MYSQL import scrape_amazon
from scrapfly_webscraper import run
from TEST_data_to_JSON import outputtojson
from TEST_data_to_REMOVEBUTTON import removeproduct
from TEST_data_to_SQL_keyword import outputkeywordsort
from table1FINAL_MYSQL1 import keywordtable
from table1FINAL_MYSQL2 import keywordtable1
from table1FINAL_MYSQL3 import allreviewtable
from livereload import Server
import time
import json
import asyncio
from TEST_vine_to_SQL import vinefilter
from TEST_marketplace_to_SQL import marketplacefilter
import datetime
from collections import defaultdict
from operator import itemgetter

from table2FINAL_MYSQL import individual_keyword
keyword = 'good'
individual_keyword(keyword)
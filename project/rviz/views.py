import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime
import django
import os
import time
from django.shortcuts import render
from models import *

# Create your views here.
def scrape_arxiv(arxiv_id):
	"""
	Using the id of a paper from arxiv, scrape it and save it to the database
	"""
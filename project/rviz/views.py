import sys
import os
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import django
from django.shortcuts import render
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team26.settings')
django.setup()

import time
from rviz.models import ResearchPaper, Author

# Create your views here.
def scrape_arxiv(arxiv_id):
	"""
	Using the id of a paper from arxiv, scrape it and save it to the database
	"""
	pass

def get_relational_data():
	# through model contains the relationships between objects in db
	citation_model = ResearchPaper.citations.through
	citations = citation_model.objects.all()

	citation_pairs = citation_model.objects.values_list('from_researchpaper_id', 'to_researchpaper_id')
	print(f"citation relations: {citation_pairs}, obj: {type(citation_pairs)}")
	return citation_pairs

""" FORMATTING
def get edges from db:
	# query the edges and relationship from postgre

def send edges:
	# array of relationships to front end
	# 		must be k, v pair
	
def send papers:
	# general query  from DB
"""

""" CONTROLS FOR FRONT END
def init load:
	# loads a discrete num of papers from DB
	
def filter:
	# post req for filtering data

def upload:
	# post req for adding papers
"""

""" LATER
def parse uploaded paper:
	# finds citations, etc
"""

# add quants to models
# add function to query database for sheen

# fix git connection

def main():
	get_relational_data()

if __name__ == '__main__':
	main()
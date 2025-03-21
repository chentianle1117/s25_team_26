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
	for parent, child in citation_pairs:
		print(f"parent: {parent}, child: {child}")
	print(f"citation relations: {citation_pairs}, obj: {type(citation_pairs)}")
	return citation_pairs

def scrape_arxiv_paper(arxiv_id):
	api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"

	time.sleep(1)

	try:
		response = requests.get(api_url)
		response.raise_for_status()

		root = ET.fromstring(response.content)
		ns = {"atom": "http://www.w3.org/2005/Atom",
			  "arxiv": "http://export.arxiv.org/schemas/atom",}

		entry = root.find(".//atom:entry", ns)

		if not entry:
			print(f"No paper found with id: {arxiv_id}")
			return None

		title = entry.find("atom:title", ns).text.strip()
		print(f"Article title: {title}")
		abstract = entry.find("atom:summary", ns).text.strip()
		print(f"Article abstract: {abstract}")

		doi_element = entry.find(".//arxiv.doi", ns)
		doi = doi_element.text if doi_element else None
		print(f"Article doi: {doi}")

		published_text = entry.find("atom:published", ns).text
		print(f"Article published: {published_text}")
		publication_date = datetime.strptime(published_text[:10], "%Y-%m-%d").date()
		print(f"\t\tdate: {published_text}")

		url = entry.find('./atom:link[@rel="alternate"]', ns).get("href")
		print(f"article url: {url}")

		# TODO: add paper to DB, for now just get data
		# paper, created = ResearchPaper.objects.update_or_create(
		# 	doi=doi if doi else f"arxiv:{arxiv_id}",
		# 	defaults={
		# 		'title': title,
		# 		'abstract': abstract,
		# 		'publication_date': publication_date,
		# 		'url': url,
		# 		'source_site': 'arxiv'
		# 	}
		# )

		# Extract and add authors
		author_elements = entry.findall('atom:author', ns)
		for author_element in author_elements:
			author_name = author_element.find('atom:name', ns).text
			print(f"author: {author_name}")

		# Extract categories/keywords
		categories = []
		for category in entry.findall('.//arxiv:category', ns):
			categories.append(category.get('term'))

		print(f"categories: {categories}")

		# paper.save()
	except requests.exceptions.RequestException as e:
		print(f"Error fetching paper {arxiv_id}: {e}")
	except Exception as e:
		print(f"Error processing paper {arxiv_id}: {e}")

	return None

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
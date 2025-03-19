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
import argparse

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
		else:
			print(f"Full entry:\n{entry}")

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
		paper, created = ResearchPaper.objects.update_or_create(
			doi=doi if doi else f"arxiv:{arxiv_id}",
			defaults={
				'title': title,
				'publication_date': publication_date,
				'url': url,
			}
		)

		print(f"paper: {paper}")

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

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--id',
		help="enter the arxiv id of the article to scrape",
		type=str,
	)
	args = parser.parse_args()
	print(f"Attempting to scrape paper with Arxiv ID: {args.id}")
	scrape = scrape_arxiv_paper(args.id)

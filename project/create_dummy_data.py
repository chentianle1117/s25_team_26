import os
import sys
import django
import random
from datetime import date, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "team26.settings")

django.setup()

from rviz.models import Author, ResearchPaper


def create_dummy_data(num_authors=5, num_papers=10):
	print(f"Creating {num_authors} authors and {num_papers} papers")

	# Fix the random name selection
	first_names = ["David", "Sheen", "Graham"]
	last_names = ["Chen", "Cao", "Felton"]

	authors = []
	for i in range(num_authors):
		# Use random.choice instead of indexing with randint
		name = f"{random.choice(first_names)} {random.choice(last_names)}"
		author = Author.objects.create(name=name)
		authors.append(author)
		print(f"Created author: {author.name}")

	papers = []
	for i in range(num_papers):
		title = f"Test paper {i}"
		days_back = random.randint(0, 5 * 365)
		pub_date = date.today() - timedelta(days=days_back)
		url = f"https://arxiv.org/{abs(hash(title))}"
		doi = f"{abs(hash(title))}"  # Simplified DOI generation

		paper = ResearchPaper.objects.create(
			title=title,
			publication_date=pub_date,
			url=url,
			doi=doi,
		)

		# Add random authors (1-3)
		num_paper_authors = min(random.randint(1, 3), len(authors))
		paper_authors = random.sample(authors, num_paper_authors)
		paper.authors.add(*paper_authors)

		paper.zotero_id = f"ITEM-{random.randint(1000, 9999)}"
		paper.save()

		papers.append(paper)
		print(f"Created paper: {paper.title}")

	# Add citations
	for paper in papers:
		num_citations = random.randint(0, 5)
		if num_citations > 0:
			# Don't cite yourself
			potential_citations = [p for p in papers if p != paper]
			if potential_citations:
				citations = random.sample(
					potential_citations,
					min(num_citations, len(potential_citations))
				)
				paper.citations.add(*citations)
				print(f"Added {len(citations)} citations to {paper.title}")


if __name__ == '__main__':
	create_dummy_data()
	print("Done creating dummy data")
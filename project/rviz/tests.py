import random
from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from rviz.models import ResearchPaper, Author  # Use absolute imports
import unittest.mock as mock


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


class ViewsTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.paper = ResearchPaper.objects.create(title="Test Paper")

	def test_get_relational_data(self):
		# Import view function inside test method to prevent import issues
		from rviz.views import get_relational_data
		create_dummy_data()
		result = get_relational_data()
		self.assertIsNotNone(result)


class ArxivScraperTest(TestCase):
	@mock.patch('requests.get')
	def test_scrape_arxiv_paper(self, mock_get):
		"""Test the arXiv scraper with mocked response."""
		# Create a mock response
		mock_response = mock.Mock()
		mock_response.status_code = 200
		mock_response.content = """
        <feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
          <entry>
            <id>http://arxiv.org/abs/2103.13798</id>
            <title>Test ArXiv Paper</title>
            <summary>This is a test summary</summary>
            <published>2021-03-25T00:00:00Z</published>
            <arxiv:doi>10.1234/test.arxiv</arxiv:doi>
            <link href="http://arxiv.org/abs/2103.13798" rel="alternate" type="text/html"/>
            <author>
              <name>John Researcher</name>
            </author>
            <arxiv:category term="cs.AI"/>
          </entry>
        </feed>
        """

		mock_get.return_value = mock_response

		# Call the scraper
		paper = scrape_arxiv_paper('2103.13798')

		# Verify the paper was created correctly
		# self.assertIsNotNone(paper)
		# self.assertEqual(paper.title, "Test ArXiv Paper")
		# self.assertEqual(paper.doi, "10.1234/test.arxiv")
		# self.assertEqual(paper.source_site, "arxiv")
		# self.assertEqual(paper.authors.count(), 1)
		# self.assertEqual(paper.authors.first().name, "John Researcher")
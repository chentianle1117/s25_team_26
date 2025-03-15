from django.db import models

class Author(models.Model):
	"""
	Author model for, you guessed it, the author of the paper
	"""
	name = models.CharField(max_length=200)

	def __repr__(self):
		return f"Author: {self.name}"

class ResearchPaper(models.Model):
	"""
	Research paper model representing the meta data for papers taken from https://www.arXiv.org
	"""
	### Basic Data ###
	title = models.CharField(max_length=500)
	publication_date = models.DateField(blank=True, null=True)
	authors = models.ManyToManyField(Author, related_name='papers')
	url = models.URLField(blank=True, null=True)
	doi = models.CharField(max_length=255, blank=True, null=True)

	### Relational - Citations ###
	# citations reference other ResearchPaper objects
	citations = models.ManyToManyField('self', symmetrical=False, related_name='cited_by', blank=True)

	### Zotero ###
	zotero_id = models.CharField(max_length=255, blank=True, null=True)


	# dummy data
	# format to something acceptable by the front end
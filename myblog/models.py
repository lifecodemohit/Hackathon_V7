from django.db import models

# Create your models here.
class Question(models.Model) :
	user_name = models.CharField(max_length=200)
	heading = models.TextField()
	main_text = models.TextField()
	pub_date = models.DateTimeField(auto_now=True)
	votes = models.IntegerField(default = 0)
	views = models.IntegerField(default = 0)
	num_answers = models.IntegerField(default = 0)
	hash_tag = models.CharField(max_length=2000)
	votes_user = models.TextField()
	views_user = models.TextField()
	def __unicode__(self):  # Python 3: def __str__(self):
		return self.heading

class Comment(models.Model) :
	comment_link_id = models.ForeignKey(Question)
	comment_user_name = models.CharField(max_length=200)
	comment_main_text = models.TextField()
	comment_pub_date = models.DateTimeField(auto_now=True)
	comment_votes = models.IntegerField(default = 0)
	comment_votes_user = models.TextField()
	def __unicode__(self):  # Python 3: def __str__(self):
		return self.comment_link_id
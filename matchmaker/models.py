from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Musician(models.Model):
	BEGINNER = 'A'
	INTERMEDIATE = 'I'
	PROFESSIONAL = 'P'
	LEVELS = (
		(BEGINNER, 'Beginner'),
		(INTERMEDIATE, 'Intermediate'),
		(PROFESSIONAL, 'Professional'),
	)

	user = models.OneToOneField(User, on_delete=models.PROTECT)
	level = models.CharField(max_length=1, choices=LEVELS, blank=True)
	firstaccess = models.BooleanField(default=True)

	@classmethod
	def create(cls, user):
		return cls(user=user)

	def __str__(self):
		return self.user.username
		
	def __unicode__(self):
		return self.user.username



class Solo(models.Model):
	
	TERRIBLE = 1
	VERYBAD = 2
	BAD = 3
	MODERATE = 4
	GOOD = 5
	VERYGOOD = 6
	EXCELLENT = 7

	OPTIONS = (
		(TERRIBLE, 'Terrible'),
		(VERYBAD, 'Very bad'),
		(BAD, 'Bad'),
		(MODERATE, 'Moderate'),
		(GOOD, 'Good'),
		(VERYGOOD, 'Very good'),
		(EXCELLENT, 'Excellent'),
	)
	
	musician = models.ForeignKey(Musician, null=True, on_delete=models.PROTECT)
	evaluated = models.BooleanField(default=False)
	solo = models.CharField(max_length=100, blank=True)
	usesolo = models.BooleanField(default=False)
	rating = models.IntegerField(choices=OPTIONS, null=True)

	class Meta:
		abstract = True

	@classmethod
	def create(cls, solo, musician):
		return cls(solo=solo, musician=musician)


	def __str__(self):
		return '%d - %s' % (self.id, self.solo)

	def __unicode__(self):
		return '%d - %s' % (self.id, self.solo)



class SoloAllRules(Solo):

	def get_dir(self):
		return 'solos/allrules'

	def get_solo_type(self):
		return 1



class SoloRandom(Solo):

	def get_dir(self):
		return 'solos/randoms'

	def get_solo_type(self):
		return 2
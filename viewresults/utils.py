from django.contrib.auth.models import User

from matchmaker.models import Musician, SoloAllRules, SoloRandom, Solo

import matchmaker.utils as mutils

import os

import pygal

import csv

import shutil


class ResultByMusicians(object):
	def __init__(self, musname, musid, allrulesvotes, randrulesvotes, drawvotes, unvoted):
		self.musname = musname
		self.musid = musid
		self.allrulesvotes = allrulesvotes
		self.randrulesvotes = randrulesvotes
		self.drawvotes = drawvotes
		self.unvoted = unvoted



class UserEvaluation(object):
	def __init__(self, musname, musid, terribles, verybads, bads, moderates, goods, verygoods, excellents, unevaluateds):
		self.musname = musname
		self.musid = musid
		self.terribles = terribles
		self.verybads = verybads
		self.bads = bads
		self.moderates = moderates
		self.goods = goods
		self.verygoods = verygoods
		self.excellents = excellents
		self.unevaluateds = unevaluateds
		


class Statistic(object):
	def __init__(self, musname, musid, randaverage, allrulesaverage):
		self.musname = musname
		self.musid = musid
		self.randaverage = randaverage
		self.allrulesaverage = allrulesaverage

	def get_difference(self):
		return (self.allrulesaverage - self.randaverage)



def get_all_musicians():
	return Musician.objects.all()



def get_allrulesvotes(musician):
	return MatchRFull.objects.filter(musician=musician, voted=True, winner=MatchRFull.FULLWIN).count()



def get_randrulesvotes(musician):
	return MatchRFull.objects.filter(musician=musician, voted=True, winner=MatchRFull.RANDWIN).count()



def get_drawvotes(musician):
	return MatchRFull.objects.filter(musician=musician, voted=True, winner=MatchRFull.DRAW).count()



def get_unvoted_count(musician):
	return MatchRFull.objects.filter(musician=musician, voted=False).count()


def get_sum_allrules():
	return MatchRFull.objects.filter(voted=True, winner=MatchRFull.FULLWIN).count()


def get_sum_nonrules():
	return MatchRFull.objects.filter(voted=True, winner=MatchRFull.RANDWIN).count()


def get_sum_draw():
	return MatchRFull.objects.filter(voted=True, winner=MatchRFull.DRAW).count()


def get_sum_unvoted():
	return MatchRFull.objects.filter(voted=False).count()


def get_musician_contests(musid):
	musician = Musician.objects.get(user=User.objects.get(pk=int(musid)))
	return MatchRFull.objects.filter(musician=musician)


def get_musician_by_id(musid):
	return Musician.objects.get(user=User.objects.get(pk=int(musid)))


def get_contest_by_id(contest_id):
	return MatchRFull.objects.get(pk=int(contest_id))



def get_beginner_random_wins():
	return MatchRFull.objects.filter(musician__level=Musician.BEGINNER, winner=MatchRFull.RANDWIN).count()


def get_beginner_allrules_wins():
	return MatchRFull.objects.filter(musician__level=Musician.BEGINNER, winner=MatchRFull.FULLWIN).count()


def get_intermediate_random_wins():
	return MatchRFull.objects.filter(musician__level=Musician.INTERMEDIATE, winner=MatchRFull.RANDWIN).count()


def get_intermediate_allrules_wins():
	return MatchRFull.objects.filter(musician__level=Musician.INTERMEDIATE, winner=MatchRFull.FULLWIN).count()


def get_professional_random_wins():
	return MatchRFull.objects.filter(musician__level=Musician.PROFESSIONAL, winner=MatchRFull.RANDWIN).count()


def get_professional_allrules_wins():
	return MatchRFull.objects.filter(musician__level=Musician.PROFESSIONAL, winner=MatchRFull.FULLWIN).count()


def create_by_musicians_level_chart(bwins, intwins, prowins):
	line_chart = pygal.Bar()
	line_chart.title = 'Solos score by musicians level'
	line_chart.x_labels = ['Beginner', 'Intermediate', 'Professional']
	line_chart.add('Random', [ bwins.get('brandwins'), intwins.get('intrandwins'), prowins.get('prorandwins') ])
	line_chart.add('Optimized', [ bwins.get('ballruleswins'), intwins.get('intallruleswins'), prowins.get('proallruleswins') ])

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'bymlevel.svg'

	line_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	line_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_beginner_random_use_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Beginners random use (%)"

	bdontuse = MatchRFull.objects.filter(musician__level=Musician.BEGINNER, winner=MatchRFull.RANDWIN, usewinner=False).count()
	buse = MatchRFull.objects.filter(musician__level=Musician.BEGINNER, winner=MatchRFull.RANDWIN, usewinner=True).count()

	pie_chart.add('Use winner', buse)
	pie_chart.add("Don't Use winner", bdontuse)

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'byusebeginner.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_beginner_allrules_use_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Beginners all rules use (%)"

	bdontuse = MatchRFull.objects.filter(musician__level=Musician.BEGINNER, winner=MatchRFull.FULLWIN, usewinner=False).count()
	buse = MatchRFull.objects.filter(musician__level=Musician.BEGINNER, winner=MatchRFull.FULLWIN, usewinner=True).count()

	pie_chart.add('Use winner', buse)
	pie_chart.add("Don't Use winner", bdontuse)

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'byuseallrulesbeginner.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name




def get_intermediate_random_use_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Intermediate random use (%)"

	bdontuse = MatchRFull.objects.filter(musician__level=Musician.INTERMEDIATE, winner=MatchRFull.RANDWIN, usewinner=False).count()
	buse = MatchRFull.objects.filter(musician__level=Musician.INTERMEDIATE, winner=MatchRFull.RANDWIN, usewinner=True).count()

	pie_chart.add('Use winner', buse)
	pie_chart.add("Don't Use winner", bdontuse)

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'byranduseinterm.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name




def get_intermediate_allrules_use_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Intermediate all rules use (%)"

	bdontuse = MatchRFull.objects.filter(musician__level=Musician.INTERMEDIATE, winner=MatchRFull.FULLWIN, usewinner=False).count()
	buse = MatchRFull.objects.filter(musician__level=Musician.INTERMEDIATE, winner=MatchRFull.FULLWIN, usewinner=True).count()

	pie_chart.add('Use winner', buse)
	pie_chart.add("Don't Use winner", bdontuse)

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'byalluseinterm.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_professional_random_use_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Professional random use (%)"

	bdontuse = MatchRFull.objects.filter(musician__level=Musician.PROFESSIONAL, winner=MatchRFull.RANDWIN, usewinner=False).count()
	buse = MatchRFull.objects.filter(musician__level=Musician.PROFESSIONAL, winner=MatchRFull.RANDWIN, usewinner=True).count()

	pie_chart.add('Use winner', buse)
	pie_chart.add("Don't Use winner", bdontuse)

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'byrandusepro.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name




def get_professional_allrules_use_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Professional all rules use (%)"

	bdontuse = MatchRFull.objects.filter(musician__level=Musician.PROFESSIONAL, winner=MatchRFull.FULLWIN, usewinner=False).count()
	buse = MatchRFull.objects.filter(musician__level=Musician.PROFESSIONAL, winner=MatchRFull.FULLWIN, usewinner=True).count()

	pie_chart.add('Use winner', buse)
	pie_chart.add("Don't Use winner", bdontuse)

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'byallusepro.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def by_musician_random_terribles_count(musician):
	return SoloRandom.objects.filter(musician=musician, evaluated=True, rating=Solo.TERRIBLE).count()


def by_musician_random_verybads_count(musician):
	return SoloRandom.objects.filter(musician=musician, evaluated=True, rating=Solo.VERYBAD).count()


def by_musician_random_bads_count(musician):
	return SoloRandom.objects.filter(musician=musician, evaluated=True, rating=Solo.BAD).count()


def by_musician_random_moderates_count(musician):
	return SoloRandom.objects.filter(musician=musician, evaluated=True, rating=Solo.MODERATE).count()


def by_musician_random_goods_count(musician):
	return SoloRandom.objects.filter(musician=musician, evaluated=True, rating=Solo.GOOD).count()


def by_musician_random_verygoods_count(musician):
	return SoloRandom.objects.filter(musician=musician, evaluated=True, rating=Solo.VERYGOOD).count()

def by_musician_random_excellents_count(musician):
	return SoloRandom.objects.filter(musician=musician, evaluated=True, rating=Solo.EXCELLENT).count()


def by_musician_random_unevaluateds_count(musician):
	return SoloRandom.objects.filter(musician=musician, evaluated=False).count()



def by_musician_allrules_terribles_count(musician):
	return SoloAllRules.objects.filter(musician=musician, evaluated=True, rating=Solo.TERRIBLE).count()


def by_musician_allrules_verybads_count(musician):
	return SoloAllRules.objects.filter(musician=musician, evaluated=True, rating=Solo.VERYBAD).count()


def by_musician_allrules_bads_count(musician):
	return SoloAllRules.objects.filter(musician=musician, evaluated=True, rating=Solo.BAD).count()


def by_musician_allrules_moderates_count(musician):
	return SoloAllRules.objects.filter(musician=musician, evaluated=True, rating=Solo.MODERATE).count()


def by_musician_allrules_goods_count(musician):
	return SoloAllRules.objects.filter(musician=musician, evaluated=True, rating=Solo.GOOD).count()


def by_musician_allrules_verygoods_count(musician):
	return SoloAllRules.objects.filter(musician=musician, evaluated=True, rating=Solo.VERYGOOD).count()

def by_musician_allrules_excellents_count(musician):
	return SoloAllRules.objects.filter(musician=musician, evaluated=True, rating=Solo.EXCELLENT).count()


def by_musician_allrules_unevaluateds_count(musician):
	return SoloAllRules.objects.filter(musician=musician, evaluated=False).count()


def get_random_evals_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Randoms evaluations (%)"

	pie_chart.add('Terrible', SoloRandom.objects.filter(evaluated=True, rating=Solo.TERRIBLE).count())
	pie_chart.add('Very bad', SoloRandom.objects.filter(evaluated=True, rating=Solo.VERYBAD).count())
	pie_chart.add('Bad', SoloRandom.objects.filter(evaluated=True, rating=Solo.BAD).count())
	pie_chart.add('Moderate', SoloRandom.objects.filter(evaluated=True, rating=Solo.MODERATE).count())
	pie_chart.add('Good', SoloRandom.objects.filter(evaluated=True, rating=Solo.GOOD).count())
	pie_chart.add('Very good', SoloRandom.objects.filter(evaluated=True, rating=Solo.VERYGOOD).count())
	pie_chart.add('Excellent', SoloRandom.objects.filter(evaluated=True, rating=Solo.EXCELLENT).count())

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'bymusrandevals.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_allrules_evals_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "AllRules evaluations (%)"

	pie_chart.add('Terrible', SoloAllRules.objects.filter(evaluated=True, rating=Solo.TERRIBLE).count())
	pie_chart.add('Very bad', SoloAllRules.objects.filter(evaluated=True, rating=Solo.VERYBAD).count())
	pie_chart.add('Bad', SoloAllRules.objects.filter(evaluated=True, rating=Solo.BAD).count())
	pie_chart.add('Moderate', SoloAllRules.objects.filter(evaluated=True, rating=Solo.MODERATE).count())
	pie_chart.add('Good', SoloAllRules.objects.filter(evaluated=True, rating=Solo.GOOD).count())
	pie_chart.add('Very good', SoloAllRules.objects.filter(evaluated=True, rating=Solo.VERYGOOD).count())
	pie_chart.add('Excellent', SoloAllRules.objects.filter(evaluated=True, rating=Solo.EXCELLENT).count())

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'bymusallrulesevals.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name


def get_musician_randoms(musician):
	return SoloRandom.objects.filter(musician=musician)


def get_musician_allrules(musician):
	return SoloAllRules.objects.filter(musician=musician)


def get_randsolo_by_id(soloid):
	return SoloRandom.objects.get(pk=soloid)


def get_allrules_solo_by_id(soloid):
	return SoloAllRules.objects.get(pk=soloid)


def get_beginner_voters_count():
	musicians = Musician.objects.filter(level=Musician.BEGINNER)
	total = 0

	for mu in musicians:
		if not mutils.has_unevaluated_solos(mu.user):
			total += 1

	return total



def get_intermediate_voters_count():
	musicians = Musician.objects.filter(level=Musician.INTERMEDIATE)
	total = 0

	for mu in musicians:
		if not mutils.has_unevaluated_solos(mu.user):
			total += 1

	return total



def get_professional_voters_count():
	musicians = Musician.objects.filter(level=Musician.PROFESSIONAL)
	total = 0

	for mu in musicians:
		if not mutils.has_unevaluated_solos(mu.user):
			total += 1

	return total



def get_beginner_random_votes_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Beginners Randoms evals (%)"

	pie_chart.add('Terrible', SoloRandom.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.TERRIBLE).count())
	pie_chart.add('Very bad', SoloRandom.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.VERYBAD).count())
	pie_chart.add('Bad', SoloRandom.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.BAD).count())
	pie_chart.add('Moderate', SoloRandom.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.MODERATE).count())
	pie_chart.add('Good', SoloRandom.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.GOOD).count())
	pie_chart.add('Very good', SoloRandom.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.VERYGOOD).count())
	pie_chart.add('Excellent', SoloRandom.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.EXCELLENT).count())

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'begrandevals.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_beginner_allrules_votes_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Beginners allRules evaluations (%)"

	pie_chart.add('Terrible', SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.TERRIBLE).count())
	pie_chart.add('Very bad', SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.VERYBAD).count())
	pie_chart.add('Bad', SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.BAD).count())
	pie_chart.add('Moderate', SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.MODERATE).count())
	pie_chart.add('Good', SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.GOOD).count())
	pie_chart.add('Very good', SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.VERYGOOD).count())
	pie_chart.add('Excellent', SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, evaluated=True, rating=Solo.EXCELLENT).count())

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'begallrulesevals.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_intermediate_random_votes_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Intermediate Randoms evals (%)"

	pie_chart.add('Terrible', SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.TERRIBLE).count())
	pie_chart.add('Very bad', SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.VERYBAD).count())
	pie_chart.add('Bad', SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.BAD).count())
	pie_chart.add('Moderate', SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.MODERATE).count())
	pie_chart.add('Good', SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.GOOD).count())
	pie_chart.add('Very good', SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.VERYGOOD).count())
	pie_chart.add('Excellent', SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.EXCELLENT).count())

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'interrandevals.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_intermediate_allrules_votes_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Intermediate allRules evaluations (%)"

	pie_chart.add('Terrible', SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.TERRIBLE).count())
	pie_chart.add('Very bad', SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.VERYBAD).count())
	pie_chart.add('Bad', SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.BAD).count())
	pie_chart.add('Moderate', SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.MODERATE).count())
	pie_chart.add('Good', SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.GOOD).count())
	pie_chart.add('Very good', SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.VERYGOOD).count())
	pie_chart.add('Excellent', SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, evaluated=True, rating=Solo.EXCELLENT).count())

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'interallrulesevals.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_professional_random_votes_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Professionals Randoms evals (%)"

	pie_chart.add('Terrible', SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.TERRIBLE).count())
	pie_chart.add('Very bad', SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.VERYBAD).count())
	pie_chart.add('Bad', SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.BAD).count())
	pie_chart.add('Moderate', SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.MODERATE).count())
	pie_chart.add('Good', SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.GOOD).count())
	pie_chart.add('Very good', SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.VERYGOOD).count())
	pie_chart.add('Excellent', SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.EXCELLENT).count())

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'profrandevals.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_professional_allrules_votes_chart():
	pie_chart = pygal.Pie(print_values=True)
	pie_chart.title = "Professionals allRules evaluations (%)"

	pie_chart.add('Terrible', SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.TERRIBLE).count())
	pie_chart.add('Very bad', SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.VERYBAD).count())
	pie_chart.add('Bad', SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.BAD).count())
	pie_chart.add('Moderate', SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.MODERATE).count())
	pie_chart.add('Good', SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.GOOD).count())
	pie_chart.add('Very good', SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.VERYGOOD).count())
	pie_chart.add('Excellent', SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, evaluated=True, rating=Solo.EXCELLENT).count())

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'profallrulesevals.svg'

	pie_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	pie_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name


def get_average(itemset):
	total = 0
	for i in itemset:
		total += i.rating

	return float("{0:.2f}".format(total / float(len(itemset))) )



def get_all_averages():
	musicians = Musician.objects.all().order_by('id')

	statistics = []

	for mu in musicians:

		if SoloRandom.objects.filter(musician=mu, evaluated=False) or SoloAllRules.objects.filter(musician=mu, evaluated=False):
			continue

		rands = SoloRandom.objects.filter(musician=mu)
		alls = SoloAllRules.objects.filter(musician=mu)

		if rands and alls:
			statistics.append( Statistic(mu.user.username, mu.id, get_average(rands), get_average(alls) ) )

	return statistics



def get_bylevel_averages(leveltype):
	if leveltype in ['b', 'B']:
		musicians = Musician.objects.filter(level=Musician.BEGINNER).order_by('id')
	elif leveltype in ['i', 'I']:
		musicians = Musician.objects.filter(level=Musician.INTERMEDIATE).order_by('id')
	elif leveltype in ['p', 'P']:
		musicians = Musician.objects.filter(level=Musician.PROFESSIONAL).order_by('id')

	statistics = []

	for mu in musicians:

		if SoloRandom.objects.filter(musician=mu, evaluated=False) or SoloAllRules.objects.filter(musician=mu, evaluated=False):
			continue

		rands = SoloRandom.objects.filter(musician=mu)
		alls = SoloAllRules.objects.filter(musician=mu)

		if rands and alls:
			statistics.append( Statistic(mu.user.username, mu.id, get_average(rands), get_average(alls) ) )

	return statistics


def get_usesolo_score_all():
	csv_url = '%s/matchmaker/templates/static/csvfiles' % os.getcwd()
	csv_url2 = '%s/matchmaker/templates/sfiles/csvfiles' % os.getcwd()
	csvfile = 'usesolo_statistcs.csv'

	musicians = Musician.objects.all()
	with open('%s/%s' %(csv_url2, csvfile), 'a+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow( ['name', 'use_opt', 'use_rand'])
		for m in musicians:
			writer.writerow( [m.user.username,
			 SoloAllRules.objects.filter(musician=m, usesolo=True).count(),
			 SoloRandom.objects.filter(musician=m, usesolo=True).count()])
			
	shutil.copyfile('%s/%s' %(csv_url2, csvfile), '%s/%s' %(csv_url, csvfile))

	return csvfile	


def get_avg_avg(statistics):
	randtotal = 0
	alltotal = 0
	for s in statistics:
		randtotal += s.randaverage
		alltotal += s.allrulesaverage

	return (float("{0:.2f}".format(randtotal / float(len(statistics))) ), float("{0:.2f}".format(alltotal / float(len(statistics))) )    )



def get_csv_avg_file(begaverages, interaverages, proaverages):
	csv_url = '%s/matchmaker/templates/static/csvfiles' % os.getcwd()
	csv_url2 = '%s/matchmaker/templates/sfiles/csvfiles' % os.getcwd()
	csvfile = 'average_statistcs.csv'

	with open('%s/%s' %(csv_url2, csvfile), 'w+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow( ['name', 'type', 'averagescore', 'level'] )
		for b in begaverages:
			writer.writerow( [b.musname, 'random', b.randaverage, 'beginner'] )
			writer.writerow( [b.musname, 'opt', b.allrulesaverage, 'beginner'] )

		for i in interaverages:
			writer.writerow( [i.musname, 'random', i.randaverage, 'intermediate'] )
			writer.writerow( [i.musname, 'opt', i.allrulesaverage, 'intermediate'] )

		for p in proaverages:
			writer.writerow( [p.musname, 'random', p.randaverage, 'professional'] )
			writer.writerow( [p.musname, 'opt', p.allrulesaverage, 'professional'] )

	shutil.copyfile('%s/%s' %(csv_url2, csvfile), '%s/%s' %(csv_url, csvfile))

	return csvfile



def get_csv_avg_bymusicians(begaverages, interaverages, proaverages):
	csv_url = '%s/matchmaker/templates/static/csvfiles' % os.getcwd()
	csv_url2 = '%s/matchmaker/templates/sfiles/csvfiles' % os.getcwd()
	csvfile = 'average_statistcs_mode2.csv'

	with open('%s/%s' %(csv_url2, csvfile), 'w+') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow( ['musician', 'level', 'difference (opt-rand)'] )
		for b in begaverages:
			writer.writerow( [b.musname, 'beginner', float("{0:.2f}".format(b.allrulesaverage - b.randaverage)) ] )

		for i in interaverages:
			writer.writerow( [i.musname, 'intermediate', float("{0:.2f}".format(i.allrulesaverage - i.randaverage)) ] )

		for p in proaverages:
			writer.writerow( [p.musname, 'professional', float("{0:.2f}".format(p.allrulesaverage - p.randaverage)) ] )

	shutil.copyfile('%s/%s' %(csv_url2, csvfile), '%s/%s' %(csv_url, csvfile))

	return csvfile




def get_csv_score_file():
	csv_url = '%s/matchmaker/templates/static/csvfiles' % os.getcwd()
	csv_url2 = '%s/matchmaker/templates/sfiles/csvfiles' % os.getcwd()
	csvfile = 'usage_statistcs.csv'

	solos_dir = 'matchmaker/templates/static/solos'
	solos_random = os.listdir( '%s/%s/randoms' %(os.getcwd(), solos_dir) )
	solos_all = os.listdir( '%s/%s/allrules' %(os.getcwd(), solos_dir) )

	with open('%s/%s' %(csv_url2, csvfile), 'w+b') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow( ['song', 'type', 'percentage_use'] )
		for sr in solos_random:
			randuse = SoloRandom.objects.filter(solo=sr, evaluated=True, usesolo=True).count()
			randnonuse = SoloRandom.objects.filter(solo=sr, evaluated=True, usesolo=False).count()
			percentage = float("{0:.1f}".format(float(randuse)/ (randuse + randnonuse)) )
			writer.writerow( [sr, 'rand', percentage] )

		for sa in solos_all:
			alluse = SoloAllRules.objects.filter(solo=sa, evaluated=True, usesolo=True).count()
			allnonuse = SoloAllRules.objects.filter(solo=sa, evaluated=True, usesolo=False).count()
			percentage = float("{0:.1f}".format(float(alluse)/ (alluse + allnonuse)) )
			writer.writerow( [sa, 'opt', percentage] )
			


	shutil.copyfile('%s/%s' %(csv_url2, csvfile), '%s/%s' %(csv_url, csvfile))

	return csvfile


def get_randuse_chart():
	line_chart = pygal.Bar()
	line_chart.title = 'Rand Solos use'
	line_chart.x_labels = ['Terrible', 'Very bad', 'Bad', 'Moderate', 'Good', 'Very good', 'Excellent']

	ter_use = SoloRandom.objects.filter(rating=Solo.TERRIBLE, usesolo=True).count()
	ter_not_use = SoloRandom.objects.filter(rating=Solo.TERRIBLE, usesolo=False).count()
	vbad_use = SoloRandom.objects.filter(rating=Solo.VERYBAD, usesolo=True).count()
	vbad_not_use = SoloRandom.objects.filter(rating=Solo.VERYBAD, usesolo=False).count()
	bad_use = SoloRandom.objects.filter(rating=Solo.BAD, usesolo=True).count()
	bad_not_use = SoloRandom.objects.filter(rating=Solo.BAD, usesolo=False).count()
	mod_use = SoloRandom.objects.filter(rating=Solo.MODERATE, usesolo=True).count()
	mod_not_use = SoloRandom.objects.filter(rating=Solo.MODERATE, usesolo=False).count()
	good_use = SoloRandom.objects.filter(rating=Solo.GOOD, usesolo=True).count()
	good_not_use = SoloRandom.objects.filter(rating=Solo.GOOD, usesolo=False).count()
	vgood_use = SoloRandom.objects.filter(rating=Solo.VERYGOOD, usesolo=True).count()
	vgood_not_use = SoloRandom.objects.filter(rating=Solo.VERYGOOD, usesolo=False).count()
	exc_use = SoloRandom.objects.filter(rating=Solo.EXCELLENT, usesolo=True).count()
	exc_not_use = SoloRandom.objects.filter(rating=Solo.EXCELLENT, usesolo=False).count()


	line_chart.add("Don't use", [ter_not_use, vbad_not_use, bad_not_use, mod_not_use, good_not_use, vgood_not_use, exc_not_use])
	line_chart.add('Use', [ter_use, vbad_use, bad_use, mod_use, good_use, vgood_use, exc_use])

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'generalrandsolouse.svg'

	line_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	line_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name


def get_allrulesuse_chart():
	line_chart = pygal.Bar()
	line_chart.title = 'AllRules Solos use'
	line_chart.x_labels = ['Terrible', 'Very bad', 'Bad', 'Moderate', 'Good', 'Very good', 'Excellent']

	ter_use = SoloAllRules.objects.filter(rating=Solo.TERRIBLE, usesolo=True).count()
	ter_not_use = SoloAllRules.objects.filter(rating=Solo.TERRIBLE, usesolo=False).count()
	vbad_use = SoloAllRules.objects.filter(rating=Solo.VERYBAD, usesolo=True).count()
	vbad_not_use = SoloAllRules.objects.filter(rating=Solo.VERYBAD, usesolo=False).count()
	bad_use = SoloAllRules.objects.filter(rating=Solo.BAD, usesolo=True).count()
	bad_not_use = SoloAllRules.objects.filter(rating=Solo.BAD, usesolo=False).count()
	mod_use = SoloAllRules.objects.filter(rating=Solo.MODERATE, usesolo=True).count()
	mod_not_use = SoloAllRules.objects.filter(rating=Solo.MODERATE, usesolo=False).count()
	good_use = SoloAllRules.objects.filter(rating=Solo.GOOD, usesolo=True).count()
	good_not_use = SoloAllRules.objects.filter(rating=Solo.GOOD, usesolo=False).count()
	vgood_use = SoloAllRules.objects.filter(rating=Solo.VERYGOOD, usesolo=True).count()
	vgood_not_use = SoloAllRules.objects.filter(rating=Solo.VERYGOOD, usesolo=False).count()
	exc_use = SoloAllRules.objects.filter(rating=Solo.EXCELLENT, usesolo=True).count()
	exc_not_use = SoloAllRules.objects.filter(rating=Solo.EXCELLENT, usesolo=False).count()


	line_chart.add("Don't use", [ter_not_use, vbad_not_use, bad_not_use, mod_not_use, good_not_use, vgood_not_use, exc_not_use])
	line_chart.add('Use', [ter_use, vbad_use, bad_use, mod_use, good_use, vgood_use, exc_use])

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'generalallrulessolouse.svg'

	line_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	line_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_beginner_randuse_chart():
	line_chart = pygal.Bar()
	line_chart.title = 'Beginners rand use'
	line_chart.x_labels = ['Terrible', 'Very bad', 'Bad', 'Moderate', 'Good', 'Very good', 'Excellent']

	ter_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER ,rating=Solo.TERRIBLE, usesolo=True).count()
	ter_not_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.TERRIBLE, usesolo=False).count()
	vbad_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.VERYBAD, usesolo=True).count()
	vbad_not_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.VERYBAD, usesolo=False).count()
	bad_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.BAD, usesolo=True).count()
	bad_not_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.BAD, usesolo=False).count()
	mod_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.MODERATE, usesolo=True).count()
	mod_not_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.MODERATE, usesolo=False).count()
	good_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.GOOD, usesolo=True).count()
	good_not_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.GOOD, usesolo=False).count()
	vgood_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.VERYGOOD, usesolo=True).count()
	vgood_not_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.VERYGOOD, usesolo=False).count()
	exc_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.EXCELLENT, usesolo=True).count()
	exc_not_use = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.EXCELLENT, usesolo=False).count()


	line_chart.add("Don't use", [ter_not_use, vbad_not_use, bad_not_use, mod_not_use, good_not_use, vgood_not_use, exc_not_use])
	line_chart.add('Use', [ter_use, vbad_use, bad_use, mod_use, good_use, vgood_use, exc_use])

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'begrandsolouse.svg'

	line_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	line_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_beginner_allrulesuse_chart():
	line_chart = pygal.Bar()
	line_chart.title = 'Beginners AllRules Solos use'
	line_chart.x_labels = ['Terrible', 'Very bad', 'Bad', 'Moderate', 'Good', 'Very good', 'Excellent']

	ter_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER ,rating=Solo.TERRIBLE, usesolo=True).count()
	ter_not_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.TERRIBLE, usesolo=False).count()
	vbad_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.VERYBAD, usesolo=True).count()
	vbad_not_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.VERYBAD, usesolo=False).count()
	bad_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.BAD, usesolo=True).count()
	bad_not_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.BAD, usesolo=False).count()
	mod_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.MODERATE, usesolo=True).count()
	mod_not_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.MODERATE, usesolo=False).count()
	good_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.GOOD, usesolo=True).count()
	good_not_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.GOOD, usesolo=False).count()
	vgood_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.VERYGOOD, usesolo=True).count()
	vgood_not_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.VERYGOOD, usesolo=False).count()
	exc_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.EXCELLENT, usesolo=True).count()
	exc_not_use = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, rating=Solo.EXCELLENT, usesolo=False).count()


	line_chart.add("Don't use", [ter_not_use, vbad_not_use, bad_not_use, mod_not_use, good_not_use, vgood_not_use, exc_not_use])
	line_chart.add('Use', [ter_use, vbad_use, bad_use, mod_use, good_use, vgood_use, exc_use])

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'begallrulessolouse.svg'

	line_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	line_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_intermed_randuse_chart():
	line_chart = pygal.Bar()
	line_chart.title = 'Intermediate rand use'
	line_chart.x_labels = ['Terrible', 'Very bad', 'Bad', 'Moderate', 'Good', 'Very good', 'Excellent']

	ter_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE ,rating=Solo.TERRIBLE, usesolo=True).count()
	ter_not_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.TERRIBLE, usesolo=False).count()
	vbad_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.VERYBAD, usesolo=True).count()
	vbad_not_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.VERYBAD, usesolo=False).count()
	bad_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.BAD, usesolo=True).count()
	bad_not_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.BAD, usesolo=False).count()
	mod_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.MODERATE, usesolo=True).count()
	mod_not_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.MODERATE, usesolo=False).count()
	good_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.GOOD, usesolo=True).count()
	good_not_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.GOOD, usesolo=False).count()
	vgood_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.VERYGOOD, usesolo=True).count()
	vgood_not_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.VERYGOOD, usesolo=False).count()
	exc_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.EXCELLENT, usesolo=True).count()
	exc_not_use = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.EXCELLENT, usesolo=False).count()


	line_chart.add("Don't use", [ter_not_use, vbad_not_use, bad_not_use, mod_not_use, good_not_use, vgood_not_use, exc_not_use])
	line_chart.add('Use', [ter_use, vbad_use, bad_use, mod_use, good_use, vgood_use, exc_use])

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'interrandsolouse.svg'

	line_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	line_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_intermed_allrulesuse_chart():
	line_chart = pygal.Bar()
	line_chart.title = 'Intermediate AllRules Solos use'
	line_chart.x_labels = ['Terrible', 'Very bad', 'Bad', 'Moderate', 'Good', 'Very good', 'Excellent']

	ter_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE ,rating=Solo.TERRIBLE, usesolo=True).count()
	ter_not_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.TERRIBLE, usesolo=False).count()
	vbad_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.VERYBAD, usesolo=True).count()
	vbad_not_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.VERYBAD, usesolo=False).count()
	bad_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.BAD, usesolo=True).count()
	bad_not_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.BAD, usesolo=False).count()
	mod_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.MODERATE, usesolo=True).count()
	mod_not_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.MODERATE, usesolo=False).count()
	good_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.GOOD, usesolo=True).count()
	good_not_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.GOOD, usesolo=False).count()
	vgood_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.VERYGOOD, usesolo=True).count()
	vgood_not_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.VERYGOOD, usesolo=False).count()
	exc_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.EXCELLENT, usesolo=True).count()
	exc_not_use = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, rating=Solo.EXCELLENT, usesolo=False).count()


	line_chart.add("Don't use", [ter_not_use, vbad_not_use, bad_not_use, mod_not_use, good_not_use, vgood_not_use, exc_not_use])
	line_chart.add('Use', [ter_use, vbad_use, bad_use, mod_use, good_use, vgood_use, exc_use])

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'interallrulessolouse.svg'

	line_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	line_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_prof_randuse_chart():
	line_chart = pygal.Bar()
	line_chart.title = 'Professionals rand use'
	line_chart.x_labels = ['Terrible', 'Very bad', 'Bad', 'Moderate', 'Good', 'Very good', 'Excellent']

	ter_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL ,rating=Solo.TERRIBLE, usesolo=True).count()
	ter_not_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.TERRIBLE, usesolo=False).count()
	vbad_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.VERYBAD, usesolo=True).count()
	vbad_not_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.VERYBAD, usesolo=False).count()
	bad_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.BAD, usesolo=True).count()
	bad_not_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.BAD, usesolo=False).count()
	mod_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.MODERATE, usesolo=True).count()
	mod_not_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.MODERATE, usesolo=False).count()
	good_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.GOOD, usesolo=True).count()
	good_not_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.GOOD, usesolo=False).count()
	vgood_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.VERYGOOD, usesolo=True).count()
	vgood_not_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.VERYGOOD, usesolo=False).count()
	exc_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.EXCELLENT, usesolo=True).count()
	exc_not_use = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.EXCELLENT, usesolo=False).count()


	line_chart.add("Don't use", [ter_not_use, vbad_not_use, bad_not_use, mod_not_use, good_not_use, vgood_not_use, exc_not_use])
	line_chart.add('Use', [ter_use, vbad_use, bad_use, mod_use, good_use, vgood_use, exc_use])

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'profrandsolouse.svg'

	line_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	line_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_prof_allrulesuse_chart():
	line_chart = pygal.Bar()
	line_chart.title = 'Professionals AllRules Solos use'
	line_chart.x_labels = ['Terrible', 'Very bad', 'Bad', 'Moderate', 'Good', 'Very good', 'Excellent']

	ter_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL ,rating=Solo.TERRIBLE, usesolo=True).count()
	ter_not_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.TERRIBLE, usesolo=False).count()
	vbad_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.VERYBAD, usesolo=True).count()
	vbad_not_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.VERYBAD, usesolo=False).count()
	bad_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.BAD, usesolo=True).count()
	bad_not_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.BAD, usesolo=False).count()
	mod_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.MODERATE, usesolo=True).count()
	mod_not_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.MODERATE, usesolo=False).count()
	good_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.GOOD, usesolo=True).count()
	good_not_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.GOOD, usesolo=False).count()
	vgood_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.VERYGOOD, usesolo=True).count()
	vgood_not_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.VERYGOOD, usesolo=False).count()
	exc_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.EXCELLENT, usesolo=True).count()
	exc_not_use = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, rating=Solo.EXCELLENT, usesolo=False).count()


	line_chart.add("Don't use", [ter_not_use, vbad_not_use, bad_not_use, mod_not_use, good_not_use, vgood_not_use, exc_not_use])
	line_chart.add('Use', [ter_use, vbad_use, bad_use, mod_use, good_use, vgood_use, exc_use])

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'profallrulessolouse.svg'

	line_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	line_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name



def get_general_solo_use():

	line_chart = pygal.Bar()

	line_chart.title = 'Overview "this solo can be used..."'
	line_chart.x_labels = ['All', 'Beginner', 'Intermediate', 'Professional']

	allsolouse_rand = SoloRandom.objects.filter(usesolo=True).count()
	allsolouse_opt = SoloAllRules.objects.filter(usesolo=True).count()

	allsolouse_begrand = SoloRandom.objects.filter(musician__level=Musician.BEGINNER, usesolo=True).count()
	allsolouse_begopt = SoloAllRules.objects.filter(musician__level=Musician.BEGINNER, usesolo=True).count()

	allsolouse_interrand = SoloRandom.objects.filter(musician__level=Musician.INTERMEDIATE, usesolo=True).count()
	allsolouse_interopt = SoloAllRules.objects.filter(musician__level=Musician.INTERMEDIATE, usesolo=True).count()

	allsolouse_prorand = SoloRandom.objects.filter(musician__level=Musician.PROFESSIONAL, usesolo=True).count()
	allsolouse_proopt = SoloAllRules.objects.filter(musician__level=Musician.PROFESSIONAL, usesolo=True).count()

	line_chart.add("Random", [allsolouse_rand, allsolouse_begrand, allsolouse_interrand, allsolouse_prorand])
	line_chart.add('Optimized', [allsolouse_opt, allsolouse_begopt, allsolouse_interopt, allsolouse_proopt])

	chart_url = '%s/matchmaker/templates/static/charts' % os.getcwd()
	chart_url2 = '%s/matchmaker/templates/sfiles/charts' % os.getcwd()
	chart_name = 'generalsolouse.svg'

	line_chart.render_to_file( '%s/%s' %(chart_url, chart_name) )
	line_chart.render_to_file( '%s/%s' %(chart_url2, chart_name) )

	return chart_name


def get_solos_scores(solostype=None):
	solos_dir = 'matchmaker/templates/static/solos'
	solos_random = os.listdir( '%s/%s/randoms' %(os.getcwd(), solos_dir) )
	solos_all = os.listdir( '%s/%s/allrules' %(os.getcwd(), solos_dir) )

	allsolos = []
	
	if solostype == 'rand':
		for s in solos_random:
			allsolos.append({
					'soloname': s,
					'terrible': SoloRandom.objects.filter(solo=s, evaluated=True, rating=Solo.TERRIBLE).count(),
					'verybad': SoloRandom.objects.filter(solo=s, evaluated=True, rating=Solo.VERYBAD).count(),
					'bad': SoloRandom.objects.filter(solo=s, evaluated=True, rating=Solo.BAD).count(),
					'moderate': SoloRandom.objects.filter(solo=s, evaluated=True, rating=Solo.MODERATE).count(),
					'good': SoloRandom.objects.filter(solo=s, evaluated=True, rating=Solo.GOOD).count(),
					'verygood': SoloRandom.objects.filter(solo=s, evaluated=True, rating=Solo.VERYGOOD).count(),
					'excellent': SoloRandom.objects.filter(solo=s, evaluated=True, rating=Solo.EXCELLENT).count(),
				})
	elif solostype == 'all':
		for s in solos_all:
			allsolos.append({
					'soloname': s,
					'terrible': SoloAllRules.objects.filter(solo=s, evaluated=True, rating=Solo.TERRIBLE).count(),
					'verybad': SoloAllRules.objects.filter(solo=s, evaluated=True, rating=Solo.VERYBAD).count(),
					'bad': SoloAllRules.objects.filter(solo=s, evaluated=True, rating=Solo.BAD).count(),
					'moderate': SoloAllRules.objects.filter(solo=s, evaluated=True, rating=Solo.MODERATE).count(),
					'good': SoloAllRules.objects.filter(solo=s, evaluated=True, rating=Solo.GOOD).count(),
					'verygood': SoloAllRules.objects.filter(solo=s, evaluated=True, rating=Solo.VERYGOOD).count(),
					'excellent': SoloAllRules.objects.filter(solo=s, evaluated=True, rating=Solo.EXCELLENT).count(),
				})

	else:
		return None

	return allsolos

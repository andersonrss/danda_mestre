from django.shortcuts import render

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseServerError, JsonResponse

from django.contrib.auth.decorators import login_required

import viewresults.utils as utils

# Create your views here.


@login_required(login_url='/contest/login/')
def by_musicians(request):
	musicians = utils.get_all_musicians()
	if not musicians:
		return HttpResponseServerError('No musicians found')

	results = []

	for mu in musicians:
		musername = mu.user.username
		musid = mu.user.id
		muallrulesvotes = utils.get_allrulesvotes(mu)
		murandrulesvotes = utils.get_randrulesvotes(mu)
		mudrawvotes = utils.get_drawvotes(mu)
		munvoted = utils.get_unvoted_count(mu)

		results.append( utils.ResultByMusicians(musername, musid, muallrulesvotes, murandrulesvotes, mudrawvotes, munvoted) )
		
	totals = {
		'totalallrules': utils.get_sum_allrules(),
		'totalnonrules': utils.get_sum_nonrules(),
		'totaldraw': utils.get_sum_draw(),
		'totalunvoted': utils.get_sum_unvoted(),
	}


	return render(request, 'bymusicians.html', {'results': results, 'totals': totals})




@login_required(login_url='/contest/login/')
def by_musicians_level(request):
	bwins = {
		'brandwins': utils.get_beginner_random_wins(),
		'ballruleswins': utils.get_beginner_allrules_wins()
	}

	intwins = {
		'intrandwins': utils.get_intermediate_random_wins(),
		'intallruleswins': utils.get_intermediate_allrules_wins()
		}

	prowins = {
		'prorandwins': utils.get_professional_random_wins(),
		'proallruleswins': utils.get_professional_allrules_wins()
		}

	chart_name = utils.create_by_musicians_level_chart(bwins, intwins, prowins)

	return render(request, 'bymlevel.html', {'chart_name': chart_name, 'bwins': bwins, 'intwins': intwins, 'prowins': prowins})



@login_required(login_url='/contest/login/')
def show_musician_contests(request, musid):
	musician = utils.get_musician_by_id(musid)
	contests = utils.get_musician_contests(musid)

	return render(request, 'musiciancontests.html', {'musician': musician, 'contests': contests})


@login_required(login_url='/contest/login/')
def get_playcontest(request, contest_id):
	if request.is_ajax():
		contest = utils.get_contest_by_id(contest_id)
		solo_random = '/static/'+ contest.get_dir_solo_one() + '/' + contest.solo_one
		solo_allrules = '/static/'+ contest.get_dir_solo_two() + '/' + contest.solo_two
		return JsonResponse({'solo_random': solo_random, 'solo_allrules': solo_allrules})
	else:
		return HttpResponseForbidden()


@login_required(login_url='/contest/login/')
def by_solo_use(request):

	charts = {
		'beginner_random_use_chart': utils.get_beginner_random_use_chart(),
		'beginner_allrules_use_chart': utils.get_beginner_allrules_use_chart(),
		'intermediate_random_use_chart': utils.get_intermediate_random_use_chart(),
		'intermediate_allrules_use_chart': utils.get_intermediate_allrules_use_chart(),
		'professional_random_use_chart': utils.get_professional_random_use_chart(),
		'professional_allrules_use_chart': utils.get_professional_allrules_use_chart(),
	}

	return render(request, 'bysolouse.html', {'charts': charts})


@login_required
def show_musicians_evaluations(request):
	musicians = utils.get_all_musicians()
	if not musicians:
		return HttpResponseServerError('No musicians found')

	rand_evaluations = []
	allrules_evaluations = []

	for mu in musicians:
		musername = mu.user.username
		musid = mu.user.id
		terribles = utils.by_musician_random_terribles_count(mu)
		verybads = utils.by_musician_random_verybads_count(mu)
		bads = utils.by_musician_random_bads_count(mu)
		moderates = utils.by_musician_random_moderates_count(mu)
		goods = utils.by_musician_random_goods_count(mu)
		verygoods = utils.by_musician_random_verygoods_count(mu)
		excelents = utils.by_musician_random_excellents_count(mu)
		unevaluated = utils.by_musician_random_unevaluateds_count(mu)

		rand_evaluations.append( utils.UserEvaluation(musername, musid, terribles, verybads, bads, 
			moderates, goods, verygoods, excelents, unevaluated) )

		musername = mu.user.username
		musid = mu.user.id
		terribles = utils.by_musician_allrules_terribles_count(mu)
		verybads = utils.by_musician_allrules_verybads_count(mu)
		bads = utils.by_musician_allrules_bads_count(mu)
		moderates = utils.by_musician_allrules_moderates_count(mu)
		goods = utils.by_musician_allrules_goods_count(mu)
		verygoods = utils.by_musician_allrules_verygoods_count(mu)
		excelents = utils.by_musician_allrules_excellents_count(mu)
		unevaluated = utils.by_musician_allrules_unevaluateds_count(mu)

		allrules_evaluations.append( utils.UserEvaluation(musername, musid, terribles, verybads, bads, 
			moderates, goods, verygoods, excelents, unevaluated) )

	random_eval_chart = utils.get_random_evals_chart()
	allrules_eval_chart = utils.get_allrules_evals_chart()

	return render(request, 'musiciansevaluations.html', {'rand_evaluations': rand_evaluations, 'allrules_evaluations': allrules_evaluations,
		'random_eval_chart': random_eval_chart, 'allrules_eval_chart': allrules_eval_chart})


@login_required(login_url='/contest/login/')
def show_single_musician_evaluations(request, musid):
	musician = utils.get_musician_by_id(musid)
	randoms = utils.get_musician_randoms(musician)
	allrules = utils.get_musician_allrules(musician)

	return render(request, 'singlemusevals.html', {'musician': musician, 'randoms': randoms, 'allrules': allrules})



@login_required(login_url='/contest/login/')
def get_randsolo(request, soloid):
	if request.is_ajax():
		solo = utils.get_randsolo_by_id(soloid)
		solo_url = '/static/'+ solo.get_dir() + '/' + solo.solo
		return JsonResponse({'solo': solo_url})
	else:
		return HttpResponseForbidden()



@login_required(login_url='/contest/login/')
def get_allrulesolo(request, soloid):
	if request.is_ajax():
		solo = utils.get_allrules_solo_by_id(soloid)
		solo_url = '/static/'+ solo.get_dir() + '/' + solo.solo
		return JsonResponse({'solo': solo_url})
	else:
		return HttpResponseForbidden()



@login_required(login_url='/contest/login/')
def show_begevals(request):
	bcount = utils.get_beginner_voters_count()
	charts = {
			'randchart': utils.get_beginner_random_votes_chart(),
			'allruleschart': utils.get_beginner_allrules_votes_chart(),
		}

	return render(request, 'bylvlevals.html', {'type': 'Beginners', 'bcount': bcount, 'charts': charts})



@login_required(login_url='/contest/login/')
def show_interevals(request):
	bcount = utils.get_intermediate_voters_count()
	charts = {
			'randchart': utils.get_intermediate_random_votes_chart(),
			'allruleschart': utils.get_intermediate_allrules_votes_chart(),
		}

	return render(request, 'bylvlevals.html', {'type': 'Intermediates', 'bcount': bcount, 'charts': charts})



@login_required(login_url='/contest/login/')
def show_profevals(request):
	bcount = utils.get_professional_voters_count()
	charts = {
			'randchart': utils.get_professional_random_votes_chart(),
			'allruleschart': utils.get_professional_allrules_votes_chart(),
		}

	return render(request, 'bylvlevals.html', {'type': 'Professionals', 'bcount': bcount, 'charts': charts})



@login_required(login_url='/contest/login/')
def show_statistics(request):
	begaverages = utils.get_bylevel_averages('b')
	randbegavg, allrulesbegavg = utils.get_avg_avg(begaverages)

	interaverages = utils.get_bylevel_averages('i')
	randinteravg, allrulesinteravg = utils.get_avg_avg(interaverages)

	proaverages = utils.get_bylevel_averages('p')
	randproavg, allrulesproavg = utils.get_avg_avg(proaverages)

	csvfile = utils.get_csv_avg_file(begaverages, interaverages, proaverages)

	csvfile2 = utils.get_csv_avg_bymusicians(begaverages, interaverages, proaverages)

	utils.get_usesolo_score_all()

	return render(request, 'byaverages.html', { 'begaverages': begaverages, 'interaverages': interaverages, 'proaverages': proaverages,
		'randbegavg': randbegavg, 'allrulesbegavg': allrulesbegavg, 'randinteravg': randinteravg, 'allrulesinteravg': allrulesinteravg,
		 'randproavg': randproavg, 'allrulesproavg': allrulesproavg, 'csvfile': csvfile, 'csvfile2': csvfile2 })



@login_required(login_url='/contest/login/')
def show_solouse_general(request):
	randuse = utils.get_randuse_chart()
	allrulesuse = utils.get_allrulesuse_chart()

	csvfile = utils.get_csv_score_file()
	return render(request, 'generalsolouse.html', {'usetype': 'General', 'randuse': randuse, 'allrulesuse': allrulesuse, 'csvfile': csvfile})



@login_required(login_url='/contest/login/')
def show_solouse_beginner(request):
	randuse = utils.get_beginner_randuse_chart()
	allrulesuse = utils.get_beginner_allrulesuse_chart()

	return render(request, 'generalsolouse.html', {'usetype': 'Beginners', 'randuse': randuse, 'allrulesuse': allrulesuse})



@login_required(login_url='/contest/login/')
def show_solouse_intermed(request):
	randuse = utils.get_intermed_randuse_chart()
	allrulesuse = utils.get_intermed_allrulesuse_chart()

	return render(request, 'generalsolouse.html', {'usetype': 'Intermediates', 'randuse': randuse, 'allrulesuse': allrulesuse})



@login_required(login_url='/contest/login/')
def show_solouse_prof(request):
	randuse = utils.get_prof_randuse_chart()
	allrulesuse = utils.get_prof_allrulesuse_chart()

	return render(request, 'generalsolouse.html', {'usetype': 'Professionals', 'randuse': randuse, 'allrulesuse': allrulesuse})



@login_required(login_url='/contest/login/')
def show_solosdetails(request):
	solosr = utils.get_solos_scores(solostype='rand')
	solosa = utils.get_solos_scores(solostype='all')
	return render(request, 'soloscore.html', {'solosr': solosr, 'solosa': solosa})



@login_required(login_url='/contest/login/')
def show_general_use(request):
	generalsolouse = utils.get_general_solo_use()
	return render(request, 'generalsolouse.html', {'usetype': 'General', 'randuse': generalsolouse, 'allrulesuse': generalsolouse})
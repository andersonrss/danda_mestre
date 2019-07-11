from matchmaker.models import SoloAllRules, SoloRandom, Solo

from django.contrib.auth.models import User

from itertools import chain

import random, os

def has_matches_assigned(user):
	matches = MatchRFull.objects.filter(musician=user.musician)

	if matches:
		return True
	else:
		return False



def has_evaluations_assigned(user):
    random_evals = SoloRandom.objects.filter(musician=user.musician)
    allrules_evals = SoloAllRules.objects.filter(musician=user.musician)

    if random_evals or allrules_evals:
        return True
    else:
        return False



def has_unevaluated_solos(user):
    random_evals = SoloRandom.objects.filter(musician=user.musician, evaluated=False)
    allrules_evals = SoloAllRules.objects.filter(musician=user.musician, evaluated=False)

    if random_evals or allrules_evals:
        return True
    else:
        return False



def get_evaluation(user):
    rsolos = SoloRandom.objects.filter(musician=user.musician, evaluated=False)
    asolos = SoloAllRules.objects.filter(musician=user.musician, evaluated=False)

    solos = list(chain(rsolos, asolos))

    random.seed()
    random.shuffle(solos)

    return random.choice(solos)



def has_level_defined(user):
	if user.musician.level:
		return True
	else:
		return False


def assign_evaluations(user):
    solos_dir = 'matchmaker/templates/static/solos'
    solos_random = os.listdir( '%s/%s/randoms' %(os.getcwd(), solos_dir) )
    # solos_few = os.listdir( '%s/%s/fewrules' %(os.getcwd(), solos_dir) )
    solos_all = os.listdir( '%s/%s/allrules' %(os.getcwd(), solos_dir) )

    random.seed()
    random.shuffle(solos_random)
    random.shuffle(solos_all)
    
    for i in range(3):
        rsolo = SoloRandom.create(solos_random[i], user.musician)
        rsolo.save()

        asolo = SoloAllRules.create(solos_all[i], user.musician)
        asolo.save()



def has_unvoted_matches(user):
    # if MatchRF.objects.filter(musician=user.musician, voted=False):
    #     return True
    # elif MatchFF.objects.filter(musician=user.musician, voted=False):
    #     return True
    # elif MatchRFull.objects.filter(musician=user.musician, voted=False):
    #     return True
    if MatchRFull.objects.filter(musician=user.musician, voted=False):
        return True
    else:
        return False



def get_count_contests_remaining(user):
    countrf = MatchRF.objects.filter(musician=user.musician, voted=False).count()
    countff = MatchFF.objects.filter(musician=user.musician, voted=False).count()
    countrfull = MatchRFull.objects.filter(musician=user.musician, voted=False).count()

    return (countrf + countff + countrfull)



def get_count_evaluations_remaining(user):
    count_rsolos = SoloRandom.objects.filter(musician=user.musician, evaluated=False).count()
    count_asolos = SoloAllRules.objects.filter(musician=user.musician, evaluated=False).count()

    return (count_asolos + count_rsolos)



def assign_matches_bkp(user):
    solos_dir = 'matchmaker/templates/static/solos'
    solos_full = os.listdir( '%s/%s/fullrules' %(os.getcwd(), solos_dir) )
    # solos_few = os.listdir( '%s/%s/fewrules' %(os.getcwd(), solos_dir) )
    solos_non = os.listdir( '%s/%s/nonrules' %(os.getcwd(), solos_dir) )

    random.seed()

    # for i in range(3):
    for i in range(6):
        solo_non = solos_non[random.randint(0,len(solos_non)-1)]
    	# solo_few = solos_few[random.randint(0,len(solos_few)-1)]
    	# solo_full = solos_full[random.randint(0,len(solos_full)-1)]
        solo_full = 'out-' + solo_non.split('-')[1]

    	# rf = MatchRF.create(solo_non, solo_few)
    	# rf.musician = user.musician
    	# rf.save()

    	# ff = MatchFF.create(solo_few, solo_full)
    	# ff.musician = user.musician
    	# ff.save()

        rfull = MatchRFull.create(solo_non, solo_full)
        rfull.musician = user.musician
        rfull.save()



def assign_matches(user):
    solos_dir = 'matchmaker/templates/static/solos'
    solos_full = os.listdir( '%s/%s/fullrules' %(os.getcwd(), solos_dir) )
    solos_non = os.listdir( '%s/%s/nonrules' %(os.getcwd(), solos_dir) )

    random.seed()
    random.shuffle(solos_non)

    for i in range(6):
        solo_non = solos_non[i]
        solo_full = 'out-' + solo_non.split('-')[1]

        rfull = MatchRFull.create(solo_non, solo_full)
        rfull.musician = user.musician
        rfull.save()



def assign_matches_bkp3(user):
    solos_dir = 'matchmaker/templates/static/solos'
    solos_full = os.listdir( '%s/%s/fullrules' %(os.getcwd(), solos_dir) )
    solos_non = os.listdir( '%s/%s/nonrules' %(os.getcwd(), solos_dir) )

    random.seed()
    random.shuffle(solos_non)
    random.shuffle(solos_full)

    for i in range(6):
        solo_non = solos_non[i]
        solo_full = solos_full[i]

        rfull = MatchRFull.create(solo_non, solo_full)
        rfull.musician = user.musician
        rfull.save()




def get_contest(user):
    rf = list( MatchRF.objects.filter(musician=user.musician, voted=False) )
    ff = list( MatchFF.objects.filter(musician=user.musician, voted=False) ) 
    rfull = list( MatchRFull.objects.filter(musician=user.musician, voted=False) )

    matches = rf + ff + rfull

    random.seed()
    return matches[random.randint(0,len(matches)-1)]



def vote_match(matchtype, winner, usewinner):
    mt = matchtype.split('-')
    
    if mt[0] == 'rf':
        try:
            match = MatchRF.objects.get( pk=int(mt[1]) )
            if winner == 0:
                match.winner = MatchRF.DRAW
            elif winner == 1:
                match.winner = MatchRF.RANDWIN
            elif winner == 2:
                match.winner = MatchRF.FEWWIN

            if usewinner:
                match.usewinner = True

            match.voted = True
            match.save()
        except Exception as e:
            return False
    elif mt[0] == 'ff':
        try:
            match = MatchFF.objects.get( pk=int(mt[1]) )
            if winner == 0:
                match.winner = MatchFF.DRAW
            elif winner == 1:
                match.winner = MatchFF.FEWWIN
            elif winner == 2:
                match.winner = MatchFF.FULLWIN

            if usewinner:
                match.usewinner = True

            match.voted = True
            match.save()
        except Exception as e:
            return False
    elif mt[0] == 'rfull':
        try:
            match = MatchRFull.objects.get( pk=int(mt[1]) )
            if winner == 0:
                match.winner = MatchRFull.DRAW
            elif winner == 1:
                match.winner = MatchRFull.RANDWIN
            elif winner == 2:
                match.winner = MatchRFull.FULLWIN

            if usewinner:
                match.usewinner = True
                
            match.voted = True
            match.save()
        except Exception as e:
            return False
    else:
        return False

    return True



def evaluate_solo(evaluationtype, evaluationid, solo_rate, usesolo):
    if evaluationtype == 1:
        evaluation = SoloAllRules.objects.get(pk=evaluationid)
    elif evaluationtype == 2:
        evaluation = SoloRandom.objects.get(pk=evaluationid)
    else:
        raise Exception('Evaluation type not identified')

    if solo_rate == 1:
        evaluation.rating = Solo.TERRIBLE
    elif solo_rate == 2:
        evaluation.rating = Solo.VERYBAD
    elif solo_rate == 3:
        evaluation.rating = Solo.BAD
    elif solo_rate == 4:
        evaluation.rating = Solo.MODERATE
    elif solo_rate == 5:
        evaluation.rating = Solo.GOOD
    elif solo_rate == 6:
        evaluation.rating = Solo.VERYGOOD
    elif solo_rate == 7:
        evaluation.rating = Solo.EXCELLENT

    if usesolo:
        evaluation.usesolo = True

    evaluation.evaluated = True
    evaluation.save()
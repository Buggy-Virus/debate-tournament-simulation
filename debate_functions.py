import numpy as np
import math as m
import operator as op

def make_debaters(dbtr_num, dbtr_mn_mn, dbtr_mn_std, dbtr_std_mn, dbtr_std_std):
	# Makes a list of debaters based upon average score and average score standard deviation
	min_zero = lambda x: max(x, 0)
	v_min_zero = np.vectorize(min_zero)
	dbtr_mns = v_min_zero(np.random.normal(dbtr_mn_mn, dbtr_mn_std, dbtr_num))
	dbtr_stds = v_min_zero(np.random.normal(dbtr_std_mn, dbtr_std_std, dbtr_num))
	dbtrs = np.concatenate(([dbtr_mns], [dbtr_stds]), axis=0)
	return dbtrs

def make_teams(dbtrs, dbtr_mn_mn, dbtr_mn_std):
	# Makes debate teams of two debaters, by the stronger debater picking the weaker, then seeds them
	temp_mns = dbtrs[0,:]
	sorted_inds = np.argsort(temp_mns)[::-1]
	evictable_dbtrs = dbtrs[:,sorted_inds]
	dbtr_num = len(temp_mns)
	cream_num = int(dbtr_num // 5)
	teams = {}
	for i in range(dbtr_num // 2):
		num_left = evictable_dbtrs.shape[1]
		beta_ind = int(np.random.uniform(1, min(cream_num, num_left - 1)))
		alpha = (evictable_dbtrs[0,0], evictable_dbtrs[1,0])
		beta = (evictable_dbtrs[0,beta_ind], evictable_dbtrs[1,beta_ind])
		team_mean = alpha[0] + beta[0]
		seed = team_mean > np.random.normal(3 * dbtr_mn_mn, 2 * dbtr_mn_std)
		team = {'id': i, 'mean': team_mean, 'alpha': alpha, 'beta': beta, 'seed': seed, 'wins': 0, 'losses': 0, 'score': 0, 'result': None, 'ideal': None}
		teams[i] = team
		evictable_dbtrs = np.delete(evictable_dbtrs, beta_ind, axis=1)
		evictable_dbtrs = np.delete(evictable_dbtrs, 0, axis=1)
	return teams

def copy_teams(teams):
	team_copy = {}
	for team_id in list(teams.keys()):
		copycat = {}
		og = teams[team_id]
		for attr in list(og.keys()):
			copycat[attr] = og[attr]
		team_copy[team_id] = copycat
	return team_copy

def pair_teams(round_num, teams, seed_rounds, dutch):
	pairings = []
	if round_num in seed_rounds:
		seeded = list(filter(lambda x: x['seed'], teams.values()))
		unseeded = list(filter(lambda x: not x['seed'], teams.values()))
		num_seeded = len(seeded)
		num_unseeded = len(unseeded)		
		for i in range(min(num_seeded, num_unseeded)):
			s_id = int(np.random.uniform(0, num_seeded - 1))
			u_id = int(np.random.uniform(0, num_unseeded - 1))
			seed_team = seeded[s_id]['id']
			scrub_team = unseeded[u_id]['id']
			del seeded[s_id]
			del unseeded[u_id]
			num_seeded -= 1
			num_unseeded -= 1
			pairings.append((seed_team, scrub_team))
		if num_seeded != 0:
			leftover = seeded
			num_leftover = len(leftover)
		elif num_unseeded != 0:
			leftover = unseeded
			num_leftover = len(leftover)
		else:
			num_leftover = 0	
		for i in range(num_leftover // 2):
			x_ind = int(np.random.uniform(0, num_leftover - 1))
			x_team = leftover[x_ind]['id']
			del leftover[x_ind]
			num_leftover -= 1
			y_ind = int(np.random.uniform(0, num_leftover - 1))
			y_team = leftover[y_ind]['id']
			del leftover[y_ind]
			num_leftover -= 1
			pairings.append((x_team, y_team))
	else:
		brackets = list(range(round_num))
		push_down = None
		bye = None
		for bracket in brackets:
			rel_teams = list(filter(lambda x: x['wins'] == bracket, teams.values()))
			ordered_teams = sorted(rel_teams, key=lambda x: x['score'], reverse=True)
			len_ordered_teams = len(ordered_teams)
			if push_down != None and len_ordered_teams % 2 == 1:
				ordered_teams.insert(0, push_down)
				push_down = None
				len_ordered_teams += 1
			elif push_down != None and bracket != brackets[-1]:
				new_push_down = ordered_teams[0]
				del ordered_teams[0]
				ordered_teams.insert(0, push_down)
				push_down = new_push_down
			elif push_down != None:
				bye = ordered_teams[-1]
				ordered_teams.insert(0, push_down)
				del ordered_teams[-1]
			elif len_ordered_teams % 2 == 1 and bracket != brackets[-1]:
				push_down = ordered_teams[0]
				del ordered_teams[0]
				len_ordered_teams -= 1
			elif len_ordered_teams % 2 == 1:
				bye = ordered_teams[-1]
				del ordered_teams[-1]
				len_ordered_teams -= 1
			if dutch:
				ordered_teams = ordered_teams[:len_ordered_teams // 2] + ordered_teams[len_ordered_teams // 2:][::-1]
			for i in range(len_ordered_teams // 2):
				x_team, y_team = ordered_teams[i]['id'], ordered_teams[-(i + 1)]['id']
				pairings.append((x_team, y_team))
		if bye != None:
			pairings.append(bye['id'], bye['id'])
	return pairings

def run_round(pairings, teams, judge_bias):
	results = {}
	for pair in pairings:
		x_team = teams[pair[0]]
		y_team = teams[pair[1]]
		x_id, x_alpha, x_beta = x_team['id'], x_team['alpha'], x_team['beta']
		y_id, y_alpha, y_beta = y_team['id'], y_team['alpha'], y_team['beta']
		x_team_value = np.random.normal(x_alpha[0], x_alpha[1]) + np.random.normal(x_beta[0], x_beta[1])
		y_team_value = np.random.normal(y_alpha[0], y_alpha[1]) + np.random.normal(y_beta[0], x_beta[1])
		x_team_score = np.random.normal(x_team_value, judge_bias)
		y_team_score = np.random.normal(y_team_value, judge_bias)
		if x_team_score > y_team_score:
			results[y_id] = (y_id, y_team_score, False)
			results[x_id] = (x_id, x_team_score, True)
		else:
			results[x_id] = (x_id, x_team_score, False)
			results[y_id] = (y_id, y_team_score, True)
	return results

def update_teams(teams, results):
	for team_id in list(results.keys()):
		result = results[team_id]
		teams[team_id]['score'] += result[1]
		if result[2]:
			teams[team_id]['wins'] += 1
		else:
			teams[team_id]['losses'] += 1
	return teams

def apda_tournament(num_rounds, teams, judge_bias, dutch):
	for i in range(1, num_rounds + 1):
		pairings = pair_teams(i, teams, [1], dutch)
		results = run_round(pairings, teams, judge_bias)
		teams = update_teams(teams, results)
	return teams

def check_results(num_rounds, teams):
	team_list = list(teams.values())
	error_teams = []
	num_errors = 0
	for i in range(len(team_list)):
		team = team_list[i]
		if team['wins'] + team['losses'] != num_rounds:
			num_errors += 1
			error_teams.append(team)
	return (num_errors, error_teams)

def para_tournament(num_rounds, teams, judge_bias, dutch):
	rec_results = {}
	old_results = {}
	for i in range(1, num_rounds + 1):
		teams = update_teams(teams, old_results)
		pairings = pair_teams(i, teams, [1, 2], dutch)
		old_results = rec_results
		rec_results = run_round(pairings, teams, judge_bias)
	teams = update_teams(update_teams(teams, old_results), rec_results)
	num_errors, error_teams = check_results(num_rounds, teams)
	if num_errors != 0:
		print('Team Errors:', num_errors)
		print('Error Teams:', error_teams)
	return teams

def assign_results(teams):
	team_list = list(teams.values())
	results_team_list = sorted(team_list, key=lambda x: (x['wins'], x['score']), reverse=True)
	ordered_team_list = sorted(team_list, key=lambda x: x['mean'], reverse=True)
	for i in range(len(team_list)):
		results_team = results_team_list[i]
		ordered_team = ordered_team_list[i]
		teams[results_team['id']]['result'] = i
		teams[ordered_team['id']]['ideal'] = i 
	return teams

def break_score(teams, dimensions, transform):
	team_list = list(teams.values())
	result_break = sorted(team_list, key=lambda x: x['result'])[:dimensions]
	ideal_break = sorted(team_list, key=lambda x: x['ideal'])[:dimensions]
	num_missed = 0
	infil_dist = 0
	miss_score = 0
	for i in range(dimensions):
		result_team = result_break[i]
		ideal_team = ideal_break[i]
		if result_team not in ideal_break:
			num_missed += 1
			infil_dist += result_team['ideal'] - (dimensions - 1)
		if ideal_team not in result_break:
			miss_score += transform(dimensions - ideal_team['ideal'])
	return (num_missed, infil_dist, miss_score)

def combination(n, r):
    return int((math.factorial(n)) / ((math.factorial(r)) * math.factorial(n - r)))

def pascals_triangle(rows):
    result = []
    for count in range(rows):
        row = [] 
        for element in range(count + 1): 
            row.append(combination(count, element))
        result.append(row)
    return result

def bracket_score(num_rounds, teams): #Unfinished
	pascal_row = pascals_trianle(num_rounds + 1)[-1]
	num_teams = len(teams)
	bracket_num = list(map(lambda x: num_teams * x * 2 ** (-num_rounds)))
	result_break = sorted(team_list, key=lambda x: x['result'])
	ideal_break = sorted(team_list, key=lambda x: x['ideal'])
	num_missed = 0
	infil_dist = 0
	miss_score = 0
	pass

def vector_distance(teams, dimensions, transform):
	team_list = list(teams.values())
	results_team_list = sorted(list(teams.values()), key=lambda x: (x['result']), reverse=True)
	results_vector = np.array(list(map(lambda x: x['ideal'], results_team_list)))[:dimensions]
	ideal_vector = np.array(list(range(0,len(team_list)))[::-1])[:dimensions]
	alt_ideal_vector = transform(ideal_vector)
	alt_results_vector = transform(results_vector)
	distance = np.linalg.norm(alt_ideal_vector - alt_results_vector)
	return distance
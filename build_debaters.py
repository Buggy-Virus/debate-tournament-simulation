import numpy as np
import math as m


def make_debaters(dbtr_num, dbtr_mn_mn, dbtr_mn_std, dbtr_std_mn, dbtr_std_std):
	dbtr_mns = np.random.normal(dbtr_mn_mn, dbtr_mn_std, dbtr_num)
	dbtr_stds = np.random.normal(dbtr_std_mn, dbtr_std_std, dbtr_num)
	dbtrs = np.concatenate(([dbtr_mns], [dbtr_stds]), axis=0)
	return dbtrs

def make_teams(dbtrs, dbtr_mn_mn, dbtr_mn_std):
	temp_mns = dbtrs[0,:]
	sorted_inds = np.artsort(temp_mns)
	evictable_dbtrs = dbtrs[:,sorted_inds]
	dbtr_num = len(temp_mns)
	cream_num = int(dbtr_num / 5)
	teams = {}
	for i in range(dbtr_num / 2):
		num_left = evictable_dbtrs.shape[1]
		beta_ind = np.random.uniform(1, min(cream_num, num_left - 1))
		alpha = (evictable_dbtrs[0,0], evictable_dbtrs[1,0])
		beta = (evictable_dbtrs[0,beta_ind], evictable_dbtrs[1,beta_ind])
		team_mean = alpha[0] + beta[0]
		seed = team_mean > np.random.normal(3 * dbtr_mn_mn, 2 * dbtr_mn_std)
		team = [i, team_mean, alpha, beta, seed, 0, 0, 0]
		teams[i] = team

def apda_round(round_num, teams, judge_bias):
	if round_num == 1:
		seeded = list(filter(lambda x: x[4], teams.values()))
		unseeded = list(filter(lambda x: x[4], teams.values()))
		num_seeded = len(seeded)
		num_unseeded = len(unseeded)
		for i in range(min(num_seeded, num_unseeded)):
			s_id = np.random.uniform(0, num_seeded - 1)
			u_id = np.random.uniform(0, num_unseeded - 1)
			seed_team = seeded[s_id]
			scrub_team = unseeded[u_id]
			del seeded[s_id]
			del unseeded[u_id]
			num_seeded -= 1
			num_unseeded -= 1
			seed_id, seed_alpha, seed_beta = seed_team[0], seed_team[2], seed_team[3]
			scrub_id, scrub_alpha, scrub_beta = scrub_team[0], scrub_team[2], scrub_team[3]
			seed_team_value = np.random.normal(seed_alpha[0], seed_alpha[1]) + np.random.normal(seed_beta[0], seed_beta[1])
			scrub_team_value = np.random.normal(scrub_alpha[0], scrub_alpha[1]) + np.random.normal(scrub_beta[0], scrub_beta[1])
			seed_team_score = np.random.normal(seed_team_value, judge_bias)
			scrub_team_score = np.random.normal(scrub_team_value, judge_bias)
			teams[seed_id][7] += seed_team_score
			teams[scrub_id][7] += scrub_team_score
			if seed_team_score > scrub_team_score:
				teams[seed_id][5] += 1
				teams[scrub_id][6] += 1
			else:
				teams[seed_id][6] += 1
				teams[scrub_id][5] += 1
		if num_seeded != 0:
			leftover = seeded
			num_leftover = len(leftover)
		elif num_unseeded != 0:
			leftover = unseeded
			num_leftover = len(leftover)
		else:
			num_leftover = 0
		for i in range(num_leftover / 2):
			x_ind = np.random.uniform(0, num_leftover - 1)
			x_team = leftover[x_ind]
			del leftover[x_ind]
			num_leftover -= 1
			y_ind = np.random.uniform(0, num_leftover - 1)
			y_team = leftover[y_ind]
			del leftover[y_ind]
			num_leftover -= 1
			x_id, x_alpha, x_beta = x_team[0], x_team[2], x_team[3]
			y_id, y_alpha, y_beta = y_team[0], y_team[2], y_team[3]
			x_team_value = np.random.normal(x_alpha[0], x_alpha[1]) + np.random.normal(x_beta[0], x_beta[1])
			y_team_value = np.random.normal(y_alpha[0], y_alpha[1]) + np.random.normal(y_beta[0], x_beta[1])
			x_team_score = np.random.normal(x_team_value, judge_bias)
			y_team_score = np.random.normal(y_team_value, judge_bias)
			teams[x_id] += x_team_score
			teams[y_id] += y_team_score
			if x_team_score > y_team_score:
				teams[x_id][5] += 1
				teams[y_id][6] += 1
			else:
				teams[x_id][6] += 1
				teams[y_id][5] += 1
	# You have to rewrite the non-first round Apda pairings
	else:
		brackets = list(range(round_num))
		for bracket in brackets:
			rel_teams = list(filter(lambda x: x[5] == bracket, teams.values()))
			len_rel_teams = len(rel_teams)
			for i in range(len_rel_teams / 2):
				x_ind = np.random.uniform(0, len_rel_teams - 1)
				x_team = rel_teams[x_ind]
				del rel_teams[x_ind]
				len_rel_teams -= 1
				y_ind = np.random.uniform(0, len_rel_teams - 1)
				y_team = rel_teams[y_ind]
				del rel_teams[y_ind]
				len_rel_teams -= 1
				x_id, x_alpha, x_beta = x_team[0], x_team[2], x_team[3]
				y_id, y_alpha, y_beta = y_team[0], y_team[2], y_team[3]
				x_team_value = np.random.normal(x_alpha[0], x_alpha[1]) + np.random.normal(x_beta[0], x_beta[1])
				y_team_value = np.random.normal(y_alpha[0], y_alpha[1]) + np.random.normal(y_beta[0], x_beta[1])
				x_team_score = np.random.normal(x_team_value, judge_bias)
				y_team_score = np.random.normal(y_team_value, judge_bias)
				teams[x_id] += x_team_score
				teams[y_id] += y_team_score
				if x_team_score > y_team_score:
					teams[x_id][5] += 1
					teams[y_id][6] += 1
				else:
					teams[x_id][6] += 1
					teams[y_id][5] += 1
	return teams

def pair_teams(round_num, teams, seed_rounds, dutch):
	pairings = []
	if round_num in seed_rounds:
		seeded = list(filter(lambda x: x[4], teams.values()))
		unseeded = list(filter(lambda x: x[4], teams.values()))
		num_seeded = len(seeded)
		num_unseeded = len(unseeded)		
		for i in range(min(num_seeded, num_unseeded)):
			s_id = np.random.uniform(0, num_seeded - 1)
			u_id = np.random.uniform(0, num_unseeded - 1)
			seed_team = seeded[s_id]
			scrub_team = unseeded[u_id]
			del seeded[s_id]
			del unseeded[u_id]
			num_seeded -= 1
			num_unseeded -= 1
			pairings.append([seed_team, scrub_team])
		if num_seeded != 0:
			leftover = seeded
			num_leftover = len(leftover)
		elif num_unseeded != 0:
			leftover = unseeded
			num_leftover = len(leftover)
		else:
			num_leftover = 0	
		for i in range(num_leftover / 2):
			x_ind = np.random.uniform(0, num_leftover - 1)
			x_team = leftover[x_ind]
			del leftover[x_ind]
			num_leftover -= 1
			y_ind = np.random.uniform(0, num_leftover - 1)
			y_team = leftover[y_ind]
			del leftover[y_ind]
			num_leftover -= 1
			pairings.append([x_team, y_team])
	else:
		brackets = list(range(round_num))
		for bracket in brackets:
			rel_teams = list(filter(lambda x: x[5] == bracket, teams.values()))
			ordered_teams = sorted(rel_teams, key=itemgetter(7))
			len_ordered_teams = len(ordered_teams)
			if dutch:
				ordered_teams = ordered_teams[:len_ordede_teams / 2] + ordered_teams[len_ordede_teams / 2:]
			for i in range(len_rel_teams / 2):
				x_team, y_team = ordered_teams[i], ordered_teams[-(i + 1)]
				pairings.append([x_team, y_team])
	return pairings

def run_round(pairings, teams, judge_bias):
	results = {}
	for pair in pairings:
		x_team = pair[0]
		y_team = pair[1]
		x_id, x_alpha, x_beta = x_team[0], x_team[2], x_team[3]
		y_id, y_alpha, y_beta = y_team[0], y_team[2], y_team[3]
		x_team_value = np.random.normal(x_alpha[0], x_alpha[1]) + np.random.normal(x_beta[0], x_beta[1])
		y_team_value = np.random.normal(y_alpha[0], y_alpha[1]) + np.random.normal(y_beta[0], x_beta[1])
		x_team_score = np.random.normal(x_team_value, judge_bias)
		y_team_score = np.random.normal(y_team_value, judge_bias)
		if x_team_score > y_team_score:
			results[x_id] = [x_id, x_team_score, True]
			results[y_id] = [y_id, y_team_score, False]
		else:
			results[x_id] = [x_id, x_team_score, False]
			results[y_id] = [y_id, y_team_score, True]
	return results

def update_teams(teams, results):
	for id in results.keys():
		result = results[id]
		teams[id][7] += result[1]
		if result[2]:
			teams[id][5] += 1
		else:
			teams[id][6] += 1
	return teams


def apda_tournament(num_rounds, teams, judge_bias):
	for i in range(1, num_rounds + 1):
		pairings = pair_teams(i, teams, [1], dutch)
		results = run_round(pairings, teams, judge_bias)
		teams = update_teams(i, teams, judge_bias)
	return teams

def para_tournmanet(num_rounds, teams, judge_bias, dutch):
	rec_results = {}
	old_results = {}
	for i in range(1, num_rounds + 1):
		teams = update_teams(teams, old_results)
		pairings = pair_teams(i - 1, teams, [1, 2], dutch)
		old_results = rec_results
		rec_results = run_round(pairings, teams, judge_bias)
	teams = update_teams(update_teams(teams, old_results), rec_results)
	return teams

dbtr_num = 1024
dbtr_mn_mn = 50
dbtr_mn_std = 15
dbtr_std_mn = 15
dbtr_std_std = 10
judge_bias = 20

dbtrs = make_debaters(dbtr_num, dbtr_mn_mn, dbtr_mn_std, dbtr_std_mn, dbtr_std_std)
teams = make_teams(dbtrs, dbtr_mn_mn, dbtr_mn_std)




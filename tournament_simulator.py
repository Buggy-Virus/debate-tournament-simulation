import debate_functions as df
import numpy as np
from time import gmtime, strftime
import uuid
import csv

with open('tournResults/results.csv', 'a', newline='') as csvfile:
	wr = csv.writer(csvfile, dialect='excel')
	wr.writerow(['test - ' + str(uuid.uuid4()), str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))])

team_sims = 100
tourn_sims = 1000

dbtr_num = 512
team_num = dbtr_num // 2
break_num = team_num // 8
dbtr_mn_mn = 1000
dbtr_mn_std = 300
dbtr_mn_mn_std = 0
dbtr_std_mn = 250
dbtr_std_std = 250
dbtr_std_mn_std = 0
judge_std = 800
judge_std_std = 0
apda_rounds = 6
para_rounds = 6

print('Total number of unique team sets: %d' % team_sims)
print('Total number of tournament simulations per team set: %d' % tourn_sims)
print('')

print(' - Beginning simulations - ')
print('')
apda_avg_dists = []
para_avg_dists = []
dpda_avg_dists = []
dara_avg_dists = []
apda_break_avg_dists = []
para_break_avg_dists = []
dpda_break_avg_dists = []
dara_break_avg_dists = []
apda_num_misseds = []
para_num_misseds = []
dpda_num_misseds = []
dara_num_misseds = []
apda_infil_dists = []
para_infil_dists = []
dpda_infil_dists = []
dara_infil_dists = []
apda_score_misseds = []
para_score_misseds = []
dpda_score_misseds = []
dara_score_misseds = []
for i in range(team_sims):
	if i % 10 == 0:
		print('Unique team sets completed: %d' % i)
	dbtrs = df.make_debaters(dbtr_num, np.random.normal(dbtr_mn_mn, dbtr_mn_mn_std), dbtr_mn_std, np.random.normal(dbtr_std_mn, dbtr_std_mn_std), dbtr_std_std)
	teams = df.make_teams(dbtrs, dbtr_mn_mn, dbtr_mn_std)
	apda_avg_dist_temp = 0
	para_avg_dist_temp = 0
	dpda_avg_dist_temp = 0
	dara_avg_dist_temp = 0
	apda_break_avg_dist_temp = 0
	para_break_avg_dist_temp = 0
	dpda_break_avg_dist_temp = 0
	dara_break_avg_dist_temp = 0
	apda_break_score_temp = 0
	para_break_score_temp = 0
	dpda_break_score_temp = 0
	dara_break_score_temp = 0
	for j in range(tourn_sims):
		#if j % 100 == 0:
		#	print('Tournaments completed: %d' % j)
		apda_teams = df.copy_teams(teams)
		para_teams = df.copy_teams(teams)
		dpda_teams = df.copy_teams(teams)
		dara_teams = df.copy_teams(teams)
		df.apda_tournament(apda_rounds, apda_teams, np.random.normal(judge_std, judge_std_std), False)
		df.para_tournament(para_rounds, para_teams, np.random.normal(judge_std, judge_std_std), False)
		df.apda_tournament(apda_rounds, dpda_teams, np.random.normal(judge_std, judge_std_std), True)
		df.para_tournament(para_rounds, dara_teams, np.random.normal(judge_std, judge_std_std), True)
		df.assign_results(apda_teams)
		df.assign_results(para_teams)
		df.assign_results(dpda_teams)
		df.assign_results(dara_teams)
		apda_avg_dists.append(df.vector_distance(apda_teams, team_num, lambda x: x))
		para_avg_dists.append(df.vector_distance(para_teams, team_num, lambda x: x))
		dpda_avg_dists.append(df.vector_distance(dpda_teams, team_num, lambda x: x))
		dara_avg_dists.append(df.vector_distance(dara_teams, team_num, lambda x: x))
		apda_break_avg_dists.append(df.vector_distance(apda_teams, break_num, lambda x: x))
		para_break_avg_dists.append(df.vector_distance(para_teams, break_num, lambda x: x))
		dpda_break_avg_dists.append(df.vector_distance(dpda_teams, break_num, lambda x: x))
		dara_break_avg_dists.append(df.vector_distance(dara_teams, break_num, lambda x: x))
		apda_nm, apda_id, apda_ms = df.break_score(apda_teams, break_num, lambda x: x)
		para_nm, para_id, para_ms = df.break_score(para_teams, break_num, lambda x: x)
		dpda_nm, dpda_id, dpda_ms = df.break_score(dpda_teams, break_num, lambda x: x)
		dara_nm, dara_id, dara_ms = df.break_score(dara_teams, break_num, lambda x: x)
		apda_num_misseds.append(apda_nm)
		para_num_misseds.append(para_nm)
		dpda_num_misseds.append(dpda_nm)
		dara_num_misseds.append(dara_nm)
		apda_infil_dists.append(apda_id)
		para_infil_dists.append(para_id)
		dpda_infil_dists.append(dpda_id)
		dara_infil_dists.append(dara_id)
		apda_score_misseds.append(apda_ms)
		para_score_misseds.append(para_ms)
		dpda_score_misseds.append(dpda_ms)
		dara_score_misseds.append(dara_ms)

apda_avg_dist = sum(apda_avg_dists) / len(apda_avg_dists)
para_avg_dist = sum(para_avg_dists) / len(para_avg_dists)
dpda_avg_dist = sum(dpda_avg_dists) / len(dpda_avg_dists)
dara_avg_dist = sum(dara_avg_dists) / len(dara_avg_dists)
apda_break_avg_dist = sum(apda_break_avg_dists) / len(apda_break_avg_dists)
para_break_avg_dist = sum(para_break_avg_dists) / len(para_break_avg_dists)
dpda_break_avg_dist = sum(dpda_break_avg_dists) / len(dpda_break_avg_dists)
dara_break_avg_dist = sum(dara_break_avg_dists) / len(dara_break_avg_dists)
apda_num_missed = sum(apda_num_misseds) / len(apda_num_misseds)
para_num_missed = sum(para_num_misseds) / len(para_num_misseds)
dpda_num_missed = sum(dpda_num_misseds) / len(dpda_num_misseds)
dara_num_missed = sum(dara_num_misseds) / len(dara_num_misseds)
apda_infil_dist = sum(apda_infil_dists) / len(apda_infil_dists)
para_infil_dist = sum(para_infil_dists) / len(para_infil_dists)
dpda_infil_dist = sum(dpda_infil_dists) / len(dpda_infil_dists)
dara_infil_dist = sum(dara_infil_dists) / len(dara_infil_dists)
apda_score_missed = sum(apda_score_misseds) / len(apda_score_misseds)
para_score_missed = sum(para_score_misseds) / len(para_score_misseds)
dpda_score_missed = sum(dpda_score_misseds) / len(dpda_score_misseds)
dara_score_missed = sum(dara_score_misseds) / len(dara_score_misseds)

print('')
print(' - Completed simulations - ')
print('')
print('Average distances from expected results')
print('Apda Tournament: %r' % apda_avg_dist)
print('Parallel Tournament: %r' % para_avg_dist)
print('Dutch Apda Tournament: %r' % dpda_avg_dist)
print('Dutch Parallel Tournament: %r' % dara_avg_dist)
print('')
print('Average distances from expected break')
print('Apda Tournament: %r' % apda_break_avg_dist)
print('Parallel Tournament: %r' % para_break_avg_dist)
print('Dutch Apda Tournament: %r' % dpda_break_avg_dist)
print('Dutch Parallel Tournament: %r' % dara_break_avg_dist)
print('')
print('Average number teams missing the break')
print('Apda Tournament: %r' % apda_num_missed)
print('Parallel Tournament: %r' % para_num_missed)
print('Dutch Apda Tournament: %r' % dpda_num_missed)
print('Dutch Parallel Tournament: %r' % dara_num_missed)
print('')
print('Average number dist of teams missing break')
print('Apda Tournament: %r' % apda_infil_dist)
print('Parallel Tournament: %r' % para_infil_dist)
print('Dutch Apda Tournament: %r' % dpda_infil_dist)
print('Dutch Parallel Tournament: %r' % dara_infil_dist)
print('')
print('Average break score')
print('Apda Tournament: %r' % apda_score_missed)
print('Parallel Tournament: %r' % para_score_missed)
print('Dutch Apda Tournament: %r' % dpda_score_missed)
print('Dutch Parallel Tournament: %r' % dara_score_missed)


with open('tournResults/results.csv', 'a', newline='') as csvfile:
	wr = csv.writer(csvfile, dialect='excel')
	wr.writerow([
		apda_rounds,
		para_rounds,
		apda_avg_dist, 
		para_avg_dist, 
		dpda_avg_dist, 
		dara_avg_dist,
		apda_break_avg_dist,
		para_break_avg_dist,
		dpda_break_avg_dist,
		dara_break_avg_dist,
		apda_num_missed, 
		para_num_missed, 
		dpda_num_missed,
		dara_num_missed,
		apda_infil_dist,
		para_infil_dist,
		dpda_infil_dist,
		dara_infil_dist,
		apda_score_missed,
		para_score_missed,
		dpda_score_missed,
		dara_score_missed])
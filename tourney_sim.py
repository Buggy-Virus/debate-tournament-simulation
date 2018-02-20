import debate_functions as df

dbtr_num = 16
team_num = dbtr_num // 2
dbtr_mn_mn = 200
dbtr_mn_std = 80
dbtr_std_mn = 80
dbtr_std_std = 60
judge_bias = 70

dbtrs = df.make_debaters(dbtr_num, dbtr_mn_mn, dbtr_mn_std, dbtr_std_mn, dbtr_std_std)
teams = df.make_teams(dbtrs, dbtr_mn_mn, dbtr_mn_std)
apda_teams = df.copy_teams(teams)
para_teams = df.copy_teams(teams)
dummy_teams = df.copy_teams(teams)

df.apda_tournament(5, apda_teams, judge_bias, False)
df.para_tournament(6, para_teams, judge_bias, False)
#print(para_teams == apda_teams)

for team_id in list(dummy_teams.keys()):
	dummy_teams[team_id]['wins'] = dummy_teams[team_id]['mean']
	dummy_teams[team_id]['score'] = -dummy_teams[team_id]['mean']

#print(df.vector_distance(apda_results, team_num, lambda x: x))
#print(df.vector_distance(para_results, team_num, lambda x: x))
#print(df.vector_distance(teams, team_num, lambda x: x))
print(df.vector_distance(dummy_teams, team_num, lambda x: x))

import csv
from time import gmtime, strftime

with open('tournResults/results.csv', 'w', newline='') as csvfile:
	wr = csv.writer(csvfile, dialect='excel')
	wr.writerow(['Wiped at: ' + str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))])

with open('tournResults/results.csv', 'a', newline='') as csvfile:
	wr = csv.writer(csvfile, dialect='excel')
	wr.writerow([
		'apda_rounds',
		'para_rounds',
		'apda_avg_dist', 
		'para_avg_dist', 
		'dpda_avg_dist', 
		'dara_avg_dist',
		'apda_break_avg_dist',
		'para_break_avg_dist',
		'dpda_break_avg_dist',
		'dara_break_avg_dist',
		'apda_num_missed', 
		'para_num_missed', 
		'dpda_num_missed',
		'dara_num_missed',
		'apda_infil_dist',
		'para_infil_dist',
		'dpda_infil_dist',
		'dara_infil_dist',
		'apda_score_missed',
		'para_score_missed',
		'dpda_score_missed',
		'dara_score_missed'])
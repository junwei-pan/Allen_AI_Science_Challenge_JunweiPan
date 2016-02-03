import sys

path_predict = sys.argv[1]

def cal_metrics(d_id_answer, d_id_answer_p):
    n_correct = 0
    n_total = len(d_id_answer.keys())
    for key in d_id_answer_p.keys():
        if d_id_answer.has_key(key):
            if d_id_answer[key] == d_id_answer_p[key]:
                n_correct += 1
    print n_correct, n_total, n_correct * 1.0 / n_total

d_id_answer = {}
d_id_answer_p = {}
path_train = '/home/jwpan/Labs/Kaggle/Allen_AI_Science_Challenge_JunweiPan/data/training_set.tsv'
for index, line in enumerate(open(path_train)):
    lst = line.strip('\n').split('\t')
    d_id_answer[lst[0]] = lst[2]

for index, line in enumerate(open(path_predict)):
    lst = line.strip('\n').split(',')
    d_id_answer_p[lst[0]] = lst[1].upper()


    

cal_metrics(d_id_answer, d_id_answer_p)

import json
import pymysql
import os

try:
    conn = pymysql.connect(host="101.132.109.217",
                            port=3306,
                            user="ieei",
                            passwd="Diangongdao_B",
                            charset="utf8",
                            db="Final_Homework")
    cursor = conn.cursor()
except:
    print('Fail to connect to the database.')

savedir = './responses'
filelist = os.listdir(savedir)

for i in filelist:
    id = i.split('.')[0]
    tagdict = {}
    with open(os.path.join(savedir, i), 'r', encoding='utf8') as f:
        tagsJson = json.load(f)
    for t in tagsJson['body']:
        tagdict[t['tag']] = t['cnt']
    cursor.execute('UPDATE Users \
        SET tags={} \
            where userId={};'.format(str(tagdict).strip('\{\}'),id))
conn.commit()
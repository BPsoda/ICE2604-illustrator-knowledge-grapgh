import requests
import json
import queue
import os
import time
import atexit
import threading
import pymysql

saveDir = './responses'
MAX_RETRIES = 3

visited = {}
visitingQueque = queue.Queue()


def getUsers():
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
    cursor.execute('SELECT userId FROM Users')
    users = cursor.fetchall()
    return users

def makeRequest(id):
    url='https://www.pixiv.net/ajax/user/{}/illusts/tags?lang=zh'.format(id)
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
        'cookie': 'first_visit_datetime_pc=2021-12-03+23%3A18%3A15; PHPSESSID=55008219_knaXXe1IPCq2xeku0Qa8N2gigVYrIsyh; p_ab_id=4; p_ab_id_2=6; p_ab_d_id=1674393652; yuid_b=QFEgaFc; device_token=213b5b47f3560987a1c0e47ee269e5a2; privacy_policy_agreement=3; c_type=19; privacy_policy_notification=0; a_type=0; b_type=1; tag_view_ranking=GX5cZxE2GY~b_G3UDfpN0~Ngz9KxUrJt~yZf1XmIy-U~RTJMXD26Ak~Lt-oEicbBr~gZWEWFTj-b~nriWjM9urd~jH0uD88V6F~qtVr8SCFs5~ELQp_nY0yD~ug04aDt3QG~K8esoIs2eW~LJo91uBPz4~aKhT3n4RHZ~FGFzwIh-Ko~HY55MqmzzQ~cxG7coNmIs~gRmNQHNbpA~kGYw4gQ11Z~HLWLeyYOUF~3W4zqr4Xlx~x1DDNnVZp9~1Xpow_4E0Y~kPAdgJpr8w~Bo7J-JbNu0~41c5XnZzc5~jNY6LUmcR6~lQGtQGMEhM~tMMdi_BJ8J~SQ0YGuzF-x~jhuUT0OJva~pzzjRSV6ZO~E5nFezN1vr~GV1cfVtr59~_H0rpHGXWO~kEFWIQSMy2~Sk4JRoM-tE~QfHe9Nt5we~W4Y5eToO0e~y489EcSQ8H~GF09UjQt_e~AtMuN7rnw5~BSkdEJ73Ii~fQ7hBDQ-Oy~QaKsoeqKi5~kQuLD4NvZr~r1vRjXa1Om~wKl4cqK7Gl~ylO3Y-Ere0~ko30YJxw7F~RolC8IrBVO~O7EUQ7rYfX~z0yXlSLXfe~88R-whWgJ8~6N7_jSUlOj~Kf_cVhHMOa~S4gozzBBKk~ljlQhziu7j~LiIVUDLEGO~1yIPTg75Rl~UmHg-r2a6H~nv7MfZGns6~5F_kzMEG3B~E-5uFZ2SN4~0JvURp1dNS~_pwIgrV8TB~0xsDLqCEW6~DcMFRkXx6k~Bd2L9ZBE8q~Avyrt8Dl6U~DADQycFGB0~Bx3XxRyJlI~MM6RXH_rlN~SqVgDNdq49~gpglyfLkWs~XMwx0jvD8S~23HIY-2l7F~Wm3hwR8POW~ojBJPtZVUi~N9pISanqh_~kMjNs0GHNN~I5npEODuUW~axApUC5dvK~CrFcrMFJzz~KsJYQeAdFM~EvP-chnyjU~QliAD3l3jr~d2oWv_4U1L~GHdWNxkeD5~BLhAVeDmI2~KSZM1779CN~q303ip6Ui5~tIqkVZurKP~MHugbgF9Xo~RS84WqiWyC; QSI_S_ZN_5hF4My7Ad6VNNAi=r:10:6; __cf_bm=WnCpT2N09Msnj2Gef3Ix6zX_sW_uO.MMQltFUB962tc-1639238529-0-AVvKnOhArWrFR9giuXmR6BfgnnuNsRxmudrlfqBV+pVTHzGdVKvuN2UcmBqvjSpzt/RKRV+RglRkJvRs/iixwcz8S/GV4FBLcBXJ2m/ECjJU',
        'referer': 'https://www.pixiv.net/users/{}/illustrations'.format(id),
    }
    proxy = '127.0.0.1:7890'
    proxies = {
        #'http': 'http://ieei:ieei_2021@crawler.acemap.cn:13130',
        #'https': 'https://ieei:ieei_2021@crawler.acemap.cn:13130',
        'http': 'http://'+proxy,
        'https': 'https://'+proxy,
    }
    #for retries in range(MAX_RETRIES + 1):
        #try:
    response = requests.get(url, headers=headers, proxies=proxies).json()
        #except:
        #    if retries == 0:
        #        print(threading.current_thread().name + ': Network error at {}. Retry in 3 seconds'.format(id))
        #    elif retries < MAX_RETRIES:
        #        print(threading.current_thread().name + ': Retry {} failed...'.format(retries+1))
        #    else:
        #        print(threading.current_thread().name + ' exited.')
        #        visitingQueque.put(id)
        #        exit()
        #    time.sleep(3)

    return response

def writeJSON(id, content):
    #try:
        with open(os.path.join(saveDir, str(id)+'.json'), 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        print('Saved to {}.json'.format(id))
    #except:
    #    print('Saving {}.json error!'.format(id))
     #   print(json.dumps(content, indent=2))
    

def loadVisited():
    visitedList = os.listdir(saveDir)
    for file in visitedList:
        id = file.split('.')[0]
        visited[id] = 1
    print('Loaded total {} visited records'.format(len(visitedList)))
    if (len(visitedList) > 0):
        with open('queue.txt', 'r') as fq:
            queuelist = fq.read().strip(',').split(',')
            for q in queuelist:
                visitingQueque.put(q)
            print('loaded visiting queue with length {}'.format(len(queuelist)))

@atexit.register
def saveQueue():
    with open('queue.txt', 'w') as fq:
        while not visitingQueque.empty():
            fq.write(visitingQueque.get()+',')
    print('Safely exited')


   
def crawler():
    startTime = time.time()
    epoch = 0
    while(len(visited) < 10000):
        if visitingQueque.empty():
            print('Queue is empty')
            exit()
        visitingId = visitingQueque.get()
        while (visitingId in visited) : 
            visitingId = visitingQueque.get()
        response = makeRequest(visitingId)
        writeJSON(visitingId, response)

        epoch += 1
        if (epoch % 10 == 0):
            timeSpent = int(time.time() - startTime)
            print(threading.current_thread().name + ' Epoch{}: total time {}m {}s'.format(epoch, timeSpent//60, timeSpent%60))

def spawnMulitiThread(thread_num):
    threadGroup = []
    for i in range(thread_num):
        threadGroup.append(threading.Thread(target=crawler))
        threadGroup[i].start()
    print('Spawned {} threads'.format(thread_num))
    
    
if __name__ == '__main__':
    users = getUsers()
    for i in users:
        visitingQueque.put(i[0])
    loadVisited()
    spawnMulitiThread(4)
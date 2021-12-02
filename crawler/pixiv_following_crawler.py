import requests
import json
import queue
import os
import time
import atexit
import threading

saveDir = './responses'
MAX_RETRIES = 3

visited = {}
visitingQueque = queue.Queue()


def makeRequest(id):
    url='https://www.pixiv.net/ajax/user/{}/following?offset=0&limit=24&rest=show&tag=&lang=zh'.format(id)
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
        'cookie': YOUR COOKIE,
        'referer': 'https://www.pixiv.net/users/{}/following'.format(id),
    }
    proxy = '127.0.0.1:7890'
    proxies = {
        'http': 'http//' + proxy,
        'https': 'https://' + proxy,
    }
    for retries in range(MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=headers, proxies=proxies).json()
            total = response['body']['total']
            for i in range(24, total, 24):
                url='https://www.pixiv.net/ajax/user/{}/following?offset={}&limit=24&rest=show&tag=&lang=zh'.format(id, i)
                partialResponse = requests.get(url, headers=headers, proxies=proxies).json()
                for user in partialResponse['body']['users']:
                    response['body']['users'].append(user)
            break
        except:
            if retries == 0:
                print(threading.current_thread().name + ': Network error. Retry in 3 seconds')
            elif retries < MAX_RETRIES:
                print(threading.current_thread().name + ': Retry {} failed...'.format(retries+1))
            else:
                print(threading.current_thread().name + ' exited.')
                visitingQueque.put(id)
                exit()
            time.sleep(3)

    visited[id] = 1
    for user in response['body']['users']:
        visitingQueque.put(user['userId'])
    return response

def writeJSON(id, content):
    try:
        with open(os.path.join(saveDir, id+'.json'), 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        print('Saved to {}.json'.format(id))
    except:
        print('Saving {}.json error!'.format(id))
        print(json.dumps(content, indent=2))
    

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
        visitingId = visitingQueque.get()
        while (visitingId in visited) : 
            visitingId = visitingQueque.get()
        response = makeRequest(visitingId)
        writeJSON(visitingId, response)

        epoch += 1
        if (epoch % 10 == 0):
            timeSpent = int(time.time() - startTime)
            print('Epoch{}: total time {}m {}s'.format(epoch, timeSpent//60, timeSpent%60))

def spawnMulitiThread(thread_num):
    threadGroup = []
    for i in range(thread_num):
        threadGroup.append(threading.Thread(target=crawler))
        threadGroup[i].start()
    print('Spawned {} threads'.format(thread_num))
    
    
if __name__ == '__main__':
    startId = '6662895'
    visitingQueque.put(startId)
    loadVisited()
    spawnMulitiThread(4)

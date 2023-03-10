# Make Illustrators Relationship Visible: Final Report of ICE2604 Group 2
<img src="img/logo.png"></img>


## Project Design
&emsp;&emsp;There are numerous awesome illustrators and delicate illustrations on the internet.But have you ever thought how they are related to each other?  
&emsp;&emsp;Our project aims to find and visualizing the relationship between each illustrator and illustration, by the means of **illustrator map** and **illustration ranking & trending**.  
### Illustrator map
&emsp;&emsp;By static the tags of one illustrator's works and turn it to a vector, we can represent the style of an author as a vector. Plotting it one a graph and add following relationship as edges, we get the illustrator map.  
<img src="img/word2vec.png"></img>

### Ranking & Trending
&emsp;&emsp;By analyze the create date, tags and bookmarks of illustration, we can point out the trending and make predictions.
<img src="img/trending.png"></img>


***
## Data and Crawler
### Crawler  
#### Website analysis
&emsp;&emsp;The data source of our project is pixiv.net, an online community of artist.  
The data we want include:  
- The basic information of a illustrator
- The following illustrators of one illustrator
- The recent works of illustrators
- The tags of an illustrator
- The basic information of an illustration
- The tags of an illustation

&emsp;&emsp;After looking into the XHR of the website, we find these information in two responses:   
- `https://www.pixiv.net/ajax/user/{userId}/illusts/tags?lang=zh`
- `https://www.pixiv.net/ajax/user/{userId}/following?offset={}&limit={}&rest=show&tag=&lang=zh`

&emsp;&emsp;The content looks like this:  
```json
// /ajax/user/15158551/following
{
	"error": false,
	"message": "",
	"body": {
		"users": [
			{
				"userId": "15871673",
				"userName": "ユウマ",
				"profileImageUrl": "https://i.pximg.net/user-profile/img/2019/10/27/18/42/33/16468488_e4f111bf6b5e635c0a71caf767e8cc03_170.jpg",
				"userComment": "...",
				"following": false,
				"followed": false,
				"isBlocking": false,
				"isMypixiv": false,
				"illusts": [
					{
						"id": "95076157",
						"title": "『生にしがみつく あまーい味がするね』",
						"illustType": 0,
						"xRestrict": 0,
						"restrict": 0,
						"sl": 4,
						"url": "https://i.pximg.net/c/250x250_80_a2/img-master/img/2021/12/28/00/52/42/95076157_p0_square1200.jpg",
						"description": "",
						"tags": [
							"創作",
							"オリジナル"
						],
						"userId": "15871673",
						"userName": "ユウマ",
						"width": 2480,
						"height": 3508,
						"pageCount": 1,
						"isBookmarkable": true,
						"bookmarkData": null,
						"alt": "#創作 『生にしがみつく あまーい味がするね』 - ユウマ的插画",
						"titleCaptionTranslation": {
							"workTitle": null,
							"workCaption": null
						},
						"createDate": "2021-12-28T00:52:42+09:00",
						"updateDate": "2021-12-28T00:52:42+09:00",
						"isUnlisted": false,
						"isMasked": false,
						"profileImageUrl": "https://i.pximg.net/user-profile/img/2019/10/27/18/42/33/16468488_e4f111bf6b5e635c0a71caf767e8cc03_50.jpg"
					},
					...
				],
				"novels": [],
				"acceptRequest": false
			},
			...
		],
		"total": 86,
		"followUserTags": [],
		"zoneConfig": {
			...
		},
		"extraData": {
			...
		}
	}
}
```
```json
// /ajax/user/15158551/illusts/tags?lang=zh
{
	"error": false,
	"message": "",
	"body": [
		{
			"tag": "オリジナル",
			"tag_translation": "原创",
			"tag_yomigana": "おりじなる",
			"cnt": 77
		},
		{
			"tag": "不思議の国のアリス",
			"tag_translation": "爱丽丝梦游仙境",
			"tag_yomigana": "ふしぎのくにのありす",
			"cnt": 2
		},
		...
	]
}
```

#### Make requests
&emsp;&emsp;We makes requests with the python module `requests`. Consider the anti reptile measures, we alse applied `clash` as the agent pool.  
&emsp;&emsp;The pixiv has relatively loose anti reptile measures. It only checks `referrence` and `Cookie`.  
```python
def makeRequest(id):
    url='https://www.pixiv.net/ajax/user/{}/following?offset=0&limit=24&rest=show&tag=&lang=zh'.format(id)
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
        'cookie': 'xxx',
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
            # retry after 3 seconds
            if retries == 0:
                print(': Network error. Retry in 3 seconds')
            elif retries < MAX_RETRIES:
                print(': Retry {} failed...'.format(retries+1))
            else:
                print(' exited.')
                visitingQueque.put(id)
                exit()
            time.sleep(3)

    visited[id] = 1
    for user in response['body']['users']:
        visitingQueque.put(user['userId'])
    return response
```

#### Cawl the whole net
&emsp;&emsp;After finishing one illustrator, we want the cawler to retieve information of other illustrators as well. This can be realized by crawling the following of the current illustrator.  
&emsp;&emsp;The following relationship constructs a directed graph of illustrators. If we traverse the net, we can get all the information we want. So, we search the net with BFS.  
```python
visited = {}
visitingQueque = queue.Queue()

while(len(visited) < 10000):
    visitingId = visitingQueque.get()
    while (visitingId in visited) : 
        visitingId = visitingQueque.get()
    response = makeRequest(visitingId)
```
&emsp;&emsp;Another version to crawl (the same solving ideas, but not as robust)
```python
import requests
import collections
import json
followers = []
ids=collections.deque()
id_used=[6662895]
def dumptojson(res):
    fp = open('homework.json', 'w', encoding='utf-8')
    json.dump(res, fp=fp, ensure_ascii=False)
def getSinglefollow1(id):
    follower=[{'main_id':id}]
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'cookie': 'xxx',
        'referer': 'https://www.pixiv.net/users/' + id + '/following',
    }
    url = 'https://www.pixiv.net/ajax/user/'+id+'/following?offset=0&limit=24&rest=show&tag=&lang=zh'
    response =requests.get(url, headers=headers).json()
    total = response['body']['total']
    for i in range(0,total,24):
        url='https://www.pixiv.net/ajax/user/'+id+'/following?offset='+str(i*24)+'&limit=24&rest=show&tag=&lang=zh'
        response = requests.get(url, headers=headers).json()
        users = response['body']['users']
        for user in users:
            id = user['userId']
            if(id not in id_used):
                ids.append(id)
            username = user['userName']
            illusts = user['illusts']
            imgs_id = []
            imgs_title = []
            imgs_url = []
            for illust in illusts:
                img_id = illust['id']
                img_title = illust['title']
                img_url = illust['url']
                imgs_id.append(img_id)
                imgs_title.append(img_title)
                imgs_url.append(img_url)
            follower.append({'id': id, 'username': username, 'img_id': imgs_id, 'img_title': imgs_title, 'img_url': imgs_url})
    return follower
def getAllfollow():
    global repeat
    follower=[{'main_id':'6662895'}]
    s=requests.session()
    url = 'https://www.pixiv.net/ajax/user/6662895/following?offset=0&limit=24&rest=show&tag=&lang=zh'
    headers1 = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'cookie': 'xxx',
        'referer': 'https://www.pixiv.net/users/6662895/following',
    }
    response = s.get(url, headers=headers1).json()
    total= response['body']['total']
    for i in range(0,total,24):
        url='https://www.pixiv.net/ajax/user/6662895/following?offset='+str(i)+'&limit=24&rest=show&tag=&lang=zh'
        response = s.get(url, headers=headers1).json()
        users = response['body']['users']
        for user in users:
            id = user['userId']
            ids.append(id)
            username=user['userName']
            illusts=user['illusts']
            imgs_id=[]
            imgs_title=[]
            imgs_url=[]
            for illust in illusts:
                img_id=illust['id']
                img_title=illust['title']
                img_url=illust['url']
                imgs_id.append(img_id)
                imgs_title.append(img_title)
                imgs_url.append(img_url)
            follower.append({'id':id,'username':username,'img_id':imgs_id,'img_title':imgs_title,'img_url':imgs_url})
        followers.append(follower)
    while(len(id_used)<10000):
        cur_id=ids.popleft()
        id_used.append(cur_id)
        followers.append(getSinglefollow1(cur_id))
    print(len(ids))
    return followers
res=getAllfollow()
dumptojson(res)
```
#### Multi-threading
&emsp;&emsp;Consider the network I/O takes up most of the time, it is necessary to apply multithreading. In this case, we spawned 4 threads.  
&emsp;&emsp;The `visitingQueue` can serve as the scheduler of the threads.  

### Data Sifting
&emsp;&emsp;To start with, what we had was the raw infomation we clawled from the Pixiv website in the form of **.json**. Which was heavily repeated and took up about 15GB memories after unzipped.   
&emsp;&emsp;The smallest one of them is like like this:
```json
{
  "error": false,
  "message": "",
  "body": {
    "users": [],
    "total": 0,
    "followUserTags": [],
    "zoneConfig": {
      ...
    },
    "extraData": {
      "meta": {
        ...
      }
    }
  }
}
```
&emsp;&emsp;The useful part of infomation is in ```json.load(f)["body"]["users"]```, and it's empty here, which means this user whose **userId** is ```"12138318"``` doesn't follow any other users. That's also the reason this file is the smallest.  
&emsp;&emsp;In the list of ```json.load(f)["body"]["users"]``` are all of the users that this user is following. And all we need to do is collect their userIds because **userId** can convey the infomation between them.  
&emsp;&emsp;However, there's one problem. Fisrt, we have no infomation about users themselves. If we colloct only the **userId**, all we would got is some numbers. And there's no more infomation about the user himself in his own json file. So we need to get the infomation from other users that are following this user. Doing this has a risk that if one user isn't being followed by other user then hinself would have no detailed infomation. We won't even know his userName.   
&emsp;&emsp;Luckily, we could prove that every user in the dir has someone following him except one because Huang haoxv collected them using DFS method and all of the users we saved must has someone following him except the first user chosen to be the start node.  
&emsp;&emsp;A single elem in ```json.load(f)["body"]["users"]``` would be like this:
```json
{
    "userId": "12331100",
    "userName": "飲用海",
    "profileImageUrl": "https://i.pximg.net/user-profile/img/2021/08/28/11/48/2021311004_c1b0ddbb900a4a72f3150b8f82de6026_170.jpg",
    "userComment": "",
    ...
    "illusts": [
      {
        "id": "94014080",
        "title": "まふゆ",
        ...
        "url": "https://i.pximg.net/c/250x250_80_a2/custom-thumb/img/2021/11/09/02/08/51/94014080_p0_custom1200.jpg",
        "description": "",
        "tags": [
          "プロジェクトセカイ",
          "プロセカ",
          "25時、ナイトコードで。",
          "朝比奈まふゆ",
          "プロセカ100users入り"
        ],
        ...
        "createDate": "2021-11-09T02:08:51+09:00",
        "updateDate": "2021-11-09T02:08:51+09:00",
        ...
      },
      ...
    ],
    ...
}
```
&emsp;&emsp;It's cozy that there're four illusts in ```json.load(f)["body"]["users"]["illusts"]```. As you could see, the infomation we could collect contains:

- userId
- userName
- userComment
- profileImageUrl
- illusts
- createDate

&emsp;&emsp;And with the following relation we got, we made two tables in MySQL like this:
|Users|illusts|
|:-:|:-:|
|![](./img/xjq_1.png)|![](./img/xjq_2.png)|

&emsp;&emsp;Here's the code that fills in the table:
```python
import json,os,pymysql
from tqdm import tqdm

users={files[:files.find('.')] for files in os.listdir("responses")}
d1,d,imgs,d2={},{},{},{}
for User_ID in tqdm(users):
    with open("responses/{}.json".format(User_ID),"rb") as f:
        a=json.load(f)["body"]["users"]
    d1_User_ID=[]
    for _ in a:
        if _["userId"] in users:
            d1_User_ID.append(_["userId"])
            if not _["userId"] in d:
                user={att:_[att] for att in ["userId","userName","profileImageUrl","userComment"]}
                user["illusts"]=[{att:his_imgs[att] for att in ["id","title","url","tags"]} for his_imgs in _["illusts"]]
                d[_["userId"]]=user
            for img in _["illusts"]:
                if not img["id"] in imgs:
                    imgs[img["id"]]={i:img[i] for i in ["id","title","url","tags","userId","createDate"]}
    d1[User_ID]=d1_User_ID
del User_ID,a,d1_User_ID,_,user,img
for userId in tqdm(d1):
    for his_follows in d1[userId]:
        if his_follows in d2:
            d2[his_follows]=d2[his_follows]+[userId]
        else:
            d2[his_follows]=[userId]
del userId,his_follows

conn=pymysql.connect(
    host="XXX",
    port=xxx,
    user='XXX',
    password="XXXX",
    database='XXXX',
    charset='utf8mb4'
)
cursor=conn.cursor()

tmp=[[d[userId][i] for i in ["userId","userName","profileImageUrl","userComment"]]+[",".join([_["id"] for _ in d[userId]['illusts']]),",".join(d1[userId]),len(d1[userId]),",".join(d2[userId]),len(d2[userId])] for userId in d]
cursor.executemany("INSERT INTO Users (userId,userName,profileImageUrl,userComment,illusts,following,following_count,follower,follower_count) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",tmp)
conn.commit()
tmp=[[imgs[img_id][k] for k in ["id","title","url"]]+[",".join(imgs[img_id]["tags"])]+[imgs[img_id][k] for k in ["userId","createDate"]] for img_id in imgs]
cursor.executemany("INSERT INTO illusts (id,title,url,tags,userId,createDate) VALUES (%s,%s,%s,%s,%s,%s)",tmp)
conn.commit()
```
&emsp;&emsp;Also, we used ```tqdm``` to add a process bar to visualize the procedure of the program.
***
## Search Engine
&emsp;&emsp;The search engine is based on Elastic Search. We aim to search illustrators and illustrations by id, name, tag.  
&emsp;&emsp;Because we want the exact id, so the id is `keyword` type. The name/title and tags are text type.  
&emsp;&emsp;Since the name, title and tags contain Chinese and Japanese, we tokenize them with an plugin `analysis-icu`.  
```python
# index setting
illusts_mappings = {
    "settings": {
        "index": {
            "analysis": {
                "analyzer": {
                    "cjk_analyzer": {
                        "type": "custom",
                        "tokenizer" : "icu_tokenizer"
                    }
                }
            }
        }
    },
    "mappings" : {
        "properties": {
            "id": {
                "type": "keyword",
            },
            "title": {
                "type": "text",
                "analyzer": "cjk_analyzer"
            },
            "url": {
                "type": "keyword",
            },
            "tags": {
                "type": "text",
                "analyzer": "simple"
            },
            "userId": {
                "type": "keyword",
            },
            "createDate": {
                "type": "keyword",
            },
            "bookmark_count": {
                "type": "long",
            }
        }
    }
}

# searcher
def search(self, key, method):
    ''' 搜索，返回一个由字典组成的列表结果。
    若没有满足条件返回None。
    method可以为 id, title, tags, userId, userName。
    当选取前三个时返回的是插画，选取后两个时返回的是画师'''
    searchQuery = {
        'query': {
            'match': {
                method: key
            }
        }
    }
    if method in ['id', 'title', 'tags']:
        result = self.es.search(index="illusts_index", body=searchQuery)
        return result['hits']['hits']
    elif method in ['userId', 'userName']:
        result = self.es.search(index='users_index', body=searchQuery)
        return result['hits']['hits']
    else:
        print('No match result!')
        return None
```
***
## Visualization
### Data Charts 
&emsp;&emsp;We prepared a page called "statics" to show our data size and ranking lists of some data, aiming to enrich the content of our site.

&emsp;&emsp;It mainly consists of 4 pictures, an authors ranking list,a tags ranking list, a development tendency chart of the tags in last 7 years and the word cloud picture of all the tags.

&emsp;&emsp;Using the echarts, we can easily make these pictures.

#### Tools Used
```html
<script src="/static/echarts.js"></script>
<script src="/static/jquery.js"></script>
<script src="/static/echarts-wordcloud1.js"></script>
```
&emsp;&emsp;The third one is used for the wordcloud picture. 
#### Data Acquisition 
&emsp;&emsp;All the data come from our crawler and database.

&emsp;&emsp;Through two ways, we can let the charts get the data.
##### 1. put the data in the charts(direct access)
like this:
```js
series: [...
    data: [51,74,147,199,395,667,3125]
    ...]
```
##### 2. put the data in the main.cpp(Asynchronous access)
&emsp;&emsp;It's more convenient to change the data througe this way.

like this:
```python
@app.route('/data', methods=['GET'])
def get_data():
    data={
    "categories":["巨乳","魅惑の谷間","Fate/GrandOrder","おっぱい" ,"女の子","オリジナル"],
    "data":[753,  769  ,896,1184,2990,4306],
     }
    return json.dumps(data)

```

#### Layout
&emsp;&emsp;The four pictures are put on the website side by side.
```html

<div id="main1" style="width: 50%;height: 600px;float:left;border: 1px solid rgb(0, 0, 0);"></div>
<div id="main3" style="width: 50%;height: 600px;float:right;border: 1px solid rgb(0, 0, 0);"></div>
<div id="main2" style="width: 50%;height: 700px;float:left;border: 1px solid rgb(0, 0, 0);"></div>
<div id="main4" style="width: 50%;height: 700px;float:right;border: 1px solid rgb(0, 0, 0);"></div>

```
#### The Pictures
##### 1. Two Normal Bar Charts.
&emsp;&emsp;The Asynchronous access one is like this:
```js
var mychart =echarts.init(document.getElementById('main1'),'dark');
$.getJSON('/data').done(function(data){
    mychart.setOption({
    color: [ '#00DDFF'],
    title:{
    text: 'Top6 Tags',
    x:'center',
    top:'20',
    textStyle: {
    "fontSize": 24
    },
    },
    tooltip:{},
    legend:{
        data:["作品数"],
        textStyle: {
        "fontSize": 16
    },
    x:'right',
    },
   yAxis:{
        type : 'category',
        data:data.categories,
        
        axisLabel: {
            show: true,
            textStyle: {
                color: '#FFFFFF',
            },
            fontSize: 12.5,
            interval:0,  
            rotate:45  

        },
        
    },

    xAxis:{ axisLabel: {
            show: true,
            textStyle: {
                color: '#FFFFFF',
            },
            fontSize: 12.5,
        },},
    series:[
        {
            name:'作品数',
            type:'bar',
            data:data.data,
            
        }
    ]
    });

```
&emsp;&emsp;The direct access is similar, but cut
```js
$.getJSON('/data').done(function(data)
```
&emsp;&emsp;The two pictures look like:

<img src="img/Top6 Painters.png"></img>

<img src="img/Top6 Tags.png"></img>

##### 2. The Tendency Chart.
&emsp;&emsp;It's based on the basic bar charts but change the way to deal with the data.

&emsp;&emsp;In the "series" section, add the "areaStyle".

```js
series: [
            ...
            showSymbol: false,
            areaStyle: {
                opacity: 0.8,
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                    offset: 0,
                    color: 'rgba(255, 131, 0)'
                },
                {
                    offset: 1,
                    color: 'rgba(124, 62, 76)'
                }
                ])
            },
            emphasis: {
                focus: 'series'
            },
            data: ...
        ......
        ]
```
&emsp;&emsp;It makes a picture like this, which can exhibit the tendency through years.

<img src="img/Tags tendency.png"></img>

&emsp;&emsp;It also can just focus on partial data like this.

<img src="img/tags tendency1.png"></img>

##### 3. The Wordcloud Chart.

&emsp;&emsp;We used a new js file to provide the function to make the wordcloud chart.
```js
<script src="/static/echarts-wordcloud1.js"></script>
```
&emsp;&emsp;The chart is a little different from the bar charts, mainly the "series" part ,it used the color gradient function

&emsp;&emsp;The different part is like this:
```js
    series: [ {
    type: 'wordCloud',
    gridSize: 2,
    sizeRange: [12, 50],
    rotationRange: [-90, 90],
    width: 1000,
    height: 1000,
    drawOutOfBound: true,
    textStyle: {
        
            color: function () {
                return 'rgb(' + [
                    Math.round(Math.random() * 160),
                    Math.round(Math.random() * 160),
                    Math.round(Math.random() * 160)
                ].join(',') + ')';
            
        },
        emphasis: {
            shadowBlur: 10,
            shadowColor: '#333'
        }
    },
    data:data.word,}]
```
&emsp;&emsp;The wordcloud picture look like this:
<img src="img/echarts.png"></img>


### Map: Data Visualization Tasks and Realization Ideas
#### The purpose of data visualization

&emsp;&emsp;In our division of labor, visualization mainly includes the establishment of a relationship graph from the collected illustrators information, which is used to reflect the following relationship between the illustrators as a directed graph. 



#### Realization idea 

&emsp;&emsp;Let's first establish the relationship graph between painters. The information we obtained from Pixiv includes followers of illustrators. So we set up several illustrators nodes and add directed edges between the nodes according to the followers information. For example, if illustrator A’s followers include illustrator B, we add an edge from node B to node A. 


&emsp;&emsp;Then we cluster the illustrators nodes by **Kmeans**. Because the information of the illustrators is collected and the tag information of the illustrations is recorded, we have counted the frequency of each tag appearing in each illustrators, through the tags between the illustrators similarity to cluster. 


#### Major difficulty 

&emsp;&emsp;The main software used in the visualization process is Gephi. However, when using Gephi for clustering algorithm, since the graph density is too large, it is difficult to form a clear classification between nodes, but it appears as a fairly uniform ball. 


#### Final solution

&emsp;&emsp;In order to classify the painter nodes clearly, we use the **Principal Component Analysis (PCA)** algorithm. Consider each illustrator's tags as a multi-dimensional vector, and the frequency of each tag is the value of the corresponding component of the vector; tags not owned by the illustrator are the components with a value of 0. Through this process, we created an N-dimensional vector corresponding to each illustrator in an N-dimensional vector space, and then reduced the N-dimensional vector to two dimensions to draw the corresponding two-dimensional image. 

&emsp;&emsp;After the process of the PCA algorithm, the data is clustered according to the tags information of each node. Export the coordinate information and classification information of each node as a table file, and then import it into Gephi, using Geo Layout to lay out, coloring according to the coordinates, and finally output the svg image. 

#### Final code 
```python
import pymysql
# retrieve data
conn=pymysql.connect(
    host="xxx",
    port=xxxx,
    user='xxx',
    password="xxx",
    database='xxx',
    charset='utf8mb4'
)
cursor=conn.cursor()
cursor.execute("SELECT userId,tags from Users")
a=cursor.fetchall()
d["a"]=a

b={str(a[i][0]):eval("{"+a[i][1]+"}") for i in range(len(a))}

# select tags for analysis
tags={}
for i in b:
    for j in b[i]:
        if j in tags:
            tags[j]+=1
        else:
            tags[j]=1

tags={i for i in tags if tags[i]>50}

tags=list(tags)

tmp_tags={i:ii for ii,i in enumerate(tags)}

import numpy as np
def func(x:dict):
    '''word2vec'''
    ret=np.zeros(shape=(len(tags),))
    for i in x:
        if i in tmp_tags:
            ret[tmp_tags[i]]=x[i]
    total = sum(ret)
    if (total > 0):
        ret /= total
    return ret

userIds=list(b.keys())

outp=np.vstack((func(b[i]) for i in userIds))

outp.shape
>>>(4167, 3681)


# Standardization
from sklearn.preprocessing import StandardScaler
x = StandardScaler().fit_transform(outp)
# PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)

# convert to position on the plot
pC=principalComponents*500

pC[:,0]*=1.5
pC[:,1]/=1.5

position={}
for i in range(len(userIds)):
    position["id_"+userIds[i]]=pC[i]

# write to csv
from openpyxl import Workbook
book = Workbook()
sheet = book.active
sheet.cell(row=1, column=1).value="userId"
sheet.cell(row=1, column=2).value="x"
sheet.cell(row=1, column=3).value="y"
for i in range(len(userIds)):
    sheet.cell(row=i+2, column=1).value = userIds[i]
    sheet.cell(row=i+2, column=2).value = pC[i][0]
    sheet.cell(row=i+2, column=3).value = pC[i][1]

book.save('write2cell.xlsx')
```


```python
import matplotlib.pyplot as plt
plt.scatter(principalComponents[:,0],principalComponents[:,1])
plt.show()
```


![png](img/PCA2_21_0.png)



```python
# Clustering
from scipy.cluster.vq import whiten
from sklearn.cluster import KMeans
whitened = whiten(principalComponents)
kmeans = KMeans(n_clusters=5, random_state=0).fit(whitened)
plt.scatter(whitened[kmeans.labels_==0][:,0], whitened[kmeans.labels_==0][:,1], c='b')
plt.scatter(whitened[kmeans.labels_==1][:,0], whitened[kmeans.labels_==1][:,1], c='c')
plt.scatter(whitened[kmeans.labels_==2][:,0], whitened[kmeans.labels_==2][:,1], c='g')
plt.scatter(whitened[kmeans.labels_==3][:,0], whitened[kmeans.labels_==3][:,1], c='k')
plt.scatter(whitened[kmeans.labels_==4][:,0], whitened[kmeans.labels_==4][:,1], c='m')
```
![png](img/PCA2_22_1.png)



```python
print(kmeans.inertia_)
print(kmeans.n_features_in_)
```

    1401.1819077759367
    2
    
```python
# Add text to the graph
from bs4 import BeautifulSoup
with open("index.html","r",encoding="utf-8") as f:
    soup=BeautifulSoup(f.read(),"lxml")

dxdy={}
for i in soup.find_all("circle"):
    dxdy[i["class"][0]]=[position[i["class"][0]][0]-float(i["cx"]),position[i["class"][0]][1]-float(i["cy"])]
    i["cx"]=str(position[i["class"][0]][0])
    i["cy"]=str(position[i["class"][0]][1])

for i in soup.find_all("path"):
    _=i["d"].split()
    _[1]="{},{}".format(*position[i["class"][0]])
    _[3]="{},{}".format(*position[i["class"][1]])
    i["d"]=" ".join(_)

for i in soup.find_all("text"):
    i["x"]=str(float(i["x"])+dxdy[i["class"][0]][0])
    i["y"]=str(float(i["y"])+dxdy[i["class"][0]][1])

with open("jl.html","w",encoding="utf-8") as f:
    f.write(soup.prettify())
```
***
## Website
### Page harmony
&emsp;&emsp;The most difficult part of building a website is that it must combine all the work done that realize different features of it. At first, we didn't realize that our teamate will use so many different frames such as Jquery and Bootrap，not mention that the style is quite contradictary，the frames themselves arouse conficts.the most typical one is that the vue and flask all need `[]` to bond statics, so mistake like picture below happened.
![](img/hcy_01.png)
&emsp;&emsp;That is Vue and Flask's Jinja2 module reuse problems.  
&emsp;&emsp;To slove this, we use code below:
```python
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'
```
&emsp;&emsp;But later we found different CSS can result that the page seems horribly messy. And things become troublesome especialy when it comes to locate which css make it perform like that. So although we want to make some interaction body using Vue, page harmony become so important that we have to weigh.  
&emsp;&emsp;At first we try to use Bootstrap, but it seems not as perfect as we thought. Here's a rendering of our first version
![](img/hcy_02.jpg)
&emsp;&emsp;And the same, because Bootstrap's css is confict with one of our teammate's css, we have to find a template that is more compatible.  
&emsp;&emsp;So we choose NicePage, 
because all it's headers are approximately the same.
```HTML
<html style="font-size: 16px;">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8">
    <meta name="keywords" content="Illustration &amp;amp; Art Guide">
    <meta name="description" content="">
    <meta name="page_type" content="np-template-header-footer-from-plugin">
    <title>Home</title>
    <link rel="stylesheet" href="/static/nicepage.css" media="screen">
<link rel="stylesheet" href="/static/Home.css" media="screen">
    <script class="u-script" type="text/javascript" src="/static/jquery.js" defer=""></script>
    <script class="u-script" type="text/javascript" src="/static/nicepage.js" defer=""></script>
    <meta name="generator" content="Nicepage 4.1.0, nicepage.com">
    <link id="u-theme-google-font" rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:100,100i,300,300i,400,400i,500,500i,700,700i,900,900i|Open+Sans:300,300i,400,400i,600,600i,700,700i,800,800i">
    <link id="u-page-google-font" rel="stylesheet" href="https://fonts.googleapis.com/css?family=Oswald:200,300,400,500,600,700">
    
    
    
    
    <script type="application/ld+json">{
		"@context": "http://schema.org",
		"@type": "Organization",
		"name": "",
		"logo": "images/e1480079-83f8-6e77-e4f6-3ec006fc0d60.jpg"
}</script>
    <meta name="theme-color" content="#478ac9">
    <meta property="og:title" content="Home">
    <meta property="og:type" content="website">
  </head>
  <body class="u-body u-overlap"><header class="u-align-center-xs u-border-1 u-border-grey-25 u-clearfix u-header u-header" id="sec-d1d3"><div class="u-clearfix u-sheet u-sheet-1">
        <a href="https://nicepage.com" class="u-image u-logo u-image-1" data-image-width="1080" data-image-height="1080">
          <img src="/static/images/20211223145559.png" class="u-logo-image u-logo-image-1">
        </a>
        <form action="search" method="post" class="u-border-1 u-border-grey-15 u-search u-search-right u-search-1">
          <button class="u-search-button" type="submit">
            <span class="u-search-icon u-spacing-10 u-text-grey-40">
              <svg class="u-svg-link" preserveAspectRatio="xMidYMin slice" viewBox="0 0 56.966 56.966" style=""><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#svg-b04b"></use></svg>
              <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="svg-b04b" x="0px" y="0px" viewBox="0 0 56.966 56.966" style="enable-background:new 0 0 56.966 56.966;" xml:space="preserve" class="u-svg-content"><path d="M55.146,51.887L41.588,37.786c3.486-4.144,5.396-9.358,5.396-14.786c0-12.682-10.318-23-23-23s-23,10.318-23,23  s10.318,23,23,23c4.761,0,9.298-1.436,13.177-4.162l13.661,14.208c0.571,0.593,1.339,0.92,2.162,0.92  c0.779,0,1.518-0.297,2.079-0.837C56.255,54.982,56.293,53.08,55.146,51.887z M23.984,6c9.374,0,17,7.626,17,17s-7.626,17-17,17  s-17-7.626-17-17S14.61,6,23.984,6z"></path><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>
            </span>
          </button>
          <input name="info" class="u-search-input" type="search" name="search" value="" placeholder="Search">
        </form>
        <nav class="u-align-left u-menu u-menu-dropdown u-nav-spacing-25 u-offcanvas u-menu-1">
          <div class="menu-collapse">
            <a class="u-button-style u-nav-link" href="#" style="padding: 4px 0px; font-size: calc(1em + 8px);">
              <svg class="u-svg-link" preserveAspectRatio="xMidYMin slice" viewBox="0 0 302 302" style=""><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#svg-7b92"></use></svg>
              <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="svg-7b92" x="0px" y="0px" viewBox="0 0 302 302" style="enable-background:new 0 0 302 302;" xml:space="preserve" class="u-svg-content"><g><rect y="36" width="302" height="30"></rect><rect y="236" width="302" height="30"></rect><rect y="136" width="302" height="30"></rect>
</g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>
            </a>
          </div>
          <div class="u-custom-menu u-nav-container">
            <ul class="u-nav u-unstyled u-nav-1"><li class="u-nav-item"><a class="u-button-style u-nav-link u-text-active-palette-1-base u-text-hover-palette-2-base" href="/home" style="padding: 10px 20px;">Home</a>
            </li><li class="u-nav-item"><a class="u-button-style u-nav-link u-text-active-palette-1-base u-text-hover-palette-2-base" href="/static" style="padding: 10px 20px;">Statics</a>
            </li><li class="u-nav-item"><a class="u-button-style u-nav-link u-text-active-palette-1-base u-text-hover-palette-2-base" href="/map" style="padding: 10px 20px;">Map</a>
            </li><li class="u-nav-item"><a class="u-button-style u-nav-link u-text-active-palette-1-base u-text-hover-palette-2-base" href="/search" style="padding: 10px 20px;">Search</a>
            </li><li class="u-nav-item"><a class="u-button-style u-nav-link u-text-active-palette-1-base u-text-hover-palette-2-base" href="/tags" style="padding: 10px 20px;">Tags</a>
            </li></ul>
                      </div>
                      <div class="u-custom-menu u-nav-container-collapse">
                        <div class="u-align-center u-black u-container-style u-inner-container-layout u-opacity u-opacity-95 u-sidenav">
                          <div class="u-inner-container-layout u-sidenav-overflow">
                            <div class="u-menu-close"></div>
                            <ul class="u-align-center u-nav u-popupmenu-items u-unstyled u-nav-2"><li class="u-nav-item"><a class="u-button-style u-nav-link" href="/home" style="padding: 10px 20px;">Home</a>
            </li><li class="u-nav-item"><a class="u-button-style u-nav-link" href="/static" style="padding: 10px 20px;">Statics</a>
            </li><li class="u-nav-item"><a class="u-button-style u-nav-link" href="/map" style="padding: 10px 20px;">Map</a>
            </li><li class="u-nav-item"><a class="u-button-style u-nav-link" href="/search" style="padding: 10px 20px;">Search</a>
            </li><li class="u-nav-item"><a class="u-button-style u-nav-link" href="/tags" style="padding: 10px 20px;">Tags</a>
            </li></ul>
              </div>
            </div>
            <div class="u-black u-menu-overlay u-opacity u-opacity-70"></div>
          </div>
        </nav>
      </div></header>
```
&emsp;&emsp;And different page can use different css which make it easy to locate and make changes.
![](img/hcy_03.jpg)
&emsp;&emsp;For example, we want to change some image in the html, we first find it's id equal to u-image-1, and css is map.css,then we turn to map.css and
![](img/hcy_04.jpg)
### Valid Picture 
&emsp;&emsp;We already have the **url** of each image. However, the **url** is not only forbidden here but also could not request directly because their anti-crawler methods. At first, we thought of save all of the pictures to loacl. But after computing the approximate sizeof the images, we decided to give up. Not only because wet's too large to store, but also because the data charges are costly.   
&emsp;&emsp;Suddenly, we thought of getting the image from other source. We found a mirror website of Pixiv and found that the **url** of this website is kind of similar to Pixiv. What we would have to do is converting ```"https://i.pximg.net/c/250x250_80_a2/img-master/img/2010/09/22/00/19/05/13399152_p0_square1200.jpg"``` to ```https://proxy.pixivel.moe/img-original/img/2010/09/22/00/19/05/13399152_p0.jpg``` or ```https://proxy-jp1.pixivel.moe/c/600x1200_90/img-master/img/2010/09/22/00/19/05/13399152_p0_master1200.jpg```.   
&emsp;&emsp;Here comes the problem that this mirror website is not good enough to provide all images we needed. In other word, some of the **url** is not valid.   
&emsp;&emsp;To avoid our website from showing a lot of broken images, we need to check all the urls. Which is quite time consuming. Here's the code:
```python
import pymysql,json,os
from tqdm import tqdm
users=set()
for files in os.listdir("responses"):
    users.add(files[:files.find('.')])
imgs=dict()
for User_ID in tqdm(users):
    with open("responses/{}.json".format(User_ID),"rb") as f:
        for _ in json.load(f)["body"]["users"]:
            if _["userId"] in users:
                for img in _["illusts"]:
                    if not img["id"] in imgs:
                        imgs[img["id"]]={i:img[i] for i in ["id","title","url","tags","userId","createDate"]}
conn=pymysql.connect(
    host="XXX",
    port=xxx,
    user='XXX',
    password="XXXX",
    database='XXXX',
    charset='utf8mb4'
)
cursor=conn.cursor()
tmp=[[imgs[img_id][k] for k in ["id","title","url"]]+[",".join(imgs[img_id]["tags"])]+[imgs[img_id][k] for k in ["userId","createDate"]] for img_id in imgs]
cursor.executemany("INSERT INTO illusts (id,title,url,tags,userId,createDate) VALUES (%s,%s,%s,%s,%s,%s)",tmp)
conn.commit()
```
&emsp;&emsp;&emsp;&emsp;This took us about a whole day. And I'd have to run another. (```url_foruse``` is a newly added col which stores the **url** that could be requestd directly)
```python
import requests,pymysql
from tqdm import tqdm
conn=pymysql.connect(
    host="XXX",
    port=xxx,
    user='XXX',
    password="XXXX",
    database='XXXX',
    charset='utf8mb4'
)
cursor=conn.cursor()
cursor.execute("SELECT id,url from illusts where url_foruse is NULL")
ills=cursor.fetchall()

hea="""Referer: XXXX
sec-ch-ua: XXXX
sec-ch-ua-mobile: XXXX
sec-ch-ua-platform: XXXXX
User-Agent: XXXXX""".split('\n')
hea={i[:i.find(':')].strip():i[i.find(':')+1:].strip() for i in hea}

for ill in tqdm(ills):
    _url="https://proxy.pixivel.moe/img-original/img/"+ill[1][ill[1].find("/img/")+len("/img/"):].replace("_square1200.jpg",".jpg")
    resp=requests.get(_url,stream=True)
    if resp.status_code==200:
        cursor.execute("UPDATE illusts SET url_foruse=%s WHERE id=%s",(_url,ill[0]))
        conn.commit()
    else:
        _url="https://proxy-jp1.pixivel.moe/c/600x1200_90/img-master/img/"+ill[1][ill[1].find("/img/")+len("/img/"):ill[1].find(ill[0])+len(ill[0])]+"_p0_master1200.jpg"
        resp=requests.get(_url,stream=True)
        if resp.status_code==200:
            cursor.execute("UPDATE illusts SET url_foruse=%s WHERE id=%s",(_url,ill[0]))
            conn.commit()
        else:
            cursor.execute("UPDATE illusts SET url_foruse=%s WHERE id=%s",("None",ill[0]))
            conn.commit()
```
&emsp;&emsp;At that time we havn't learnt much about **html** and **js** and didn't known about ```onerror``` of ```<img></img>```. If I'd know that, we wouldn't run a program that is such time consuming.
```html
<script>
    function imgerrorfun(x){
        var img=event.srcElement;
        img.src=x;
        img.onerror=function(){
            event.srcElement.parentNode.parentNode.parentNode.remove();
        };
    }
</script>
...
<div ...>
    <div ...>
        <div ...>
            <img src="source_1.png" onerror='imgerrorfun("source_2.png")'/>
        </div>
    </div>
</div>
```
&emsp;&emsp;By doing things like this, when ```source_1.png``` is not valid, the ```src``` would be changed to ```source_2.png```, and when ```source_2.png``` is still not valid, the whole **div** that contains this img would be removed. Thus, the webpage will have no broken image be shown.


### The Tags Page
#### Picture Part
&emsp;&emsp;Since our goal is to build a website that shows pisture, it is very important to find a good way to show others the illusts. The **Masonry Layouts** comes to our mind.  
&emsp;&emsp;The **Masonry Layouts** form is to place pictures on the page in many cols with the same width but the height is different. Probably like this:
![](img/xjq_3.png)
&emsp;&emsp;However, because of the size of the img we could get, it might be a little bit large to show so many pictures on one page. So we would just show two cols. Like this:
![](img/xjq_4.png)
&emsp;&emsp;Here's some details about the page.  
&emsp;&emsp;To keep the order of the pictures, we could not just do it with **css**, instead, we would have to do it with **js** and **css**.   
&emsp;&emsp;First of all, constrain the width of the img with **css**. Next, define the ```checkFlag``` function to reset the pictures when the ```document``` is ```onload```. In this function, I'd have to compute the num of pictures of each column. Also, we had to reset the height of container to display the pictures seperately.   
&emsp;&emsp;After doing this, the pictures is already in the form of **Masonry Layouts**. However, the num of the pictures is fixed. What we want is the type of Masonry Layouts that is endless. That would pour more and more pictures when the user scroll to the bottom of the page. In other word, the pictures must be loaded asynchronously. We have no idea about this so we would learn it from the beginning.  
&emsp;&emsp;At that time didn't know **js** well. And the first idea that comes to real is using **Ajax**, the **requests** of **js**. Here's the basic code.  
```JavaScript
var xmlhttp;
if (window.XMLHttpRequest){
    xmlhttp=new XMLHttpRequest();
}
else{
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}
xmlhttp.onreadystatechange=function(){
    if (xmlhttp.readyState==4 &&xmlhttp.status==200){
        imgData.data=eval(xmlhttp.responseText);
    }
}
xmlhttp.open("GET","/a?t="+ Math.random(),true);
xmlhttp.send();
```
&emsp;&emsp;This is used to get the infomation of the imgs to be added to the page. However, the images we got was repeated. And we could not fix it. Out of no reason. But we came to realize that we didn't needed to do so. All we need is to write the ```innerHTML``` of the container in the proper time. And the infomation of the pictures could be included then the **HTML** is rendered. Using ```Flask.render_templates```. Just like this:
```js
var imgData={
    "data":[
      {% for flask_ in flask_datas %}
        {"src":"{[flask_[1]]}","id":"{[flask_[0]]}","tsrc":"{[flask_[2]]}"},
      {% endfor %}
    ]
}
```
&emsp;&emsp;This woudn't cost much memery, since even a single picture is a lot larger than some simple text. So the problem comes to **when to write**.  
&emsp;&emsp;The answer is the time you scroll to the bottom of the page. So we defined a function named ```check_bottom``` , whitch computes the position of the scrollbar and add picture to the page.
```js
function check_bottom(){
    if((document.body.scrollTop+document.body.clientHeight-document.body.scrollHeight>-document.body.clientHeight/2)&&(document.getElementById("container").lastChild.firstChild.firstChild.firstChild.complete)){
        var cparent=document.getElementById("container");
        for(var i=0;(i<2)&&(gonelen<imgData.data.length);i++,gonelen++){
            if((imgData.data[gonelen].src!="None"))cparent.innerHTML+="<a href='/illust?id="+imgData.data[gonelen].id+"'><div class='box'><div class='box_img'><img src='"+imgData.data[gonelen].tsrc+"' onerror='imgerrorfun(\""+imgData.data[gonelen].src+"\")'/></div></div></a>";
        }
    }
}
```
&emsp;&emsp;Also, the function is used repeatly. So we need to ```var clo2=self.setInterval('check_bottom()',500);``` to call it each 500ms.  
&emsp;&emsp;Then comes the problem that the newly added picture is not well located. My solution is to call ```check_bottom``` every 500ms too.   
&emsp;&emsp;Now the pictures could be shown nicely.
#### Tags Part
&emsp;&emsp;The item that inspired us about this part is the output of the search part of **bilibili**.   
![](img/xjq_5.png)
<center><img src="img/xjq_6.png" height=200px></img></center>

&emsp;&emsp;By then we thought I've got some idea about **js**, so we decided to write it with pure **js**.  
&emsp;&emsp;Listing all of the tags is terrible, so the tags here will only contains tags that be used more than 50 times.   
&emsp;&emsp;You will find that the cyua buttons could change it's color if you click it. That means the tags be included or forbidden when you click the "确定" button.   
&emsp;&emsp;When it's cyua, it's neither selected nor forbidden. When it's lime, it's selected. When it's gray, it's forbidden.  
```js
tags_set=new Set([{% for i in _the_tags%}"{[i]}",{% endfor %}]);
ftags_set=new Set([{% for i in _the_ftags%}"{[i]}",{% endfor %}]);
function addtag(tag){
    if(tags_set.has(tag)){tags_set.delete(tag);document.getElementById(tag).style["background-color"]="gray";ftags_set.add(tag);}
    else if(ftags_set.has(tag)){ftags_set.delete(tag);document.getElementById(tag).style["background-color"]="cyan"}
    else{tags_set.add(tag);document.getElementById(tag).style["background-color"]="lime";}
}
...
...
    {% for tag in tags%}<div class="tag_sel" onclick="addtag('{[tag]}');" id="{[tag]}">{[tag]}</div>{% endfor %}
...
```
&emsp;&emsp;```tags_set``` contains all lime tags, which means selected. ```ftags_set``` contains all gray tags, which means forbidden.  
&emsp;&emsp;And here's the relation between output and two types of tags:
$$output=\bigcap_{i=1}^n tags\_set-\bigcup_{i=1}^m ftags\_set$$
(Ps:The R-18 tags is forbidden by default)  
&emsp;&emsp;This is done with python at the server:
```python
tags=request.args.get("tags","").strip()
ftags=request.args.get("ftags","").strip()
_tags=[]
_ftags=[]
if not "R-18" in tags and not "R-18" in ftags:
    ftags+=",R-18"
if tags:
    candi=set()
    flag=False
    for i in tags.split(','):
        i=i.strip()
        if i:
            _tags.append(i)
            if flag:
                candi=candi&d_top_tags[i]
            else:
                candi=d_top_tags[i].copy()
                flag=True
else:
    candi=d_id.copy()
if ftags:
    for i in ftags.split(','):
        i=i.strip()
        if i:
            _ftags.append(i)
            candi=candi-d_top_tags[i]
ret= [[i,d_url_foruse[i],func(d_url_foruse[i],i)] for i in candi]
```
&emsp;&emsp;By the way, the "确定" button is obtained without using ```<form>```, instead, it uses ```window.location.href="...";``` like this:
```js
function redire(){
    var _tags='';
    var _ftags='';
    for(i of tags_set)_tags+=i+',';
    for(i of ftags_set)_ftags+=i+',';
    window.location.href="tags?tags="+_tags+"&ftags="+_ftags;
}
```
### The Map Page
#### Zoom of Map
&emsp;&emsp;We copied the code from [svg-pan-zoom](https://github.com/bumbu/svg-pan-zoom), so there's nothing much to talk about.  
&emsp;&emsp;Also, we noticed that some pages of acemap seems also used the same zoomimg method.
|svg-pan-zoom|CCFConfCompare|
|:-:|:-:|
|![](img/xjq_7.png)|![](img/xjq_8.png)|
#### Show of Map
&emsp;&emsp;Because of the relations of the illustors is too complicated and many of them are followed and are following too many people. The edges of the graph is just too much. And will be hard to zoom or drag or find anything useful. My solution to this problem is to hide all the edges and only show edges that are related to the node selected.  
&emsp;&emsp;Thanks to the form of the output of **gephi**, each nodes has it's **id** and each nodes has it's targets in it's ```class```.
```html
<path class="id_10292 id_3079252" d="M -151.112381,530.487549 L -314.106415,-545.153503" fill="none" stroke="#b29b6c" stroke-opacity="0.4" stroke-width="1.0" style="display:none;"></path>
...
<circle class="id_2074388" cx="686.12494" cy="-1027.0114" fill="#00c7ff" fill-opacity="1.0" r="7.6373625" stroke="#000000" stroke-opacity="1.0" stroke-width="1.0"></circle>
```
&emsp;&emsp;So we could select out the edges and nodes easily using ```querySelector```.
```js
var masks = document.getElementById("node-labels").querySelectorAll("text");
var masks2 = document.getElementById("nodes").querySelectorAl("circle");
var masks3 = document.getElementById("node-labels-outline")querySelectorAll("text");
var idnow="_";
masks.forEach(function (elem){
    elem.style.cursor="pointer";
    elem.onmouseover=function(){
        if(idnow=="_"){
            masks2.forEach(function(_){
                if(_.attributes.class.nodeValue!=elem.attributes.class.nodeValue)
                _.style.display="none";
            })
            masks.forEach(function(_){
                if(_.attributes.class.nodeValue!=elem.attributes.class.nodeValue)
                _.style.display="none";
            })
            masks3.forEach(function(_){
                if(_.attributes.class.nodeValue!=elem.attributes.class.nodeValue)
                _.style.display="none";
            })
            Array.from(document.getElementById("edges").getElementsByClassName(elem.attributes.class.nodeValue)).forEach(function (line){
                if(line.classList[0]==elem.attributes.class.nodeValue){
                    document.getElementById("nodes").getElementsByClassName(line.classList[1])[0].style.display="block";
                    document.getElementById("node-labels").getElementsByClassName(line.classList[1])[0].style.display="block";
                    document.getElementById("node-labels-outline").getElementsByClassName(line.classList[1])[0].style.display="block";
                    line.style.display="block";
                }
            });
        }
    }
    elem.onmouseout=function(){
        if(idnow=="_"){
            masks2.forEach(function(_){
                _.style.display="block";
            })
            masks.forEach(function(_){
                _.style.display="block";
            })
            masks3.forEach(function(_){
                _.style.display="block";
            })
            Array.from(document.getElementById("edges").getElementsByClassName(elem.attributes.class.nodeValue)).forEach(function (line){
                line.style.display="none";
            });
        }
    }
    elem.onclick=function(){
        if(idnow=="_"){
            idnow=elem.attributes.class.nodeValue;
            masks2.forEach(function(_){
                if(_.attributes.class.nodeValue!=elem.attributes.class.nodeValue)
                _.style.display="none";
            })
            masks.forEach(function(_){
                if(_.attributes.class.nodeValue!=elem.attributes.class.nodeValue)
                _.style.display="none";
            })
            masks3.forEach(function(_){
                if(_.attributes.class.nodeValue!=elem.attributes.class.nodeValue)
                _.style.display="none";
            })
            Array.from(document.getElementById("edges").getElementsByClassName(elem.attributes.class.nodeValue)).forEach(function (line){
                if(line.classList[0]==elem.attributes.class.nodeValue){
                    document.getElementById("nodes").getElementsByClassName(line.classList[1])[0].style.display="block";
                    document.getElementById("node-labels").getElementsByClassName(line.classList[1])[0].style.display="block";
                    document.getElementById("node-labels-outline").getElementsByClassName(line.classList[1])[0].style.display="block";
                    line.style.display="block";
                }
            });
        }
        else if(idnow==elem.attributes.class.nodeValue){
            idnow="_";
            masks2.forEach(function(_){
                _.style.display="block";
            })
            masks.forEach(function(_){
                _.style.display="block";
            })
            masks3.forEach(function(_){
                _.style.display="block";
            })
            Array.from(document.getElementById("edges").getElementsByClassName(elem.attributes.class.nodeValue)).forEach(function (line){
                line.style.display="none";
            });
        }
        else{
            masks2.forEach(function(_){
                _.style.display="block";
            })
            masks.forEach(function(_){
                _.style.display="block";
            })
            masks3.forEach(function(_){
                _.style.display="block";
            })
            Array.from(document.getElementById("edges").getElementsByClassName(idnow)).forEach(function (line){
                line.style.display="none";
            });
            idnow=elem.attributes.class.nodeValue;
            masks2.forEach(function(_){
                if(_.attributes.class.nodeValue!=elem.attributes.class.nodeValue)
                _.style.display="none";
            })
            masks.forEach(function(_){
                if(_.attributes.class.nodeValue!=elem.attributes.class.nodeValue)
                _.style.display="none";
            })
            masks3.forEach(function(_){
                if(_.attributes.class.nodeValue!=elem.attributes.class.nodeValue)
                _.style.display="none";
            })
            Array.from(document.getElementById("edges").getElementsByClassName(elem.attributes.class.nodeValue)).forEach(function (line){
                if(line.classList[0]==elem.attributes.class.nodeValue){
                    document.getElementById("nodes").getElementsByClassName(line.classList[1])[0].style.display="block";
                    document.getElementById("node-labels").getElementsByClassName(line.classList[1])[0].style.display="block";
                    document.getElementById("node-labels-outline").getElementsByClassName(line.classList[1])[0].style.display="block";
                    line.style.display="block";
                }
            });
        }
    }
})
```
***
## Team cooperation
### Source Code Management
&emsp;&emsp;We managed our code with git and a GUI tool: source tree. So far, there are 72 commits, and every group member has made commit to the repository.   
<img src="img/git.png"></img>

### Database
&emsp;&emsp;We put our data on the cloud server of Alilibaba, so every member has access to the latest data.
***
## Future work
### Illustration Feature
&emsp;&emsp;The hash function used on illustrators doesn't discriminate illustrations well.  
<img src="img/illust_hash.png"></img>  
&emsp;&emsp;Current features are all based on illustration tags, rather than illustration itself. So next step, we can apply computer vision method, 
such as ResNet or AlexNet.

### Make it More Interactive
&emsp;&emsp;Most of the page is just representing the data or image, And make it a little bit boring.  
&emsp;&emsp;Some Interactive elements can be add to attract visitors.
### Handle Synonymous Tags
&emsp;&emsp;There are many synonymous tags in our data. However, the PCA algorithm can't tell if two tags hane the same meaning. For example, following four tags all refer to the same character.  
<img src="img/synonymous_tags.png"></img>
&emsp;&emsp;NLP method should be applied to find these tags of similar meanings. For example, GloVe can construct coexistence matrix, thus find the words that most likely to have the same meaning.  
<img src="img/glove.png"></img>
***
## Duty
- Data and crawler: 黄川懿，薛家奇，黄浩栩
- Search engine: 黄浩栩
- Visualization: 王鹏飞，向天乐，薛家奇
- Website: 黄川懿，向天乐，薛家奇，黄浩栩

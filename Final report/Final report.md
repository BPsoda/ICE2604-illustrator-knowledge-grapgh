> 说明：请将自己负责书写的内容写到对应的二级标题下。把改进的想法写到 future work 标题以下。如需插入图片，请放在`./img/`路径下。  
> Markdown 的语法可以参考 https://markdown.com.cn/basic-syntax/ 。相信在30分钟内你就可以掌握。  
> 如果你尚没有编辑过markdown，我建议你使用`vscode`+`markdown all in one` 插件编辑
# Make Illustrators Relationship Visible: Final Report of ICE2604 Group 2
<img src="img/logo.png"></img>
[toc]
## Project Design
There are numerous awesome illustrators and delicate illustrations on the internet.But have you ever thought how they are related to each other?  
Our project aims to find and visualizing the relationship between each illustrator and illustration, by the means of **illustrator map** and **illustration ranking & trending**.  
### Illustrator map
By static the tags of one illustrator's works and turn it to a vector, we can represent the style of an author as a vector. Plotting it one a graph and add following relationship as edges, we get the illustrator map.  
<img src="img/word2vec.png"></img>
### Ranking & Trending
By analyze the create date, tags and bookmarks of illustration, we can point out the trending and make predictions.
<img src="img/trending.png"></img>
***
## Our work
***
## Data and Crawler
### Crawler  
#### Website analysis
The data source of our project is pixiv.net, an online community of artist.  
The data we want include:  
- The basic information of a illustrator
- The following illustrators of one illustrator
- The recent works of illustrators
- The tags of an illustrator
- The basic information of an illustration
- The tags of an illustation

After looking into the XHR of the website, we find these information in two responses:   
- `https://www.pixiv.net/ajax/user/{userId}/illusts/tags?lang=zh`
- `https://www.pixiv.net/ajax/user/{userId}/following?offset={}&limit={}&rest=show&tag=&lang=zh`

The content looks like this:  
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
We makes requests with the python module `requests`. Consider the anti reptile measures, we alse applied `clash` as the agent pool.  
The pixiv has relatively loose anti reptile measures. It only checks `referrence` and `Cookie`.  
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
After finishing one illustrator, we want the cawler to retieve information of other illustrators as well. This can be realized by crawling the following of the current illustrator.  
The following relationship constructs a directed graph of illustrators. If we traverse the net, we can get all the information we want. So, we search the net with BFS.  
```python
visited = {}
visitingQueque = queue.Queue()

while(len(visited) < 10000):
    visitingId = visitingQueque.get()
    while (visitingId in visited) : 
        visitingId = visitingQueque.get()
    response = makeRequest(visitingId)
```

#### Multi-threading
Consider the network I/O takes up most of the time, it is necessary to apply multithreading. In this case, we spawned 4 threads.  
The `visitingQueue` can serve as the scheduler of the threads.  

### Data Sifting
&emsp;&emsp;&emsp;&emsp;To start with, what we had was the raw infomation we clawled from the Pixiv website in the form of **.json**. Which was heavily repeated and took up about 15GB memories after unzipped. 
&emsp;&emsp;&emsp;&emsp;The smallest one of them is like like this:
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
&emsp;&emsp;&emsp;&emsp;The useful part of infomation is in ```json.load(f)["body"]["users"]```, and it's empty here, which means this user whose **userId** is ```"12138318"``` doesn't follow any other users. That's also the reason this file is the smallest.
&emsp;&emsp;&emsp;&emsp;In the list of ```json.load(f)["body"]["users"]``` are all of the users that this user is following. And all I need to do is collect their userIds because **userId** can convey the infomation between them.
&emsp;&emsp;&emsp;&emsp;However, there's one problem. Fisrt, we have no infomation about users themselves. If I colloct only the **userId**, all we would got is some numbers. And there's no more infomation about the user himself in his own json file. So I need to get the infomation from other users that are following this user. Doing this has a risk that if one user isn't being followed by other user then hinself would have no detailed infomation. We won't even know his userName. 
&emsp;&emsp;&emsp;&emsp;Luckily, we could prove that every user in the dir has someone following him except one because Huang haoxv collected them using DFS method and all of the users we saved must has someone following him except the first user chosen to be the start node.
&emsp;&emsp;&emsp;&emsp;A single elem in ```json.load(f)["body"]["users"]``` would be like this:
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
&emsp;&emsp;&emsp;&emsp;It's cozy that there're four illusts in ```json.load(f)["body"]["users"]["illusts"]```. As you could see, the infomation we could collect contains:

- userId
- userName
- userComment
- profileImageUrl
- illusts
- createDate

&emsp;&emsp;&emsp;&emsp;And with the following relation we got, I made two tables in MySQL like this:
|Users|illusts|
|:-:|:-:|
|![](./img/xjq_1.png)|![](./img/xjq_2.png)|
&emsp;&emsp;&emsp;&emsp;Here's the code that fill in the table:
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
&emsp;&emsp;&emsp;&emsp;Also, I used ```tqdm``` to add a process bar to visualize the procedure of the program.
***
## Search Engine
The search engine is based on Elastic Search. We aim to search illustrators and illustrations by id, name, tag.  
Because we want the exact id, so the id is `keyword` type. The name/title and tags are text type.  
Since the name, title and tags contain Chinese and Japanese, we tokenize them with an plugin `analysis-icu`.  
```python
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
```
***
## Visualization
***
## Website
### Valid Picture 
&emsp;&emsp;&emsp;&emsp;We already have the **url** of each image. However, the **url** is not only forbidden here but also could not request directly because their anti-crawler methods. At first, we thought of save all of the pictures to loacl. But after computing the approximate sizeof the images, we decided to give up. Not only because It's too large to store, but also because we could not use **wifi** and the cost is too high.
&emsp;&emsp;&emsp;&emsp;Suddenly, we thought of getting the image from other source. I found a mirror website of Pixiv and found that the **url** of this website is kind of similar to Pixiv. What we would have to do is converting ```"https://i.pximg.net/c/250x250_80_a2/img-master/img/2010/09/22/00/19/05/13399152_p0_square1200.jpg"``` to ```https://proxy.pixivel.moe/img-original/img/2010/09/22/00/19/05/13399152_p0.jpg``` or ```https://proxy-jp1.pixivel.moe/c/600x1200_90/img-master/img/2010/09/22/00/19/05/13399152_p0_master1200.jpg```. 
&emsp;&emsp;&emsp;&emsp;Here comes the problem that this mirror website is not good enough to provide all images we needed. In other word, some of the **url** is not valid. 
&emsp;&emsp;&emsp;&emsp;To avoid our website from showing a lot of broken images, we need to check all the urls. Which is quite time consuming. Here's the code:
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
&emsp;&emsp;&emsp;&emsp;This took me about a whole day. And I'd have to run another. (```url_foruse``` is a newly added col which stores the **url** that could be requestd directly)
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
&emsp;&emsp;&emsp;&emsp;At that time I havn't learnt much about **html** and **js** and didn't known about ```onerror``` of ```<img></img>```. If I'd know that, I wouldn't run a program that is such time consuming.
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
&emsp;&emsp;&emsp;&emsp;By doing things like this, when ```source_1.png``` is not valid, the ```src``` would be changed to ```source_2.png```, and when ```source_2.png``` is still not valid, the whole **div** that contains this img would be removed. Thus, the webpage will have no broken image be shown.
***
### The Tags Page
#### Picture Part
&emsp;&emsp;&emsp;&emsp;Since our goal is to build a website that shows pisture, it is very important to find a good way to show others the illusts. The **Waterfall** form comes to my mind.
&emsp;&emsp;&emsp;&emsp;The **Waterfall** form is to place pictures on the page in many cols with the same width but the height is different. Probably like this:
![](img/xjq_3.png)
&emsp;&emsp;&emsp;&emsp;However, because of the size of the img we could get, it might be a little bit large to show so many pictures on one page. So we would just show two cols. Like this:
![](img/xjq_4.png)
&emsp;&emsp;&emsp;&emsp;Here's some details about the page.
&emsp;&emsp;&emsp;&emsp;To keep the order of the pictures, I could not just do it with **css**, instead, I would have to do it with **js** and **css**. 
&emsp;&emsp;&emsp;&emsp;First of all, constrain the width of the img with **css**. Next, define the ```checkFlag``` function to reset the pictures when the ```document``` is ```onload```. In this function, I'd have to compute the num of pictures of each column. Also, I had to reset the height of container to display the pictures seperately. 
&emsp;&emsp;&emsp;&emsp;After doing this, the pictures is already in the form of **Waterfall**. However, the num of the pictures is fixed. What we want is the type of Waterfall that is endless. That would pour more and more pictures when the user scroll to the bottom of the page. In other word, the pictures must be loaded asynchronously. I have no idea about this so I would learn it from the beginning.
&emsp;&emsp;&emsp;&emsp;At that time didn't know **js** well. And the first idea that comes to real is using **Ajax**, the **requests** of **js**. Here's the basic code.
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
&emsp;&emsp;&emsp;&emsp;This is used to get the infomation of the imgs to be added to the page. However, the images I got was repeated. And I could not fix it. Out of no reason. But I came to realize that I didn't needed to do so. All I need is to write the ```innerHTML``` of the container in the proper time. And the infomation of the pictures could be included then the **HTML** is rendered. Using ```Flask.render_templates```. Just like this:
```js
var imgData={
    "data":[
      {% for flask_ in flask_datas %}
        {"src":"{[flask_[1]]}","id":"{[flask_[0]]}","tsrc":"{[flask_[2]]}"},
      {% endfor %}
    ]
}
```
&emsp;&emsp;&emsp;&emsp;This woudn't cost much memery, since even a single picture is a lot larger than some simple text. So the problem comes to **when to write**.
&emsp;&emsp;&emsp;&emsp;The answer is the time you scroll to the bottom of the page. So I defined a function named ```check_bottom``` , whitch computes the position of the scrollbar and add picture to the page.
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
&emsp;&emsp;&emsp;&emsp;Also, the function is used repeatly. So I need to ```var clo2=self.setInterval('check_bottom()',500);``` to call it each 500ms.
&emsp;&emsp;&emsp;&emsp;Then comes the problem that the newly added picture is not well located. My solution is to call ```check_bottom``` every 500ms too. 
&emsp;&emsp;&emsp;&emsp;Now the pictures could be shown nicely.
#### Tags Part
&emsp;&emsp;&emsp;&emsp;The item that inspired me about this part is the output of the search part of **bilibili**. 
![](img/xjq_5.png)
<center><img src="img/xjq_6.png" height=200px></img></center>

&emsp;&emsp;&emsp;&emsp;By then I thought I've got some idea about **js**, so I decided to write it with pure **js**.
&emsp;&emsp;&emsp;&emsp;Listing all of the tags is terrible, so the tags here will only contains tags that be used more than 50 times. 
&emsp;&emsp;&emsp;&emsp;You will find that the cyua buttons could change it's color if you click it. That means the tags be included or forbidden when you click the "确定" button. 
&emsp;&emsp;&emsp;&emsp;When it's cyua, it's neither selected nor forbidden. When it's lime, it's selected. When it's gray, it's forbidden.
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
&emsp;&emsp;&emsp;&emsp;```tags_set``` contains all lime tags, which means selected. ```ftags_set``` contains all gray tags, which means forbidden.
&emsp;&emsp;&emsp;&emsp;And here's the relation between output and two types of tags:
$$output=\bigcap_{i=1}^n tags\_set-\bigcup_{i=1}^m ftags\_set$$
(Ps:The R-18 tags is forbidden by default)
&emsp;&emsp;&emsp;&emsp;This is done with python at the server:
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
&emsp;&emsp;&emsp;&emsp;By the way, the "确定" button is obtained without using ```<form>```, instead, it uses ```window.location.href="...";``` like this:
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
&emsp;&emsp;&emsp;&emsp;I copied the code from [svg-pan-zoom](https://github.com/bumbu/svg-pan-zoom), so there's nothing much to talk about.
&emsp;&emsp;&emsp;&emsp;Also, I noticed that some pages of acemap seems also used the same zoomimg method.
|svg-pan-zoom|CCFConfCompare|
|:-:|:-:|
|![](img/xjq_7.png)|![](img/xjq_8.png)|
#### Show of Map
&emsp;&emsp;&emsp;&emsp;Because of the relations of the illustors is too complicated and many of them are followed and are following too many people. The edges of the graph is just too much. And will be hard to zoom or drag or find anything useful. My solution to this problem is to hide all the edges and only show edges that are related to the node selected.
&emsp;&emsp;&emsp;&emsp;Thanks to the form of the output of **gephi**, each nodes has it's **id** and each nodes has it's targets in it's ```class```.
```html
<path class="id_10292 id_3079252" d="M -151.112381,530.487549 L -314.106415,-545.153503" fill="none" stroke="#b29b6c" stroke-opacity="0.4" stroke-width="1.0" style="display:none;"></path>
...
<circle class="id_2074388" cx="686.12494" cy="-1027.0114" fill="#00c7ff" fill-opacity="1.0" r="7.6373625" stroke="#000000" stroke-opacity="1.0" stroke-width="1.0"></circle>
```
&emsp;&emsp;&emsp;&emsp;So I could select out the edges and nodes easily using ```querySelector```.
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
## Team cooperation
### Source Code Management
We managed our code with git and a GUI tool: source tree. So far, there are 72 commits, and every group member has made commit to the repository.   
<img src="img/git.png"></img>

### Database
We put our data on the cloud server of Alilibaba, so every member has access to the latest data.
## Future work
### Illustration Feature
The hash function used on illustrators doesn't discriminate illustrations well.  
<img src="img/illust_hash.png"></img>  
Current features are all based on illustration tags, rather than illustration itself. So next step, we can apply computer vision method, 
such as ResNet or AlexNet.

### Handle Synonymous Tags
There are many synonymous tags in our data. However, the PCA algorithm can't tell if two tags hane the same meaning. For example, following four tags all refer to the same character.  
<img src="img/synonymous_tags.png"></img>
NLP method should be applied to find these tags of similar meanings. For example, GloVe can construct coexistence matrix, thus find the words that most likely to have the same meaning.  
<img src="img/glove.png"></img>
***
## Duty
- Data and crawler: 黄川懿，薛家奇，黄浩栩
- Search engine: 黄浩栩
- Visualization: 王鹏飞，向天乐，薛家奇
- Website: 黄川懿，向天乐，薛家奇，黄浩栩

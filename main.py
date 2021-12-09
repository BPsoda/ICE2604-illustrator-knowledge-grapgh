from flask import Flask,render_template,request,redirect,url_for
import pymysql
import json
import requests
import json,random
import searcher
import shelve
global result
the_tags="""[('オリジナル', 4306)
('女の子', 2990)
('R-18', 2872)
('おっぱい', 1184)
('Fate/GrandOrder', 896)
('魅惑の谷間', 769)
('巨乳', 753)
('尻神様', 748)
('極上の乳', 707)
('原神', 693)
('FGO', 661)
('オリジナル10000users入り', 598)
('アズールレーン', 518)
('水着', 503)
('オリジナル1000users入り', 493)
('バーチャルYouTuber', 464)
('仕事絵', 457)
('アークナイツ', 457)
('少女', 445)
('裸足', 440)
('漫画', 435)
('明日方舟', 435)
('VOCALOID', 430)
('初音ミク', 424)
('創作', 378)
('ホロライブ', 366)
('魅惑のふともも', 352)
('艦これ', 350)
('東方', 325)
('ウマ娘プリティーダービー', 324)
('足裏', 311)
('ぱんつ', 307)
('マニキュア', 305)
('風景', 303)
('腋', 302)
('バニーガール', 301)
('Fate/GO1000users入り', 295)
('ブルーアーカイブ', 281)
('爆乳', 271)
('オリジナル5000users入り', 270)
('原创', 256)
('黒タイツ', 254)
('着衣巨乳', 238)
('艦隊これくしょん', 232)
('黒スト', 229)
('背景', 223)
('制服', 223)
('GenshinImpact', 220)
('足指', 217)
('オリジナル3000users入り', 216)
('本家', 214)
('オリジナル7500users入り', 204)
('セーラー服', 203)
('ウマ娘', 203)
('アイドルマスターシンデレラガールズ', 202)
('おへそ', 196)
('Arknights', 196)
('落書き', 194)
('百合', 192)
('バーチャルYouTuber1000users入り', 192)
('VTuber', 189)
('アイドルマスターシャイニーカラーズ', 188)
('女子高生', 174)
('メイド', 174)
('ハロウィン', 169)
('アズールレーン1000users入り', 169)
('猫耳', 167)
('東方Project', 164)
('陰毛', 161)
('魅惑の顔', 159)
('ふつくしい', 154)
('VOCALOID1000users入り', 154)
('アイマス1000users入り', 150)
('艦これ1000users入り', 146)
('下着', 146)
('ソックス足裏', 146)
('少女前線', 145)
('プリンセスコネクト!Re:Dive', 145)
('ドールズフロントライン', 144)
('これはいい初音', 142)
('うごイラ', 139)
('アズールレーン10000users入り', 136)
('ウマ娘プリティーダービー1000users入り', 136)
('中出し', 134)
('Fate/GO5000users入り', 132)
('一之瀬アスナ', 132)
('ツインテール', 128)
('碧蓝航线', 122)
('JK', 120)
('グランブルーファンタジー', 119)
('狐耳', 118)
('Fate/GO10000users入り', 118)
('アズールレーン5000users入り', 117)
('オリジナル30000users入り', 115)
('ロリ', 115)
('ファンタジー', 113)
('にじさんじ', 113)
('船上のバニーチェイサー', 111)
('東方Project1000users入り', 110)
('美脚', 109)
('原神10000users入り', 109)
('ミクさんマジ女神', 107)
('ブルアカ', 107)
('お尻', 105)
('褐色', 102)
('少女前线', 102)
('黒髪', 101)
('Fate', 101)
('男の子', 101)
('揉みしだきたい乳', 101)
('雷電将軍', 101)
('眼鏡', 98)
('原創', 98)
('パイズリ', 97)
('裸足裏', 97)
('むちむち', 96)
('ミクさんマジ天使', 94)
('アイマス5000users入り', 92)
('ショートパンツ', 90)
('お品書き', 90)
('高品質パンツ', 90)
('長手袋', 89)
('C97', 88)
('イラスト', 87)
('アークナイツ1000users入り', 87)
('極上の女体', 86)
('獣耳', 86)
('Vtuber', 86)
('抱き枕', 83)
('黒髪ロング', 83)
('HololiveEN', 82)
('白髪', 81)
('美少女', 81)
('ブルーアーカイブ1000users入り', 81)
('ポケモン', 80)
('CLIPSTUDIOPAINT', 80)
('ラブライブ!', 80)
('同人', 79)
('原神1000users入り', 79)
('オリジナル500users入り', 78)
('剥ぎ取りたいブラ', 78)
('白タイツ', 78)
('水中', 77)
('おねショタ', 77)
('拘束', 77)
('バーチャルYouTuber10000users入り', 77)
('hololive', 77)
('剥ぎ取りたいパンツ', 76)
('VOCALOID100users入り', 75)
('ビキニ', 74)
('母乳', 73)
('原神5000users入り', 73)
('金髪', 71)
('着物', 70)
('甘雨(原神)', 70)
('插画', 69)
('尻', 69)
('へそ', 69)
('プリコネR', 69)
('エルフ', 68)
('NTR', 68)
('3DCG', 67)
('バーチャルYouTuber5000users入り', 67)
('鬼滅の刃', 67)
('ロリ巨乳', 66)
('タイツ', 66)
('グラブル', 64)
('アナル', 63)
('仰臥', 63)
('濡れ透け', 63)
('銀髪', 63)
('ハイレグ', 62)
('パンツ', 62)
('マシュ・キリエライト', 61)
('アイマス10000users入り', 60)
('角楯カリン', 60)
('ポニーテール', 59)
('サイハイブーツ', 58)
('マイクロビキニ', 58)
('パンチラ', 58)
('スク水', 57)
('ラブライブ!1000users入り', 57)
('海', 57)
('手袋', 57)
('指を突っ込みたいへそ', 57)
('3D', 56)
('FF14', 56)
('目がハート', 55)
('胸ポチ', 55)
('VOCALOID500users入り', 54)
('シャニマス', 54)
('ライスシャワー(ウマ娘)', 54)
('たくしあげ', 53)
('宣伝', 53)
('圧倒的胸囲', 53)
('ストッキング', 53)
('うちの子', 53)
('C96', 53)
('猫', 52)
('男の娘', 52)
('ボブカット', 52)
('紐タイ', 52)
('アズレン', 52)
('横乳', 52)
('ウマ娘プリティーダービー5000users入り', 52)
('エロ衣装', 51)
('はいてない', 51)
('夏', 51)
('Re:ゼロから始める異世界生活', 51)
('マント', 50)
('輪チラ', 50)
('艦これ5000users入り', 50)
('練習', 50)
('抱き枕カバー', 50)
('original', 50)
('フェラ', 50)]""".split('\n')
the_tags=[i[0] for i in eval(",".join(the_tags))]
with shelve.open("data") as d:
    d_id=d["id"]
    d_title=d["title"]
    d_tags=d["tags"]
    d_top_tags=d["top_tags"]
    d_url_foruse=d["url_foruse"]

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

def func(x:str,the_id:str):
    if "master" in x:
        return x
    else:
        return "https://proxy.pixivel.moe/c/600x1200_90/img-master"+x[x.find("/img/"):x.find(the_id)+len(the_id)]+"_p0_master1200.jpg"

with open("2.json","rb") as f:
    b=json.load(f)
app=Flask(__name__)
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'
se = searcher.Searcher()
# print(json.dumps(result[0], indent=2, separators=(',', ';')))
@app.route('/home',methods=['GET','POST'])
def vue():
    global result
    return render_template('final_project1.html')
@app.route('/a')
def jsonpic():
    return json.dumps([urls for urls in random.sample(b["data"],20) if "master" in urls["src"]])
@app.route('/search',methods=['GET','POST'])
def search():
    global result
    if (request.form):
        key = request.form['getinfo']
        if(key.isdigit()):
            result = se.search(key, 'id')
        else:
            result = se.search(key, 'userName')
        print(result)
        return render_template('search.html',result=result)
    return render_template("search.html")
@app.route('/picture')
def showpicture():
    return render_template("showpic.html",initli=[urls["src"] for urls in random.sample(b["data"],20) if "master" in urls["src"]])
@app.route('/static')
def showstatic():
    return render_template("index.html",initli=[urls["src"] for urls in random.sample(b["data"],20) if "master" in urls["src"]])
@app.route('/tags')
def mainpage():
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
    ret= [[i,d_url_foruse[i],func(d_url_foruse[i],i)] for i in candi]# if "master" in d_url_foruse[i]
    return render_template("index2.html",flask_datas=ret,tags=the_tags,_the_tags=_tags,_the_ftags=_ftags)
@app.route("/illust")
def illust():
    the_id=request.args.get("id","13399152")
    return render_template("pic.html",url_foruse=func(d_url_foruse[the_id],the_id),title=d_title[the_id],tags=d_tags[the_id],ourl=d_url_foruse[the_id])

@app.route('/data', methods=['GET'])
def get_data():
    data={
    "categories":["巨乳","魅惑の谷間","Fate/GrandOrder","おっぱい" ,"女の子","オリジナル"],
    "data":[753,  769  ,896,1184,2990,4306]
    }
    return json.dumps(data)

@app.route('/illustrator')
def profile():
    user_id = request.args.get('id').strip()
    print(user_id)
    cursor.execute('SELECT * FROM Users WHERE userId={}'.format(user_id))
    profileInfo = cursor.fetchall()[0]
    userName = profileInfo[1]
    userComment = profileInfo[2]
    profile_image = profileInfo[3]
    illusts = profileInfo[4].rstrip().split(',')
    following_count = profileInfo[6]
    follower_count = profileInfo[8]
    bg = profileInfo[9]

    cursor.execute('SELECT * FROM illusts WHERE id in %s', (illusts,))
    illustInfo = cursor.fetchall()
    urls = list(i[7] for i in illustInfo)
    return render_template('user_profile.html', userName=userName, bg=bg, profile_image=profile_image, urls=urls, following_count=following_count, follower_count=follower_count, userComment=userComment)

    
app.run(host='0.0.0.0',debug=True)

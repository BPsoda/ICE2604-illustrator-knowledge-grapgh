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
        return render_template('search1.html',result=result)
    return render_template("search1.html")
@app.route('/picture')
def showpicture():
    return render_template("showpic.html",initli=[urls["src"] for urls in random.sample(b["data"],20) if "master" in urls["src"]])
@app.route('/static')
def showstatic():
    return render_template("Statics.html")
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

@app.route('/<userId>/tags.json')
def getUserTags(userId):
    cursor.execute('SELECT tags FROM Users WHERE userId=%s', userId)
    tagsdict = cursor.fetchone()[0]
    data = []
    tagsdict = eval('{' + tagsdict + '}')
    for tag, cnt in tagsdict.items():
        data.append({'name':tag, 'value':cnt})
    return json.dumps(data)

@app.route('/data', methods=['GET'])
def get_data():
    data={
    "categories":["巨乳","魅惑の谷間","Fate/GrandOrder","おっぱい" ,"女の子","オリジナル"],
    "data":[753,  769  ,896,1184,2990,4306],
    "word":[{"name": "オリジナル",   "value":  4306},
        {"name": "女の子",   "value":  2990},
        {"name": "おっぱい",   "value":  1184},
        {"name": "Fate/GrandOrder",   "value":  896},
        {"name": "魅惑の谷間",   "value":  769},
        {"name": "巨乳",   "value":  753},
        {"name": "尻神様",   "value":  748},
        {"name": "極上の乳",   "value":  707},
        {"name": "原神",   "value":  693},
        {"name": "FGO",   "value":  661},
        {"name": "オリジナル10000users入り",   "value":  598},
        {"name": "アズールレーン",   "value":  518},
        {"name": "水着",   "value":  503},
        {"name": "オリジナル1000users入り",   "value":  493},
        {"name": "バーチャルYouTuber",   "value":  464},
        {"name": "仕事絵",   "value":  457},
        {"name": "アークナイツ",   "value":  457},
        {"name": "少女",   "value":  445},
        {"name": "裸足",   "value":  440},
        {"name": "漫画",   "value":  435},
        {"name": "明日方舟",   "value":  435},
        {"name": "VOCALOID",   "value":  430},
        {"name": "初音ミク",   "value":  424},
        {"name": "創作",   "value":  378},
        {"name": "ホロライブ",   "value":  366},
        {"name": "魅惑のふともも",   "value":  352},
        {"name": "艦これ",   "value":  350},
        {"name": "東方",   "value":  325},
        {"name": "ウマ娘プリティーダービー",   "value":  324},
        {"name": "足裏",   "value":  311},
        {"name": "ぱんつ",   "value":  307},
        {"name": "マニキュア",   "value":  305},
        {"name": "風景",   "value":  303},
        {"name": "腋",   "value":  302},
        {"name": "バニーガール",   "value":  301},
        {"name": "Fate/GO1000users入り",   "value":  295},
        {"name": "ブルーアーカイブ",   "value":  281},
        {"name": "爆乳",   "value":  271},
        {"name": "オリジナル5000users入り",   "value":  270},
        {"name": "原创",   "value":  256},
        {"name": "黒タイツ",   "value":  254},
        {"name": "着衣巨乳",   "value":  238},
        {"name": "艦隊これくしょん",   "value":  232},
        {"name": "黒スト",   "value":  229},
        {"name": "背景",   "value":  223},
        {"name": "制服",   "value":  223},
        {"name": "GenshinImpact",   "value":  220},
        {"name": "足指",   "value":  217},
        {"name": "オリジナル3000users入り",   "value":  216},
        {"name": "本家",   "value":  214},
        {"name": "オリジナル7500users入り",   "value":  204},
        {"name": "セーラー服",   "value":  203},
        {"name": "ウマ娘",   "value":  203},
        {"name": "アイドルマスターシンデレラガールズ",   "value":  202},
        {"name": "おへそ",   "value":  196},
        {"name": "Arknights",   "value":  196},
        {"name": "落書き",   "value":  194},
        {"name": "百合",   "value":  192},
        {"name": "バーチャルYouTuber1000users入り",   "value":  192},
        {"name": "VTuber",   "value":  189},
        {"name": "アイドルマスターシャイニーカラーズ",   "value":  188},
        {"name": "女子高生",   "value":  174},
        {"name": "メイド",   "value":  174},
        {"name": "ハロウィン",   "value":  169},
        {"name": "アズールレーン1000users入り",   "value":  169},
        {"name": "猫耳",   "value":  167},
        {"name": "東方Project",   "value":  164},
        {"name": "陰毛",   "value":  161},
        {"name": "魅惑の顔",   "value":  159},
        {"name": "ふつくしい",   "value":  154},
        {"name": "VOCALOID1000users入り",   "value":  154},
        {"name": "アイマス1000users入り",   "value":  150},
        {"name": "艦これ1000users入り",   "value":  146},
        {"name": "下着",   "value":  146},
        {"name": "ソックス足裏",   "value":  146},
        {"name": "少女前線",   "value":  145},
        {"name": "プリンセスコネクト!Re:Dive",   "value":  145},
        {"name": "ドールズフロントライン",   "value":  144},
        {"name": "これはいい初音",   "value":  142},
        {"name": "うごイラ",   "value":  139},
        {"name": "アズールレーン10000users入り",   "value":  136},
        {"name": "ウマ娘プリティーダービー1000users入り",   "value":  136},
        {"name": "中出し",   "value":  134},
        {"name": "Fate/GO5000users入り",   "value":  132},
        {"name": "一之瀬アスナ",   "value":  132},
        {"name": "ツインテール",   "value":  128},
        {"name": "碧蓝航线",   "value":  122},
        {"name": "JK",   "value":  120},
        {"name": "グランブルーファンタジー",   "value":  119},
        {"name": "狐耳",   "value":  118},
        {"name": "Fate/GO10000users入り",   "value":  118},
        {"name": "アズールレーン5000users入り",   "value":  117},
        {"name": "オリジナル30000users入り",   "value":  115},
        {"name": "ロリ",   "value":  115},
        {"name": "ファンタジー",   "value":  113},
        {"name": "にじさんじ",   "value":  113},
        {"name": "船上のバニーチェイサー",   "value":  111},
        {"name": "東方Project1000users入り",   "value":  110},
        {"name": "美脚",   "value":  109},
        {"name": "原神10000users入り",   "value":  109},
        {"name": "ミクさんマジ女神",   "value":  107},
        {"name": "ブルアカ",   "value":  107},
        {"name": "お尻",   "value":  105},
        {"name": "褐色",   "value":  102},
        {"name": "少女前线",   "value":  102},
        {"name":"黒髪","value":101},
        {"name":"Fate","value":101},
        {"name":"男の子","value":101},
        {"name":"揉みしだきたい乳","value":101},
        {"name":"雷電将軍","value":101},
        {"name":"眼鏡","value":98},
        {"name":"原創","value":98},
        {"name":"パイズリ","value":97},
        {"name":"裸足裏","value":97},
        {"name":"むちむち","value":96},
        {"name":"ミクさんマジ天使","value":94},
        {"name":"アイマス5000users入り","value":92},
        {"name":"ショートパンツ","value":90},
        {"name":"お品書き","value":90},
        {"name":"高品質パンツ","value":90},
        {"name":"長手袋","value":89},
        {"name":"C97","value":88},
        {"name":"イラスト","value":87},
        {"name":"アークナイツ1000users入り","value":87},
        {"name":"極上の女体","value":86},
        {"name":"獣耳","value":86},
        {"name":"Vtuber","value":86},
        {"name":"抱き枕","value":83},
        {"name":"黒髪ロング","value":83},
        {"name":"HololiveEN","value":82},
        {"name":"白髪","value":81},
        {"name":"美少女","value":81},
        {"name":"ブルーアーカイブ1000users入り","value":81},
        {"name":"ポケモン","value":80},
        {"name":"CLIPSTUDIOPAINT","value":80},
        {"name":"ラブライブ!","value":80},
        {"name":"同人","value":79},
        {"name":"原神1000users入り","value":79},
        {"name":"オリジナル500users入り","value":78},
        {"name":"剥ぎ取りたいブラ","value":78},
        {"name":"白タイツ","value":78},
        {"name":"水中","value":77},
        {"name":"おねショタ","value":77},
        {"name":"拘束","value":77},
        {"name":"バーチャルYouTuber10000users入り","value":77},
        {"name":"hololive","value":77},
        {"name":"剥ぎ取りたいパンツ","value":76},
        {"name":"VOCALOID100users入り","value":75},
        {"name":"ビキニ","value":74},
        {"name":"母乳","value":73},
        {"name":"原神5000users入り","value":73},
        {"name":"金髪","value":71},
        {"name":"着物","value":70},
        {"name":"甘雨(原神},","value":70},
        {"name":"插画","value":69},
        {"name":"尻","value":69},
        {"name":"へそ","value":69},
        {"name":"プリコネR","value":69},
        {"name":"エルフ","value":68},
        {"name":"NTR","value":68},
        {"name":"3DCG","value":67},
        {"name":"バーチャルYouTuber5000users入り","value":67},
        {"name":"鬼滅の刃","value":67},
        {"name":"ロリ巨乳","value":66},
        {"name":"タイツ","value":66},
        {"name":"グラブル","value":64},
        {"name":"アナル","value":63},
        {"name":"仰臥","value":63},
        {"name":"濡れ透け","value":63},
        {"name":"銀髪","value":63},
        {"name":"ハイレグ","value":62},
        {"name":"パンツ","value":62},
        {"name":"マシュ・キリエライト","value":61},
        {"name":"アイマス10000users入り","value":60},
        {"name":"角楯カリン","value":60},
        {"name":"ポニーテール","value":59},
        {"name":"サイハイブーツ","value":58},
        {"name":"マイクロビキニ","value":58},
        {"name":"パンチラ","value":58},
        {"name":"スク水","value":57},
        {"name":"ラブライブ!1000users入り","value":57},
        {"name":"海","value":57},
        {"name":"手袋","value":57},
        {"name":"指を突っ込みたいへそ","value":57},
        {"name":"3D","value":56},
        {"name":"FF14","value":56},
        {"name":"目がハート","value":55},
        {"name":"胸ポチ","value":55},
        {"name":"VOCALOID500users入り","value":54},
        {"name":"シャニマス","value":54},
        {"name":"ライスシャワー(ウマ娘},","value":54},
        {"name":"たくしあげ","value":53},
        {"name":"宣伝","value":53},
        {"name":"圧倒的胸囲","value":53},
        {"name":"ストッキング","value":53},
        {"name":"うちの子","value":53},
        {"name":"C96","value":53},
        {"name":"猫","value":52},
        {"name":"男の娘","value":52},
        {"name":"ボブカット","value":52},
        {"name":"紐タイ","value":52},
        {"name":"アズレン","value":52},
        {"name":"横乳","value":52},
        {"name":"ウマ娘プリティーダービー5000users入り","value":52},
        {"name":"エロ衣装","value":51},
        {"name":"はいてない","value":51},
        {"name":"夏","value":51},
        {"name":"Re:ゼロから始める異世界生活","value":51},
        {"name":"マント","value":50},
        {"name":"輪チラ","value":50},
        {"name":"艦これ5000users入り","value":50},
        {"name":"練習","value":50},
        {"name":"抱き枕カバー","value":50},
        {"name":"original","value":50},
        {"name":"フェラ","value":50},]
    }
    return json.dumps(data)

@app.route('/illustrator')
def profile():
    user_id = request.args.get('id').strip()
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
    return render_template('user_profile.html', userId=user_id, userName=userName, bg=bg, profile_image=profile_image, urls=urls, following_count=following_count, follower_count=follower_count, userComment=userComment)

    
app.run(host='0.0.0.0',debug=True)

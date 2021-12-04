from flask import Flask,request,render_template
import shelve,webbrowser
with shelve.open("data") as _d:
    Users=_d["relation"]
    # for i in Users:
    #     Users[i][1]=[j for j in Users[i][1] if j]
    #     Users[i][2]=[j for j in Users[i][2] if j]
    # _d["relation"]=Users
# exit()
app=Flask(__name__)
@app.route("/follow")
def f_():
    foll=request.args.get("foll","粉丝")
    userId=request.args.get("userId","11")
    limit=int(request.args.get("limit","1000"))
    if userId in Users:
        if foll=="粉丝":
            selected_users=[userId]+[useId for useId in Users[userId][1] if len(Users[useId][1])>limit]
            nodes=[[Users[i][0],len(Users[i][1])/1000] for i in selected_users]
            edges=[]
            for i in range(len(selected_users)):
                for j in Users[selected_users[i]][1]:
                    if j in selected_users:
                        edges.append([i,selected_users.index(j)])
        else:
            selected_users=[userId]+[useId for useId in Users[userId][2] if len(Users[useId][2])>limit]
            nodes=[[Users[i][0],len(Users[i][2])/1000] for i in selected_users]
            edges=[]
            for i in range(len(selected_users)):
                for j in Users[selected_users[i]][2]:
                    if j in selected_users:
                        edges.append([i,selected_users.index(j)])
    else:
        nodes,edges=[],[]
    return render_template("try_d3.html",nodes=nodes,edges=edges,userId=userId,limit=limit,foll=foll)
webbrowser.open("http://localhost:8010/follow")
app.run("0.0.0.0",8010)
# Git仓库使用指南
## Git及管理工具下载
1. 访问 https://www.sourcetreeapp.com/ 下载软件（Windows版本及Mac版本均有）
2. 安装，勾选安装git

## 克隆Git仓库
1. 打开 sourcetree，选择`clone`
2. 在`Source Path`输入`gitrepo@101.132.109.217:~/ICE2604_Final_Project`
3. 需要登陆，密码见公用账号.txt
4. `Destination Path`选择一个你本地的空文件夹
5. 点击`Clone`，即完成克隆。

## 修改用户名
1. 在菜单栏点击`Reprsitory->Repository Setting`
2. 点击`Advanced`，修改`User Information`

## 做出更改，提交并推送到远程仓库
1. 像对待正常文件夹一样自由修改添加内容。
2. 打开Source Tree，在左侧History中找到你想要提交的更改，点击`stage`（如果需要全部提交，也可点击`stage all`)。
3. 在文本框中书写日志，描述你做了什么，然后点击`Commit`
4. 提交之后，你的更改还只是在本地，并不能让其他人看到，还需要推送到远程仓库。
5. 点击上方菜单栏的`Push`，即可将更改推送。

## 同步
1. 在开始一天的工作以前，最好同步一下进度，免得做无用功以及引起冲突。
2. 点击上方菜单栏的`Pull`，即可从远程仓库拉取记录。

## Commit Log 书写规范
详见 https://zhuanlan.zhihu.com/p/90281637 。我们只需要写清楚 type 和 subject 即可。

## Ending
你已经学会git最基本的操作，可以很方便地和组员进行协同了！  
还有诸如check out, revert, branch, merge, rebase, fetch, stash 等进阶操作就等你自己探索了。
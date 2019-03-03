#R6查战绩
from nonebot import on_command, CommandSession
import requests
from os import path
import pickle
recorddict = {}
@on_command("recordsearch", aliases=("查战绩"), only_to_me=False)
async def zhanji(session: CommandSession):
    ID=session.get("ID", prompt="请输入您的账号名")
    zhanji = await chazhanji(ID)
    if zhanji =="" :
        await session.send("未找到该玩家!")
    else:
        print("finding..........")
        await session.send(zhanji)
#一次性查找----------------------------------------------------------

@on_command("bind", aliases=("绑定", "绑定账号"), only_to_me=False)
async def bind(session: CommandSession):
    global recorddict
    loaddict()
    ID=session.get("ID", prompt="请输入绑定的账号")
    recorddict[str (session.ctx["user_id"])] = ID
    savedict(recorddict)
    await session.send("绑定成功！")

@on_command("search", aliases=("我的战绩", "myrecord"), only_to_me=False)
async def search(session: CommandSession):
    global recorddict
    loaddict()
    if not str(session.ctx["user_id"]) in recorddict:
        session.finish("您还未绑定！")
    zhanji = await chazhanji(recorddict[str (session.ctx["user_id"])])
    if zhanji =="" :
        await session.send("未找到该玩家!")
    else:
        print("finding..........")
        await session.send(zhanji)

#绑定查找-------------------------------------------------------------
@zhanji.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.args["ID"] = stripped_arg

@bind.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.args["ID"] = stripped_arg
#处理命令------------------------------------------------------------
async def chazhanji(ID: str) -> str:

    Identity = f"{ID}"
    R6url = "https://www.r6s.cn/Stats?platform=uplay&username=" + Identity
    recordjson = requests.get(R6url)
    if not recordjson == "<Response [500]>":
        record = recordjson.json()
    else:
        await session.finish("未找到该玩家!")
    if len(record["StatGeneral"]) == 0:
        return f""
    level = record["Basicstat"][0]["level"]
    rankmath = record["Basicstat"][0]["max_rank"]
    maxmmr = record["Basicstat"][0]["max_mmr"]
    kills = record["StatGeneral"][0]["kills"]
    headshot = record["StatGeneral"][0]["headshot"]
    deaths = record["StatGeneral"][0]["deaths"]
    won = record["StatGeneral"][0]["won"]
    lost = record["StatGeneral"][0]["lost"]
    meleek = record["StatGeneral"][0]["meleeKills"]   
    Score = record["StatsScore"][0]["generalScore"]
    if rankmath == 0:
        rank = "未定级"
    elif rankmath <=4 and rankmath>=1:
        rank = "紫铜"+str(4-(rankmath-0))
    elif rankmath <=8 and rankmath>=5:
        rank = "黄铜"+str(4-(rankmath-5))
    elif rankmath <=12 and rankmath>=9:
        rank = "白银"+str(4-(rankmath-9))
    elif rankmath <=16 and rankmath>=13:
        rank = "黄金"+str(4-(rankmath-13))
    elif rankmath <=19 and rankmath>=17:
        rank = "铂金"+str(3-(rankmath-17))
    elif rankmath ==20:        
        rank = "钻石"   
    winrate = round(won/(won+lost),3)
    deathrate = round(kills/deaths,3)
    headshotrate = round(headshot/kills,3)

    return f"{ID}的战绩为：\n 等级："+str(level)+"  最高段位："+str(rank)+"    最高mmr："+str(maxmmr)+"\n击杀："+str(kills)+"  死亡："+str(deaths)+"  爆头："+str(headshot)+"  近战击杀："+str(meleek)+"  胜利："+str(won)+"  失败："+str(lost)+"\nKD:"+str(deathrate)+"  胜率："+str(winrate)+"  爆头率："+str(headshotrate)+"  评分："+str(Score)

#查找-------------------------------------------------------------------------------

def savedict(recorddict):
    with open(path.dirname(__file__)+r"\savedict\zhanjisave.pickle","wb") as outfile:
        pickle.dump(recorddict,outfile)
    print("------------------------save")

def loaddict():
    global recorddict
    temp = {}
    with open(path.dirname(__file__)+r"\savedict\zhanjisave.pickle","rb") as outfile:
        if path.getsize(path.dirname(__file__)+r"\savedict\zhanjisave.pickle") == 0 or str(outfile.read()) == r"b'\xff\xfe'":
            print("init........")
            savedict(temp)
        outfile.seek(0)
        temp = pickle.load(outfile)
    recorddict = temp
    print("------------------------load")
#保存读取----------------------------------------------------------------------------
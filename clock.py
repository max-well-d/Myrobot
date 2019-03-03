import time
from os import path
import pickle
from threading import Timer

from nonebot import on_command, CommandSession

recorddict = {}
@on_command("setclock", aliases=("定时", "预定"), only_to_me=False)
async def setclock(session: CommandSession):
    global recorddict
    session.get("time" ,prompt="您想在什么时间让我通知您？(24小时制，精确到分钟)")
    session.get("what" ,prompt="您要提醒的内容？")
    msgtype = session.ctx["message_type"]
    if msgtype == "group" or msgtype =="discuss":
        recorddict[session.args["time"]].append({session.ctx["group_id"]:session.args["what"]})
    if msgtype == "private":
        recorddict[session.args["time"]].append({session.ctx["user_id"]:session.args["what"]})


@on_command("startclock", aliases("开始定时",), only_to_me=False)
async def startclock(session: CommandSession):
    inc = 20
    perform_command(inc)

async def perform_command(inc):
    global recorddict
    nowtime = time.time()
    nowtime = time.strftime("%H:%M", time.localtime(nowtime))
    if recorddict.get(nowtime,0) != 0:
        return recorddict[nowtime]
    Timer(60,await perform_command,(20,)).start()

@on_command("delclock", aliases=("删除定时", "删除预定"), only_to_me=False)
async def delclock(session: CommandSession):

@on_command("myclock", aliases=("我的定时", "我的预定"), only_to_me=False)
async def myclock(session: CommandSession):

@setclock.args_parser
async def _1(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.args["time"] = stripped_arg

@delclock.args_parser
async def _2(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.args["num"] = stripped_arg

async def print_event(ID: str)-> str:



def saveclock(recordcclock):
    with open(path.dirname(__file__)+r"\savedict\clocksave.pickle","wb") as outfile:
        pickle.dump(recorddict,outfile)
    print("------------------------save")

def loadclock():
    global recordclock
    temp = {}
    with open(path.dirname(__file__)+r"\savedict\clocksave.pickle","rb") as outfile:
        if path.getsize(path.dirname(__file__)+r"\savedict\clocksave.pickle") == 0 or str(outfile.read()) == r"b'\xff\xfe'":
            print("init........")
            saveclock(temp)
        outfile.seek(0)
        temp = pickle.load(outfile)
    recordclock = temp
    print("------------------------load")
#保存读取----------------------------------------------------------------------------
import time
from os import path
import pickle
import random,string

from nonebot import on_command, CommandSession, permission
from apscheduler.schedulers.asyncio import AsyncIOScheduler
r_dict_p = {}
r_dict_g = {}


scheduler =AsyncIOScheduler()
scheduler.start()

def load():
    global r_dict_g,r_dict_p
    temp = {}
    empty = {}
    with open(path.dirname(__file__)+r"\savedict\clocksavep.pickle","rb") as outfile:
        if path.getsize(path.dirname(__file__)+r"\savedict\clocksavep.pickle") == 0 or str(outfile.read()) == r"b'\xff\xfe'":
            print("init........")
            save_p(empty)
        outfile.seek(0)
        temp = pickle.load(outfile)
        r_dict_p = temp

    with open(path.dirname(__file__)+r"\savedict\clocksaveg.pickle","rb") as outfile:
        if path.getsize(path.dirname(__file__)+r"\savedict\clocksaveg.pickle") == 0 or str(outfile.read()) == r"b'\xff\xfe'":
            print("init........")
            save_g(empty)
        outfile.seek(0)
        temp = pickle.load(outfile)
        r_dict_g = temp
    print("------------------------load")

def save_g(r_dict_g):
    with open(path.dirname(__file__)+r"\savedict\clocksaveg.pickle","wb") as outfile:
        pickle.dump(r_dict_g,outfile)
    print("------------------------save_g")
def save_p(r_dict_p):
    with open(path.dirname(__file__)+r"\savedict\clocksavep.pickle","wb") as outfile:
        pickle.dump(r_dict_p,outfile)
    print("------------------------save_p")
#保存读取----------------------------------------------------------------------------

load()
print("-----定时列表初始化-----")

# dict{ID:list[{msg{time:code}}]}
@on_command("startclock", aliases=("开始定时","定时开始"), only_to_me=False)
async def startclock(session: CommandSession):
    global scheduler,r_dict_p,r_dict_g
    botmsg = session.bot
    for ID,_list in r_dict_p.items():
        for num,_dict in enumerate(_list):
            for key,msgd in _dict.items():
                for msg,code in msgd.items():
                    hour = msg.partition(":")[0]
                    minute = msg.partition(":")[2]
                    print("add a job at"+hour+":"+minute + " msg:"+key+ "to:"+ID)
                    print("code="+code)
                    scheduler.add_job(func=perform_command,args=(botmsg,1,ID,num),trigger='cron',hour=hour, minute=minute,id=ID+":"+code)

    for ID,_list in r_dict_g.items():
        for num,_dict in enumerate(_list):
            for key,msgd in _dict.items():
                for msg,code in msgd.items():
                    hour = msg.partition(":")[0]
                    minute = msg.partition(":")[2]
                    print("add a job at"+hour+":"+minute + " msg:"+key+ "to:"+ID)
                    print("code="+code)
                    scheduler.add_job(func=perform_command,args=(botmsg,0,ID,num),trigger='cron',hour=hour, minute=minute,id=ID+":"+code)
    try:
        scheduler.start()
    except:
        print("时钟已经启动")
    finally:
        await session.send("所有定时已启动")

@on_command("setclock", aliases=("定时", "预定"), only_to_me=False)
async def setclock(session: CommandSession):
    global r_dict_p ,r_dict_g ,scheduler
    session.get("time" ,prompt="您想在什么时间让我通知您？(24小时制，精确到分钟)")
    session.get("what" ,prompt="您要提醒的内容？")
    msgtype = session.ctx["message_type"]
    code =random.choice(string.ascii_lowercase)
    for i in range(7):
        code = code + random.choice(string.ascii_lowercase + string.digits)
    if msgtype == "group" or msgtype =="discuss":
        if not r_dict_g.get(str(session.ctx["group_id"]),0):r_dict_g[str(session.ctx["group_id"])]=[]
        r_dict_g[str(session.ctx["group_id"])].append({session.args["what"]:{session.args["time"]:code}})
        is_private = 0
        lens = str(len(r_dict_g[str(session.ctx["group_id"])]))
        ID = str(session.ctx["group_id"])
        save_g(r_dict_g)
    if msgtype == "private":
        if not r_dict_p.get(str(session.ctx["user_id"]),0):r_dict_p[str(session.ctx["user_id"])]=[]
        r_dict_p[str(session.ctx["user_id"])].append({session.args["what"]:{session.args["time"]:code}})
        is_private = 1
        ID = str(session.ctx["user_id"])
        lens = str(len(r_dict_p[str(session.ctx["user_id"])]))
        save_p(r_dict_p)
    botmsg = session.bot
    which = int(lens) - 1
    hour = session.args["time"].partition(":")[0]
    minute = session.args["time"].partition(":")[2]
    print("add a job at"+hour+":"+minute + " msg:"+session.args["what"]+ "to:"+ID)
    scheduler.add_job(func=perform_command,args=(botmsg,is_private,ID,which),trigger='cron',hour=hour, minute=minute,id=ID+":"+code)
    await session.send("定时开始！")


async def perform_command(botmsg,is_private,ID,which):
    global r_dict_p ,r_dict_g
    nowtime = time.time()
    nowtime = time.strftime("%H:%M", time.localtime(nowtime))
    print("--------"+nowtime+"--------\n")
    print(which)
    if is_private == 0:
        for msg in r_dict_g[ID][which]:
            await botmsg.send_group_msg(group_id=ID,message=msg)
    else:
        for msg in r_dict_p[ID][which]:
            await botmsg.send_private_msg(user_id=ID,message=msg)


@on_command("delclock", aliases=("删除定时", "删除预定"), only_to_me=False)
async def delclock(session: CommandSession):
    global r_dict_g,r_dict_p ,scheduler
    msgtype = session.ctx["message_type"]
    num = session.get("num",prompt="你想删除哪一个定时任务？（回复0取消）")
    if num == "0":await session.finish("取消删除")
    if msgtype == "group" or msgtype =="discuss":
        if r_dict_g.get(str(session.ctx["group_id"]),0):
            if int(num) > len(r_dict_g[str(session.ctx["group_id"])]):session.finish("没有这个任务")
            for msg,coded in r_dict_g[str(session.ctx["group_id"])][int(num)-1].items():
                for code in coded.values():
                    del r_dict_g[str(session.ctx["group_id"])][int(num)-1]
                    scheduler.remove_job(str(session.ctx["group_id"])+":"+code)
                    await session.send("成功删除！")
                    save_g(r_dict_g)
            
        else:await session.send("你还没有定时任务")
    elif r_dict_p.get(str(session.ctx["user_id"]),0):
        if int(num) > len(r_dict_p[str(session.ctx["user_id"])]):session.finish("没有这个任务")
        for msg,coded in r_dict_p[str(session.ctx["user_id"])][int(num)-1].items():
            for code in coded.values():
                del r_dict_p[str(session.ctx["user_id"])][int(num)-1]
                scheduler.remove_job(str(session.ctx["user_id"])+":"+code)
                await session.send("成功删除！")
                save_p(r_dict_p)
    else:await session.send("你还没有定时任务")


@on_command("myclock", aliases=("我的定时", "我的预定"), only_to_me=False)
async def myclock(session: CommandSession):

    global r_dict_g,r_dict_p
    if session.ctx["message_type"] == "private": 
        if r_dict_p.get(str(session.ctx["user_id"]),0):
            for num,_dict in enumerate(r_dict_p[str(session.ctx["user_id"])]):
                for key,msgd in _dict.items():
                    for msg in msgd:
                        await session.send(str(num +1)+"."+"  时间: "+msg+"内容: "+key)
        else:
            await session.send("你还没有定时任务")
    elif r_dict_g.get(str(session.ctx["group_id"]),0):
        for num,_dict in enumerate(r_dict_g[str(session.ctx["group_id"])]):
            for key,msgd in _dict.items():
                for msg in msgd:
                    await session.send(str(num +1)+"."+"  时间: "+msg+"内容: "+key)
    else:
        await session.send("你还没有定时任务")

@on_command("closeclock", permission=permission.SUPERUSER)
async def clcl(session:CommandSession):
    global scheduler
    scheduler.shutdown(wait = False)



'''
@setclock.args_parser
async def _1(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.args["time"] = stripped_arg
'''
@delclock.args_parser
async def _2(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.args["num"] = stripped_arg





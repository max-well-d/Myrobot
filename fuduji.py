#fuduji
from nonebot import on_command, CommandSession, on_natural_language, NLPSession, NLPResult
from nonebot.command.argfilter import extractors, validators
import random

switch = {}

@on_command("fudustart",aliases=("开始复读","复读开始"), only_to_me=False)
async def openfd(session: CommandSession):
    global switch
    global quanzhi
    msgtype = session.ctx["message_type"]
    session.get("quan", prompt="请输入复读概率1~100")#, arg_filters=[between_inclusive(start=1, end=100, message="范围或格式错误")])
    if session.args["quan"].isdigit() :
        if int(session.args["quan"]) < 1 or int(session.args["quan"]) > 100:
            await session.finish("输入范围有误，复读失败") 
    else :
        await session.finish("输入的不是数字，复读失败")
    await session.send("复读开始")
    quanzhi = int(session.args["quan"])
    if msgtype == "group" or msgtype == "discuss":
        switch[str(session.ctx["group_id"])] = 1
        switch[str(session.ctx["group_id"])+"q"] = quanzhi
    elif msgtype == "private":
        switch[str(session.ctx["user_id"])] = 1
        switch[str(session.ctx["user_id"])+"q"] = quanzhi
@openfd.args_parser
async def _(session:CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if  stripped_arg != "" :
        if stripped_arg.isdigit() :
            if int(stripped_arg) < 1 or int(stripped_arg) > 100:
                await session.finish("输入范围有误，复读失败") 
        else :
            await session.finish("输入的不是数字，复读失败")

    if stripped_arg:
        session.args["quan"] = stripped_arg

@on_command("fudustop",aliases=("结束复读","复读结束"), only_to_me=False)
async def closefd(session: CommandSession):
    global switch
    msgtype = session.ctx["message_type"]
    if msgtype == "group" or msgtype =="discuss":switch[str(session.ctx["group_id"])] = 0
    if msgtype == "private":switch[str(session.ctx["user_id"])] = 0
    await session.send("复读结束")


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    global switch
    msgtype = session.ctx["message_type"]
    if msgtype == "group" or msgtype == "discuss":
        if switch.get(str(session.ctx["group_id"]),0):
            return NLPResult(100.0,("fuduji"),{"message": session.msg})
    elif switch.get(str(session.ctx["user_id"]),0):
        return NLPResult(100.0,("fuduji"),{"message": session.msg})
    return None

@on_command("fuduji")
async def fudu(session: CommandSession):
    num=random.randint(1,100)
    global switch
    msgtype = session.ctx["message_type"]
    if msgtype == "group" or msgtype =="discuss":quan = switch[str(session.ctx["group_id"])+"q"]
    if msgtype == "private":quan = switch[str(session.ctx["user_id"])+"q"]
    if num <= quan:
        await session.send(session.ctx["message"])
    else:
        pass

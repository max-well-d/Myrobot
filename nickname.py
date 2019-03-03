from nonebot import on_command, CommandSession, on_natural_language, NLPSession, NLPResult
from os import path
import pickle
nicknamedict={}
@on_command("callme", aliases=("叫我","就叫我"), only_to_me=False)
async def nickname(session: CommandSession):
    global nicknamedict, ID
    loaddict()
    session.get("nickname", prompt="我该叫你什么呢？")
    if nicknamedict.get(str(session.ctx["user_id"]),0) == 0:
        nicknamedict[ID] = session.args["nickname"]
        await session.send("好的" + session.args["nickname"])
    elif session.args["nickname"] == nicknamedict[ID]:
        await session.send("我已经认识你了" + session.args["nickname"])
    else:
        await session.send("原来你叫" + session.args["nickname"]+"啊" )
    nicknamedict[ID] = session.args["nickname"]
    resavedict(nicknamedict)

@on_natural_language(allow_empty_message=True)
async def _(session: NLPSession):
    at = str(session.ctx["message"]).strip()
    if len(at) == 0:
        return NLPResult(100.0,("atme"),{"message": session.msg})

@on_command("atme")
async def atme(session: CommandSession):
    global nicknamedict
    loaddict()
    if nicknamedict.get(str(session.ctx["user_id"]),0):
        await session.send("我一直在线上等着你，" + nicknamedict[str(session.ctx["user_id"])])
    else:
        await session.send("很期待认识你，" + str(session.ctx["user_id"]) )

@nickname.args_parser
async def _(session: CommandSession):
    global ID, nicknamedicts
    ID = str(session.ctx["user_id"])
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.args["nickname"] = stripped_arg

def resavedict(nicknamedict):
    with open(path.dirname(__file__)+r"\savedict\nicknamesave.pickle","wb") as outfile:
        pickle.dump(nicknamedict,outfile)
    print("------------------------save")

def loaddict():
    global nicknamedict 
    temp = {}
    with open(path.dirname(__file__)+r"\savedict\nicknamesave.pickle","rb") as outfile:
        if path.getsize(path.dirname(__file__)+r"\savedict\nicknamesave.pickle") == 0 or str(outfile.read()) == r"b'\xff\xfe'":
            print("init......")
            resavedict(temp)
        outfile.seek(0)
        temp = pickle.load(outfile)
    nicknamedict = temp
    print("------------------------load")
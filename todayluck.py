import requests
from nonebot import on_command, CommandSession

@on_command("constellation", aliases =("运气", "运势", "我的运势"), only_to_me=False)
async def constellation(session: CommandSession):
    session.get("xingzuo", prompt= "请输入你的星座")
    if session.args["xingzuo"] == "白羊座" or session.args["xingzuo"] == "白羊" or session.args["xingzuo"] == "Aries":
        xingzuo = "Aries"
    elif session.args["xingzuo"] == "金牛座" or session.args["xingzuo"] =="金牛" or session.args["xingzuo"] =="Taurus":
        xingzuo = "Taurus"
    elif session.args["xingzuo"] == "双子座" or session.args["xingzuo"] =="双子" or session.args["xingzuo"] =="Gemini":
        xingzuo = "Gemini"
    elif session.args["xingzuo"] == "巨蟹座" or session.args["xingzuo"] =="巨蟹" or session.args["xingzuo"] =="Cancer":
        xingzuo = "Cancer"
    elif session.args["xingzuo"] == "狮子座" or session.args["xingzuo"] =="狮子" or session.args["xingzuo"] =="Leo":
        xingzuo = "Leo"
    elif session.args["xingzuo"] == "处女座" or session.args["xingzuo"] =="处女" or session.args["xingzuo"] =="Virgo":
        xingzuo = "Virgo"
    elif session.args["xingzuo"] == "天秤座" or session.args["xingzuo"] =="天秤" or session.args["xingzuo"] =="Libra":
        xingzuo = "Libra"
    elif session.args["xingzuo"] == "天蝎座" or session.args["xingzuo"] =="天蝎" or session.args["xingzuo"] =="Scorpio":
        xingzuo = "Scorpio"
    elif session.args["xingzuo"] == "射手座" or session.args["xingzuo"] =="射手" or session.args["xingzuo"] =="Sagittarius":
        xingzuo = "Sagittarius"
    elif session.args["xingzuo"] == "摩羯座" or session.args["xingzuo"] =="摩羯" or session.args["xingzuo"] =="Capricorn":
        xingzuo = "Capricorn"
    elif session.args["xingzuo"] == "水瓶座" or session.args["xingzuo"] =="水瓶" or session.args["xingzuo"] =="Aquarius":
        xingzuo = "Aquarius"
    elif session.args["xingzuo"] == "双鱼座" or session.args["xingzuo"] =="双鱼" or session.args["xingzuo"] =="Pisces":
        xingzuo = "Pisces"
    else:
        await session.finish("输入的不是星座！")
    yunshitext = await find(xingzuo)
    await session.send(yunshitext)

async def find(xingzuo: str) -> str:
    luckurl = "https://3g.d1xz.net/yunshi/today/" + xingzuo
    luck = requests.get(luckurl)
    yunshiraw = luck.text
    title = titlecut(yunshiraw)
    time = timecut(yunshiraw)
    yunshi = yunshicut(yunshiraw)
    score = scorecut(yunshiraw)
    lucky = luckycut(yunshiraw)
    return "               " + title + "\n\n" + time + "\n\n" + yunshi + "\n" + score + "\n" + lucky

@constellation.args_parser
async def _(session:CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if stripped_arg:
        session.args["xingzuo"] = stripped_arg

def titlecut(html):
    # 内容分割的标签
    key1 = '<div class="public_yd_name">'
    key2 = '</div>'
    content = html.partition(key1)[2]
    content = content.partition(key2)[0]
    return content # 得到网页的内容

def timecut(html):
    #分割时间
    key1 = '<p class="public_yd_effective">'
    key2 = '</p>'
    content = html.partition(key1)[2]
    content = content.partition(key2)[0]
    return content # 得到网页的内容

def yunshicut(html):
    #分割运势
    key1 = '<div class="public_yd_info">'
    key2 = '</div>'
    content = html.partition(key1)[2]
    content = content.partition(key2)[0]
    return content  # 得到网页的内容
#评分    
#色、数字、星座


def scorecut(html):
    key1 = '<div class="public_yd_fraction">'
    key2 = '</div></div></div>'
    content = html.partition(key1)[2]
    content = content.partition(key2)[0]
    key1 = '<strong>'
    key2 = '</strong>'
    content1 = content.partition(key1)[2]
    content2 = content1.partition(key2)[0]
    ganqing  = "\n感情：" + content2
    content1 = content1.partition(key1)[2]
    content2 = content1.partition(key2)[0]
    jiankang = "  健康：" + content2
    content1 = content1.partition(key1)[2]
    content2 = content1.partition(key2)[0]
    caiyun   = "  财运：" + content2
    content1 = content1.partition(key1)[2]
    content2 = content1.partition(key2)[0]
    gongzuo  = "  工作：" + content2
    content1 = content1.partition(key1)[2]
    content2 = content1.partition(key2)[0]
    zonghe   = "  综合：" + content2
    return ganqing + jiankang + caiyun + gongzuo + zonghe

def luckycut(html):
    key1 = '<div class="public_yd_circular">'
    key2 = '</div></div>'
    content = html.partition(key1)[2]
    content = content.partition(key2)[0]
    key1 = '<div>'
    key2 = '<p>'
    content1 = content.partition(key1)[2]
    content2 = content1.partition(key2)[0]
    xys      = "幸运色：" + content2
    content1 = content1.partition(key1)[2]
    content2 = content1.partition(key2)[0]
    xysz     = "  幸运数字：" + content2
    content1 = content1.partition(key1)[2]
    content2 = content1.partition(key2)[0]
    xzsp     = "  星座速配：" + content2
    return xys + xysz + xzsp
'''
def find():
    xingzuo = "Aquarius"
    luckurl = "https://3g.d1xz.net/yunshi/today/" + xingzuo
    luck = requests.get(luckurl)
    yunshiraw = luck.text
    scores = score(yunshiraw)
    luckys = lucky(yunshiraw)
find()
'''
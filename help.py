#help
from nonebot import on_command, CommandSession
@on_command("help", only_to_me=False)
async def help(session: CommandSession):
	help = '''目前支持的指令有：#help
	#recordsearch(#查战绩)
	#bind(#绑定，#绑定账号)
	#search(#我的战绩, #myrecord)
	#fudustart(#开始复读，#复读开始)
	#fudustop(#结束复读，#复读结束)
	#callme(#叫我，#就叫我)
	#constellation(#运气，#运势，#我的运势)
	#huangli(#黄历, #查黄历)
	#newhotpoint(#热点,#当前热点) 
	#tdhotpoint(#今日热点,#今天热点)
	#givemeurl(#连接)
	#setclock(#定时,#预定)
	#startclock(#开始定时,#定时开始)
	#myclock(#我的定时,#我的预定)
	#delclock(#删除定时,#删除预定)
	#closeclock--Admin
	'''
	await session.send(help) 
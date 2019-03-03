from nonebot import on_command, CommandSession
@on_command("groupid")
async def gd(session: CommandSession):
	print (session.ctx["user_id"])
	if session.ctx["message_type"] == "group": print (session.ctx["group_id"])
	print (session.ctx["message_type"])
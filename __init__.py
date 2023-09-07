import os
try:
    from Builtin import eventclass, Action, CONFIG, Color
except:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), f'../../Builtin'))
    from Builtin import eventclass, Action, CONFIG, Color
import re
import json5
import random
import time
import yaml
import ruamel.yaml

PluginName = 'CustomBot'
VersionCode = "Str"
Version = "0.0.6b"
Developer = "仓鼠"

Host = CONFIG.Host

HaveReply = True
HaveLog = False

random.seed(time.time())

UserDataPath = "Plugin/CustomBot/UserData/"

#读取配置文件
config = json5.loads(open("Plugin/CustomBot/Config.json","r",encoding = "UTF-8").read())
#读取指令集
CommandList = open("Plugin/CustomBot/Commands.cf","r",encoding="UTF-8").readlines()
#读取权限组文件
PermissionGroup = yaml.load(open("Plugin/CustomBot/Permission.yml","r",encoding="UTF-8"),yaml.Loader)

#指代变量替换
def ReplacePointVar(Msg: str,data: eventclass.Message) -> str:
    try:
        Msg = Msg.replace("$SELF$",config["BotClaiming"])
        Msg = Msg.replace("$OWNER$",config["BotOwner"])
        Msg = Msg.replace("$TARGET$",data.sender["nickname"])
        Msg = Msg.replace("$TARGETQQ$",str(data.sender["user_id"]))
        Msg = Msg.replace("$TIME$",time.strftime("%H:%M:%S",time.localtime))
        Msg = Msg.replace("$YEAR$",time.strftime("%Y",time.localtime))
        Msg = Msg.replace("$MONTH$",time.strftime("%m",time.localtime))
        Msg = Msg.replace("$DAY$",time.strftime("%d",time.localtime))
        Msg = Msg.replace("$RANDOM0-10$",str(random.randint(0,10)))
        Msg = Msg.replace("$RANDOM0-100$",str(random.randint(0,100)))
        Msg = Msg.replace("$RANDDICE$",str(random.randint(1,6)))
    except:
        pass
    return Msg

#检测违禁词
def TestFilter(msg: str) -> bool:
    if len(config["Filter"]) == 0:
        return True
    for i in config["Filter"]:
        if msg.find(i):
            return False
    return True

#功能型指令执行
def StartFunc(Func: str,data: eventclass.Message,arg = []):

    #新建用户文件
    if Func == "NEWDATA":
        try:
            open(UserDataPath + ReplacePointVar(arg[0].replace("\n",""),data) + ".yml","w",encoding="UTF-8")
        except:
            pass

    #删除用户文件
    if Func == "DELDATA":
        try:
            os.remove(UserDataPath + ReplacePointVar(arg[0].replace("\n",""),data) + ".yml")
        except:
            pass
    
    #用户文件操作
    if Func == "DATA":
        yamlData = {}
        try:
            yamlData = yaml.load(open(UserDataPath + ReplacePointVar(arg[0],data) + ".yml","r",encoding="UTF-8").read(),yaml.Loader)
        except:
            pass
        if yamlData == None:
            yamlData = {}
        #写
        if arg[2] == "WRITE":
            yamlData[ReplacePointVar(arg[1],data)] = int(ReplacePointVar(arg[3].replace("\n",""),data))
        #加
        elif arg[2] == "ADD":
            try:
                yamlData[ReplacePointVar(arg[1],data)] += int(ReplacePointVar(arg[3].replace("\n",""),data))
            except:
                yamlData[ReplacePointVar(arg[1],data)] = 0
                yamlData[ReplacePointVar(arg[1],data)] += int(ReplacePointVar(arg[3].replace("\n",""),data))
        #减
        elif arg[2] == "DIM":
            try:
                yamlData[ReplacePointVar(arg[1],data)] -= int(ReplacePointVar(arg[3].replace("\n",""),data))
            except:
                yamlData[ReplacePointVar(arg[1],data)] = 0
                yamlData[ReplacePointVar(arg[1],data)] -= int(ReplacePointVar(arg[3].replace("\n",""),data))
        #删
        elif arg[2].replace("\n","") == "DELETE":
            try:
                del  yamlData[ReplacePointVar(arg[1],data)]
            except:
                pass
        writer = ruamel.yaml.YAML()
        writer.indent(mapping = 2,sequence = 4,offset = 2)
        yamlFile = open(UserDataPath + ReplacePointVar(arg[0],data) + ".yml","w",encoding="UTF-8")
        writer.dump(yamlData,yamlFile)
        yamlFile.close()

#检测功能执行
def TestFunc(Com: list,data: eventclass.Message):
    if len(Com) > 4:
        if(len(Com) == 6):
            StartFunc(Com[5],data)
        else:
            arg = []
            for i in range(len(Com) - 6):
                arg.append(Com[i + 6])
            StartFunc(Com[5],data,arg)
    else:
        pass

#匹配类消息指令回复获取
def GetReply(ReturnType: str,ReturnMsg: str,data: eventclass.Message) -> str:
    if ReturnType == "RTW":
        ReturnMsg = ReplacePointVar(ReturnMsg,data)
        return ReturnMsg
    else:
        ReturnMsgs = ReturnMsg.split("/")
        r = random.randint(0,len(ReturnMsgs) - 1)
        ReturnMsgs[r] = ReplacePointVar(ReturnMsgs[r],data)
        return ReturnMsgs[r]


def IsReply(data: eventclass.Message):
    if isinstance(data, eventclass.GroupMessage):
        if config["GroupReplyMode"] == "Any":
            if TestFilter(data.raw_message):
                return True
            else:
                return False
        else:
            msg = data.raw_message
            atField = "[CQ:at,qq=" + config["BotQQ"] + "]"
            if msg.find(atField) >= 0:
                if TestFilter(msg):
                    return True
                else:
                    return False
            else:
                return False
    else:
        return True

def Reply(data: eventclass.Message,Host):
    msg = data.raw_message
    replyMsg = ""
    old_replyMsg = ""

    #msg预处理
    if config["GroupReplyMode"] == "AT":
        atField = "[CQ:at,qq=" + config["BotQQ"] + "]"
        msg = msg.replace(atField,"")
        msg = msg.replace(" ","")

    #replyMsg预处理
    if config["GroupReplyMode"] == "AT":
        atField = "[CQ:at,qq=" + str(data.sender["user_id"]) + "]"
        replyMsg += atField
    old_replyMsg = replyMsg

    #权限标记
    nowPermission = ""
    isBlack = False

    #黑名单检测
    if str(data.sender["user_id"]) in PermissionGroup["BLACK"]:
        isBlack = True
    
    #匹配指令集
    for Command in CommandList:
        #跳过注释
        if Command.find("#") >= 0:
            if Command.split("#")[0] == "":
                continue
            else:
                Command = Command.split("#")[0]
        #指令分割
        try:
            Commands = Command.split(" ")
            Commands = [i for i in Commands if i]
        except:
            continue
        #权限组切换
        if Commands[0] == "@":
            nowPermission = Commands[1].replace("\n","")
        #匹配类消息指令
        if Commands[0] == "KEY" or Commands[0] == "EQU":
            if Commands[0] == "KEY":
                if msg.find(Commands[1]) >= 0:
                    if nowPermission == "ALL" and isBlack != True:
                        replyMsg += GetReply(Commands[2],Commands[3],data)
                        TestFunc(Commands,data)
                        break
                    else:
                        #匹配指令权限组
                        if str(data.sender["user_id"]) in PermissionGroup[nowPermission]:
                            replyMsg += GetReply(Commands[2],Commands[3],data)
                            TestFunc(Commands,data)
                            break
                        else:
                            pass
            else:
                if Commands[1] == msg:
                    if nowPermission == "ALL" and isBlack != True:
                        replyMsg += GetReply(Commands[2],Commands[3],data)
                        TestFunc(Commands,data)
                        break
                    else:
                        #匹配指令权限组
                        if str(data.sender["user_id"]) in PermissionGroup[nowPermission]:
                            replyMsg += GetReply(Commands[2],Commands[3],data)
                            TestFunc(Commands,data)
                            break
                        else:
                            pass
    
    #校验回复内容
    if replyMsg == old_replyMsg:
        replyMsg += config["UnknowMsgReply"]
        replyMsg = ReplacePointVar(replyMsg,data)
    
    if replyMsg.find("$NULL$") >= 0:
        replyMsg = ""

    if isinstance(data,eventclass.GroupMessage):
        Action.SendMsg(msg=replyMsg, type=data.message_type, Host=Host, id=data.group_id)
    else:
        Action.SendMsg(msg=replyMsg, type=data.message_type, Host=Host, id=data.user_id)
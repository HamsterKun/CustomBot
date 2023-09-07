# <center>《CustomBot插件完全教程》</center>
### <center>前言：什么是CustomBot？我为什么要使用它？</center>
&emsp;&emsp;CustomBot是一款基于MocoBot框架开发的快速实现基于关键词匹配的Bot搭建的插件，CustomBot具有**简洁**，**高效**，**快捷**等优点，让您可以在花费最少的时间下搭建出功能完整，运行稳定的QQBot；加之MocoBot框架自身的便捷性，可以让您在数分钟内即可实现Bot的从开发到部署的工作。CustomBot自身使用的指令语言简单易懂，使用轻松，短短几行便可实现许多功能复杂的对话功能，并且支持多预制随机回复，本地文件存储与管理，权限组等多种功能，帮助您随时随地DIY出属于您自己的QQBot。如果您厌倦了使用别人制作好的Bot，那么请尽情使用MocoBot＋CustomBot创作出属于您自己的作品吧！

----------------------------------------------------------------------

### <center>一、了解CustomBot目录以及配置CustomBot</center>
#### CustomBot目录结构：

&emsp;&emsp;第一次打开CustomBot目录时，我们会看到如下几个文件：
- \_\_init\_\_.py
- Commands.cf
- Config.json
- Permission.yml
- Tutorial.md

&emsp;&emsp;以及一个文件夹：
- UserData

&emsp;&emsp;我们先来了解他们各自是干什么的，“\_\_init\_\_.py”是插件的源代码文件，在您没有编程能力的前提下我们并不建议您改动其中的内容，对其的改动可能造成插件无法正常运行；而“Commands.cf”是Bot的指令集文件，也是您要编写的文件；“Permission.yml”是Bot的权限组文件，内部储存不同用户对Bot的使用权限；“Config.json”中存储的是Bot的基础配置信息，其中的内容并不难懂，在接下来的内容中将会教您如何配置“Config.json”中的内容；而“Tutorial.md”则是您正在阅读的教程文件。至于“UserData”文件夹则是给您存放Bot需要用到的文件的目录。

#### 配置CustomBot：

&emsp;&emsp;配置Bot的第一步是配置Bot的“Config.json”文件,当我们打开“Config.json”后可以看到有关提示，按照提示在双引号中填写您的Bot配置即可；然后便是配置Bot的权限组，打开“Permission.yml”文件，文件内也有详细的指引提示，根据提示配置好Permission.yml即可。

----------------------------------------------------------------------

### <center>二、CustomBot指令教学</center>

#### 1，注释与格式：

&emsp;&emsp;在CustomBot指令中支持您去写指令注释，用于帮助您整理您的指令内容，提示指令作用等等。在CustomBot指令中，以“#”引导注释，如：

    #这是一段注释

注释即可以单独自成一行，也可写在一行指令的最后，如

    KEY  你好  RTW  你好   #检测含“你好”的消息并回复“你好”

&emsp;&emsp;CutomBot指令对格式要求并不严格，表现为换行以及缩进不敏感，总体编写格式相对自由，可以怎么舒服怎么来，不需要特别注意缩进等；甚至指令本身各部分间的空格具体空多少格也可以随意（每个部分空不一样格数都可以）,但必须得空，教程中以空两格书写，方便展示各部分间的空位，实际编写只空一个空格也行。

<br>

#### 2，权限组设置：
&emsp;&emsp;权限组是CustomBot消息类指令的基础，权限组决定了您的Bot的消息会被什么样的人触发；设置权限组的命令很简单，只有两个部分以空格分开：

<center>@&emsp;权限组名称</center>

<br>
&emsp;&emsp;其第一部分“@”符号意味着这是一条设置权限组的指令，下一部分便是权限组名称。

&emsp;&emsp;权限组的作用范围是从一个设置权限组的指令到下一个设置权限组的指令，或到文件结尾；在这个范围内的指令只有该权限组内的成员才可以触发。

&emsp;&emsp;在CustomBot中默认提供了四类权限组：

|权限组名称|权限组对象|
|---------|---------|
|ALL（不需要编辑Permission）|所有人皆可触发（除黑名单用户）|
|OWNER|Bot的拥有者可触发|
|ADMIN|Bot的管理员可触发|
|BLACK|黑名单成员可触发|

&emsp;&emsp;其中**除黑名单权限组中的成员外**，其他权限组的成员均可触发自身权限组中的消息**及**ALL权限组中的消息。

&emsp;&emsp;另外，您也可以在Permission.yml中自定义权限组，在使用设置权限组指令时仅需保持权限组名称与Permission.yml中您起的权限组名称一致即可。

<br>

#### 3，匹配类消息指令：

&emsp;&emsp;该类指令是Bot处理消息的关键指令，该类指令具有固定结构，即：

<center>匹配模式&emsp;匹配字段&emsp;回复模式&emsp;回复字段</center>

<br>
&emsp;&emsp;四个部分构成，四个部分分别用空格分隔，其中“匹配模式”决定“匹配字段”以什么方式去匹配收到的消息,共有两种匹配模式，分别为“KEY”与“EQU”：

<br>

|匹配模式|触发情况|
|---|---|
|KEY|当消息中含有匹配字段时触发|
|EQU|当消息完全等于匹配字段时触发|

<br>

&emsp;&emsp;“回复模式”则决定“回复字段”以什么方式呈现，共有两种回复模式，分别为“RTW”与“RTL”：

|回复模式|回复效果|
|---|---|
|RTW|将回复字段作为回复内容回复|
|RTL|将回复字段以“/”分割为多个部分从中随机选择一个部分作为回复内容回复|

<br>
示例指令一：

    KEY  你好  RTW  你好

该指令意味当Bot收到包含“你好”的句子时返回“你好”

<br>
示例指令二：

    EQU  再见  RTL  再见/辛苦了/拜拜

该指令意味当Bot收到“再见”时会随机返回“再见”、“辛苦了”、“拜拜”中的其中一句

<br>

#### 4，功能类指令：

&emsp;&emsp;该类指令有一个很明显的特点，不具备消息反馈性质，更多的产生实际作用，比如在本地读写文件存储数据等等，功能类指令需要匹配类消息指令激活，其单独除变量赋值外无法使用。其语法是在匹配类消息指令后加入“:”后跟功能类指令，注意，匹配类消息指令与冒号、冒号与功能类指令之间均有空格，如：

    KEY  你好  RTW  你好  ：  功能类指令

接下来将正式开始介绍功能类指令。

<br>

1.文件操作类：

&emsp;&emsp;该类型指令主要是便于Bot存储长期数据使用，类似每个人的金币数，Bot对每个人的好感度等数值的存储，不必担心Bot停止运行后数据丢失。该类文件CustomBot统一以YAML文件的格式进行存储（[了解YAML文件及语法](https://zhuanlan.zhihu.com/p/145173920)），该类文件操作共涉及三大类指令，即：

|指令名称|用处|
|---|---|
|NEWDATA|新建数据文件|
|DATA|管理数据文件，对数据文件进行操作|
|DELDATA|删除数据文件|

其细分语法如下：

    NEWDATA  文件名
    DATA  文件名  键  操作  值
    DELDATA 文件名

NEWDATA与DELDATA语法较为简单，我们直接讲解DATA的操作：

|操作|效果|
|---|---|
|WRITE|对键写入值（不存在该键则会新建并写入值）
|ADD|对键加上值（不存在该键则会新建键并从零加上值）|
|DIM|对键减去值（不存在该键则会新建键并从零减去值）|
|DELETE|删除键（该操作无需填写值）|

在DATA和NEWDATA以及DELDATA的操作中，无论是文件名，还是键或值，均可以使用指代变量

---------------------------------------------------------------------

### <center>三、CustomBot中的指代变量</center>

#### 什么是指代变量：

&emsp;&emsp;指代变量是可以使用在指令的字段中的一种替代某种不确定文字的符号，如Bot的名字，Bot主人的名字，发送消息的人的名字这种不确定的文字，都可以使用相应的指代变量表示，以实现多场景的针对式回答。

#### 指代变量表：

- \$SELF\$ : Bot的自称

- \$NULL\$ : 空白占位符，在回复字段中使用代表不产生回复

- \$TARGET\$ ： 发送消息的人的昵称

- \$TARGETQQ\$ : 发送消息的人的QQ号

- \$OWNER\$ : Bot主人的名称

- \$TIME\$ : 当前“时：分：秒”格式的时间

- \$YEAR\$ : 当前的年份

- \$MONTH\$ : 当前的月份

- \$DAY\$ : 当前的日期

- \$RANDOM0-10\$ : 0至10的随机数

- \$RANDOM0-100\$ : 0至100的随机数

- \$RANDDICE\$ : 模拟掷骰1至6的随机数

----------------------------------------------------------------------

### <center>更新日志</center>

#### 测试版本：
（尾缀a：开发中间产物；尾缀b：可正式使用的开发版本；尾缀m：过渡版本，几乎发布却又继续开发的版本；无尾缀：正式版）
- V0.0.1a : 代码基础框架完工，可以运行，但不具备任何功能
- V0.0.2a ： 完善目录文件，扩展框架内容，但仍不具备使用能力
- V0.0.3b ：加入匹配类消息指令，可以正常使用
- V0.0.4b ：加入基础指代变量
- V0.0.5m ：加入权限组、Filter、注释、扩充指代变量数目、调优CustomBot指令的格式兼容程度、为Bot的消息命令做铺垫
- V0.0.6b : 加入功能型指令：文件操作(新建，写，删除)；加入全新指代变量\$NULL\$；修复\$TARGETQQ\$指代变量无效的问题

----------------------------------------------------------------------

### <center>恭喜你，你毕业了</center>
### <center>快去尝试编写属于自己的Bot吧！</center>
# 茄子派对
控制台游戏，通过复古文字方式体验流行的对战游戏。
结合了上古的MUD游戏的方式和现代的对战游戏。
游戏起源于儿子学习Python编程看到的其它小朋友写的游戏
本代码为了给儿子学习Python做一个例子，我也是一边学习Python一边增加功能，
所以早期版本一定有很多写得不好的地方，期望后面的问题越来越少。

作者：Cherami Liu(cherami.lm@gmail.com)

[解惑](http://www.jiehoo.com)


## 开发计划
- [x] 2020.4.19：游戏改名为茄子派对
- [x] 2020.4.19：提醒胜率功能，根据双方装备和等级情况计算并提醒胜率
- [x] 2020.4.19：肉搏无力情况下有突然爆发
- [x] 2020.4.19：等级功能，根据杀敌数在名字后面显示等级：青铜，白银，黄金，铂金，黑金，钻石，战神
- [x] 2020.4.19：人物攻击准心功能，杀敌越多，准心越强，杀敌数等价于等级
- [x] 2020.4.19：全部其它人物死亡提前吃鸡
- [x] 2020.4.20：玩家血量不足时自动提醒是否使用医疗包补血
- [x] 2020.4.20：一定概率爆击，伤害加倍
- [x] 2020.4.20：显示系统核心参数
- [x] 2020.4.20：攻击次数自动提高准心
- [x] 2020.4.20：完全搞怪语言
- [x] 2020.4.20：交战每超过10轮可以选择终止
- [x] 2020.4.20：增加菜鸡玩家
- [x] 2020.4.20：增加一些交通工具
- [x] 2020.4.20：增加版本号
- [x] 2020.4.20：战斗后显示总回合数
- [x] 2020.4.20：根据区域大小产生更多随机系统玩家
- [x] 2020.4.20：10回合不再提醒选项（决一胜负）
- [x] 2020.4.21：每局游戏开始预先把所有装备和敌人随机分配到固定位置
- [x] 2020.4.21：装备替换后，被替换的装备掉落在相同位置可以被其它人物获取
- [x] 2020.4.21：游戏结束，选择退出还是再玩一局
- [x] 2020.4.21：地图功能，显示当前区域情况
- [x] 2020.4.21：自动搜索功能
- [x] 2020.4.21：自动搜索敌人功能
- [x] 2020.4.21：搜索的时候自动捡起好的装备
- [x] 2020.4.21：玩家可以选择跑动方向，可以反向跑
- [x] 2020.4.21：地图迷雾模式，只能看到探索过的区域
- [x] 2020.4.21：优化数组初始化
- [x] 2020.4.24：重构，切换到多个module的模式
- [x] 2020.4.24：全力搜索敌人时自动装备更好的装备
- [x] 2020.4.24：下次移动前询问是否使用医疗包
- [x] 2020.4.25：显示玩家当前移动方向
- [x] 2020.4.25：毒害功能，毒圈从玩家落地点开始扩散，玩家落地后5单位开始扩散，玩家在毒圈中被直接伤害，头盔不起作用，在毒圈中时间越长，毒害越大
- [x] 2020.4.25：增加游戏耗时
- [x] 2020.4.25：系统中其它人物死亡广播
- [x] 2020.4.26：肥料不能补满时自动使用
- [x] 2020.4.26：失败时也显示游戏信息
- [x] 2020.4.26：遇到肥料能够不浪费时自动使用
- [x] 2020.4.26：战斗选项增加打黑枪，打一枪就跑
- [x] 2020.4.26：重构，打印输出之类的定义方法准备切换非Console模式
- [x] 2020.4.26：作弊彩蛋，地图全开闪现
- [ ] 敌人被打黑枪后开启追杀模式
- [ ] 游戏开始时选择游戏选项
- [ ] 搜索的时候自动忽略差的装备
- [ ] 增加多个装备，备用装备
- [ ] 战斗开始前可以切换装备，装备废弃后自动切换到备用装备
- [ ] 账号功能，创建玩家，玩家游戏记录
- [ ] 增加盔甲
- [ ] 背包容量
- [ ] 自动替换背包中的低档装备
- [ ] 打死敌人后可以拾取他的装备
- [ ] 逃跑的时候的准心可以考虑降低
- [ ] 系统中其它人物随机跑动并可以自动选择更好的装备
- [ ] 系统人物到达相近区域可以进行战斗，综合得分高者自动选择是否战斗
- [ ] 敌人增加智能功能，胜率太低可以逃跑，胜率非常高可以追杀
- [ ] 开始的时候可以选择难度，容易（不允许系统玩家逃跑和追杀），一般（允许系统玩家逃跑），困难（允许逃跑，允许追杀）
- [ ] 2人组队功能，随机匹配一个系统玩家
- [ ] 修改交通工具，增加座位数参数
- [ ] 二维空间

## 许可协议
[署名-非商业性使用 4.0 国际](https://creativecommons.org/licenses/by-nc/4.0/)

![CC BY-NC](https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc.png)

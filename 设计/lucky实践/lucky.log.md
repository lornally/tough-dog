

###### 20260211
Lucky: 让gpt对这个md做了下改进，然后再让kimi参考优化了一下

###### 20260210
Lucky: 我让他去github上搜关于xx方面的skill
Lucky: 我的指令都是我怎么省事怎么来
Lucky: ai自己去解决
###### 20260209
Lucky: kimi和这个忘记密码的位置开始玩命了。。。反复在调，然后就是不对。。。
Lucky: 如果他是基于代码的方式生图，这种应该很好处理。。。为啥会玩命呢
Lucky: 我给了kimi一堆条件，让他生成一个md，以后按我要求的约束来

Lucky: 我搞了一个工作流
Lucky: 现在终于不是随机给我画图了。。。
Lucky: 但是他执行的时候，最后那步还是不太行，就是调用pencil的规范画图
Lucky: 总是画不对
Lucky: 这个我救不了哇
Lucky: 我要生成一个ios下的资讯页面，底导有三个（资讯、快讯、我的）。资讯页面里有三种类型汇聚成的瀑布流结构，标题+纯文字类型、标题+一张大图类型、标题+三张小图类型。
Lucky: 卧槽。。。他搞好了
Lucky: 我让他去阅读下pencil的开发手册
Lucky: 怎么说呢，这个玩意适合给没有UI能力的程序员
Lucky: 要做个啥，就直接描述好需求，ai给你咣咣整出来了
Lucky: 你让kimi在githup上搜一下ui-ux-pro-max，然后集成一下，规定他以后遇到web的UI问题先用这个skill
Lucky: 现在我的kimi下有一个agents.md，记录了我的要求

###### 20260208




1. 让kimi使用pencil
2. 给kimi skill的链接
3. 让ai生成提示词
4. 让kimi参考历史内容



别给我答案, 咱们把问题讨论清楚, 你先看下我的问题是否完整, 你帮我查一下是不是有问题, 咱们把需求讨论清楚了再搞.


chatgpt 理解能力比较好. 讨论需求.



###### 20260206
1. lucky成功的完成了ai设计. pencil skill kimi

###### lucky
Kimi / Claude / Codex 在这里的差异（非常关键）
1️⃣ Claude：UI 库是加分项，不是必需品
Claude 自带较强的：
设计规划能力
审美一致性
所以：
✅ 不指定 UI 库也能画得不错
✅ 指定了会更稳定，但不是质变

对kimi和codex来说UI库是必须项
不然就瞎做
而且在用的过程中我发现有一个很严重的问题
我调教的好一点了，新开一个会话就变sb了
这种简直不能忍
每次新建会话后，kimi就失忆了，之前踩过的坑只要不在同一个会话里就再来一遍

###### 11
纯设计的话 sketch 我也用过。生成起来还是 效果没那么好。
可以借助一些skills 来 做，效果会好很多。 claude Opus 4.5 的 +  skills
https://mcpmarket.com/zh/tools/skills/ui-ux-pro-max-4
这个可以看看，不过生成出来的它应该是 html 不是传统的 ui 设计稿
https://ui-ux-pro-max-skill.nextlevelbuilder.io/#styles
这里有它生成出来的demo

###### roo cline cursor的提示词工程
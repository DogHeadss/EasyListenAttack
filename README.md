## 简介
 一个简单的端口监听脚本。

当有人扫描时,访问到监听端口,会返回Hello World（伪造为正常Web）,并且调用飞书（因为我们公司用飞书，用着顺手就用了）推送告警信息。

该脚本存在一定的局限性,预设的使用场景为内网环境,而非公网服务器,使用公网服务器可能带来流量过大,告警通知过多等问题。

## 使用说明

1.飞书创建机器人（你也可以修改代码，将飞书推送修改为你喜欢的推送）

2.配置脚本中的监听端口（默认8888),以及将飞书webhook机器人的地址替换。

3.启动脚本

## 展示

![image](https://github.com/user-attachments/assets/bc77bdbd-586e-4122-b94d-6f317e269156)

![image](https://github.com/user-attachments/assets/7d919350-917d-4358-8832-0d28d04cef75)

并且为了后续进行统计（自己统,我懒得写）,所有的请求记录会写入到数据库中,数据库采用sqlite（简单点，记录的方式简单点）,会在脚本目录下产生request_logs.db文件,打开即可看见请求记录,后续自己用sql语句统计吧。

![image](https://github.com/user-attachments/assets/1a9d76d2-a4bf-4538-99fb-3421694f8b48)

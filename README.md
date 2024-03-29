# GXU_XuanKe

新版正方教务系统选课脚本

*此脚本可能也适用于其他使用新版正方教务系统的学校*

# 功能介绍

## 你可以做到

- 余课监控，发现有余量课程，声音、邮件提醒

- 自动抢课，不需要坐在电脑前手动刷新

- 自动换课，先退后选，帮你“改签”所选课程

- 一次请求，全部刷新，同时监控多门课程

- 输出课程列表

- 成绩查询

  

## 你不能做到

- 选容量已满的教学班
- 在选课开放时间之外选课
- 选择时间冲突的课程
- 提高网速
- 保证一定选到课


本程序只能用来捡漏，也就是选别人退的课。强烈不建议在选课系统刚刚开放的时候使用本脚本选课（脚本需要先加载所有课程信息，很容易timeout）


受限于网络和程序本身的延迟，本程序的【换课抢课】功能可能会出现原有课程被退掉，但新课程没有选课成功的状况。虽然这种情况出现的概率很低，而且程序中已经做了一些补救措施，但还是请您在使用本功能时予以注意。

# 使用说明

## 安装

安装相关依赖

```
requests==2.22.0
rsa==4.0
beautifulsoup4==4.9.3
```

修改代码中的host_server，自行设置UA头、最大查询次数，最小查询间隔

*可选：如需邮件提醒，还需修改sendAnEmail函数中的邮箱和密码（授权码）*

```python
recipientEmail='recipient@example.com'
UA_headers="User-Agent Example"
host_server='jiaowuxitong.example.edu'
```

```python
def sendAnEmail(recipient, subject, body):
    import smtplib
    myEmail = "sender@example.com"
    PASSWORD = "password"
    from_ = "From:Sender Name<sender@example.com>\n"
    smtpobj = smtplib.SMTP("smtp.example.com", 25)
```

然后直接运行main.py即可

## 使用

1. 输入用户名、密码，登录教务系统（密码回显已关闭）
2. 按程序提示输入操作选项
3. 设置选课志愿信息，选课优先级 课程>任课教师>上课时间，具体规则请参照程序提示。如有不理解之处，请参考源代码。
4. 开始自动选课。


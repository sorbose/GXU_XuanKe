def electCourses(rwlx, xkly, kklxdm):
    # 主修课依次传入'1','1','01',校选课依次传入2,0,10，体育课依次传入2,0,05，均为str型
    # zzxk,自主选课
    print("正在获取课程信息...")
    print("此过程可能需要较长时间")
    urlZzxk = "http://jwxt2018.gxu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su=" + REALID
    resZzxk = s.get(urlZzxk, headers=headers)
    resZzxk.encoding = resZzxk.apparent_encoding
    if kklxdm == "01":
        xkkz_id = re.search(r"\(this,'01','(.*?)'\)", resZzxk.text).group(1)  # 主修
    if kklxdm == "10":
        xkkz_id = re.search(r"\(this,'10','(.*?)'\)", resZzxk.text).group(1)  # 通识选修
    if kklxdm == "05":
        xkkz_id = re.search(r"\(this,'05','(.*?)'\)", resZzxk.text).group(1)  # 体育
    # 下一步再用xkkz_id
    bklx_id = "0"
    xqh_id = re.search(r'<input.*?id="xqh_id".*?value="(.*?)"/>', resZzxk.text).group(1)
    jg_id = re.search(r'<input.*?id="jg_id.*?".*?value="(.*?)"/>', resZzxk.text).group(1)
    zyh_id = re.search(r'<input.*?id="zyh_id".*?value="(.*?)"/>', resZzxk.text).group(1)
    zyfx_id = re.search(r'<input.*?id="zyfx_id".*?value="(.*?)"/>', resZzxk.text).group(1)
    njdm_id = re.search(r'<input.*?id="njdm_id".*?value="(.*?)"/>', resZzxk.text).group(1)
    bh_id = re.search(r'<input.*?id="bh_id".*?value="(.*?)"/>', resZzxk.text).group(1)
    xbm = re.search(r'<input.*?id="xbm".*?value="(.*?)"/>', resZzxk.text).group(1)
    xslbdm = re.search(r'<input.*?id="xslbdm".*?value="(.*?)"/>', resZzxk.text).group(1)
    ccdm = re.search(r'<input.*?id="ccdm".*?value="(.*?)"/>', resZzxk.text).group(1)
    xsbj = re.search(r'<input.*?id="xsbj".*?value="(.*?)"/>', resZzxk.text).group(1)

    sfkknj = sfkkzy = sfznkx = zdkxms = sfkxq = sfkcfx = kkbk = kkbkdj = sfkgbcx = sfrxtgkcxd = tykczgxdcs = "0"
    xkxnm = re.search(r'<input.*?id="xkxnm".*?value="(.*?)"/>', resZzxk.text).group(1)
    xkxqm = re.search(r'<input.*?id="xkxqm".*?value="(.*?)"/>', resZzxk.text).group(1)
    rlkz = "0"
    jxbzb = ""
    # 由于未知的原因，bs4解析html会丢失hidden的<input>，被迫采用正则表达式获取数据

    # 主修课、通识选修、体育课的rwlx,xkly,kklxdm不一样
    # 主修课程rwlx为1，通识选修课、体育分项为2
    # xkly主修为1，通识选修、体育为0
    # kklxdm主修01，通识选修10，体育05
    urlZzxk2 = "http://jwxt2018.gxu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su=" + REALID
    postZzxk2 = {'rwlx': rwlx, 'xkly': xkly, 'bklx_id': bklx_id, 'xqh_id': xqh_id,
                 'jg_id': jg_id, 'zyh_id': zyh_id, 'zyfx_id': zyfx_id, 'njdm_id': njdm_id,
                 'bh_id': bh_id, 'xbm': xbm, 'xslbdm': xslbdm, 'ccdm': ccdm, 'xsbj': xsbj,
                 'sfkknj': sfkknj, 'sfkkzy': sfkkzy, 'sfznkx': sfznkx, 'zdkxms': zdkxms,
                 'sfkxq': sfkxq, 'sfkcfx': sfkcfx, 'kkbk': kkbk, 'kkbkdj': kkbkdj,
                 'sfkgbcx': sfkgbcx, 'sfrxtgkcxd': sfrxtgkcxd, 'tykczgxdcs': tykczgxdcs,
                 'xkxnm': xkxnm, 'xkxqm': xkxqm, 'kklxdm': kklxdm, 'rlkz': rlkz,
                 'kspage': '1', 'jspage': '200', 'jxbzb': jxbzb
                 }
    headersZzxk2 = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '305',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Host': 'jwxt2018.gxu.edu.cn',
        'Origin': 'http://jwxt2018.gxu.edu.cn',
        'Referer': 'http://jwxt2018.gxu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su=' + REALID,
        'X-Requested-With': 'XMLHttpRequest'}
    resZzxk2 = s.post(urlZzxk2, data=postZzxk2, headers=headersZzxk2)
    # print(resZzxk2.text)
    # htmZzxk2=bs4.BeautifulSoup(resZzxk2.text,"html.parser")
    optList = json.loads(resZzxk2.text)["tmpList"]
    urlZzxk3 = "http://jwxt2018.gxu.edu.cn/jwglxt/xsxk/zzxkyzb_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su=" + REALID
    postZzxk3 = {'rwlx': rwlx, 'xkly': xkly, 'bklx_id': bklx_id, 'xqh_id': xqh_id, 'jg_id': jg_id, 'zyh_id': zyh_id,
                 'zyfx_id': zyfx_id,
                 'njdm_id': njdm_id, 'bh_id': bh_id, 'xbm': xbm, 'xslbdm': xslbdm, 'ccdm': ccdm, 'xsbj': xsbj,
                 'sfkknj': sfkknj, 'sfkkzy': sfkkzy,
                 'sfznkx': sfznkx, 'zdkxms': zdkxms, 'sfkxq': sfkxq, 'sfkcfx': sfkcfx, 'kkbk': kkbk, 'kkbkdj': kkbkdj,
                 'xkxnm': xkxnm, 'xkxqm': xkxqm, 'rlkz': rlkz,
                 'kklxdm': kklxdm, 'kch_id': '', 'xkkz_id': xkkz_id, 'cxbj': '', 'fxbj': ''
                 }
    headersZzxk3 = {'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    'Content-Length': '313',
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'Host': 'jwxt2018.gxu.edu.cn',
                    'Origin': 'http://jwxt2018.gxu.edu.cn',
                    'Referer': 'http://jwxt2018.gxu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su=' + REALID,
                    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
                    'X-Requested-With': 'XMLHttpRequest'
                    }
    preKch_id = "";
    i = 0
    allCourList = []
    # fileElectCoursesName="electCourses"+kklxdm+"_"+str(int(time.time()*1000))+".txt"
    # fileElectCourses=open(fileElectCoursesName,"w")
    # fileElectCourses.write("教学班名称\t上课教师信息\t上课时间\t教学地点\t课程性质\t已选/容量\t学分\n")
    for opt in optList:
        kch_id = opt["kch_id"];
        cxbj = opt["cxbj"];
        fxbj = opt["fxbj"]
        xxkbj = opt["xxkbj"];
        kch = opt["kch"]  # xxkbj选课post要用,kch和kch_id不完全一样
        courName = opt["kcmc"];
        chosenNum = opt["yxzrs"];
        courCred = opt["xf"];
        className = opt["jxbmc"]
        if kch_id != preKch_id:
            postZzxk3['kch_id'] = kch_id;
            postZzxk3['cxbj'] = cxbj;
            postZzxk3['fxbj'] = fxbj;
            preKch_id = kch_id
            time.sleep(3 + (random.randint(0, 500)) / 100)
            resZzxk3 = s.post(urlZzxk3, data=postZzxk3, headers=headers)
            i = 0
            aCour = json.loads(resZzxk3.text)[0]
        else:
            i = i + 1
            aCour = json.loads(resZzxk3.text)[i]
        allCourList.append([optList.index(opt), i, kch_id, cxbj, fxbj, courName, aCour["jxbrl"], \
                            aCour["jsxx"].replace("<br/>", ",").split('/')[1], aCour["sksj"].replace("<br/>", ","),
                            aCour["kcxzmc"], courCred, xxkbj, kch])  # 0-6,7-12

        # print(className,aCour["jsxx"].replace("<br/>",","),aCour["sksj"].replace("<br/>",","),aCour["jxdd"].replace("<br/>",","),aCour["kcxzmc"],chosenNum,aCour["jxbrl"],courCred)
        # fileElectCourses.write(className+"\t"+aCour["jsxx"].replace("<br/>",",")+"\t"+aCour["sksj"].replace("<br/>",",")+"\t"+aCour["jxdd"].replace("<br/>",",")+"\t"+aCour["kcxzmc"]+"\t"+chosenNum+"/"+aCour["jxbrl"]+"\t"+courCred+"\n")
    print("获取课程信息完成")
    return (allCourList, postZzxk2, postZzxk3)
    # fileElectCourses.close()
    # print("获取完成")
    # print("课程信息保存到"+fileElectCoursesName)


def inputWishCour(kklxdm):
    resList = []
    tmpList = ['courName', '[wishkkxz]', '[wishTea]', '[notwishTea]', '[wishTime]', '[notwishTime]']
    fileName = "selCourRules" + kklxdm + ".txt"
    try:
        file = open(fileName, 'r')
        fileList = file.readlines()
        file.close()
        for i in range(0, len(fileList)):
            tmpList[i % 6] = fileList[i].rstrip('\n')
            if ((i % 6 == 4) or (i % 6 == 5)) and tmpList[i % 6] == ['*']:
                tmpList[i % 6] = resList[-1][i % 6]
            if (i % 6 != 0):
                tmpList[i % 6] = tmpList[i % 6].split()
            if (i % 6 == 5):
                resList.append(copy.deepcopy(tmpList))
        print("已自动读取您上次设置的选课规则：")
        print(resList)
        print("如需修改，请删除", fileName, "文件后重试")
        return resList
    except FileNotFoundError:
        file = open(fileName, 'w')
    print("请设置选课规则，排在前面的课程将先被选择")
    print("每次只能输入一个课程名称，其他信息可以输入多项，以空格分隔")
    print("输入时间时注意：格式必须和教务系统显示的时间完全一致，*号为同上号")
    print("可以不填直接敲回车，不填将跳过此项筛选条件")
    print("选课优先顺序：课程>老师>时间")
    print("填写完成后，请在输入课程名称的时候输入#号")
    i = 1
    while True:
        print("这是第", str(i), "门课程：")
        tmpList[0] = input("课程全名：")
        if tmpList[0] and tmpList[0][0] == "#":
            file.close()
            return resList
        file.write(tmpList[0] + "\n")
        tmpList[1] = input("课程性质：")
        file.write(tmpList[1] + "\n")
        tmpList[2] = input("课程教师：")
        file.write(tmpList[2] + "\n")
        tmpList[3] = input("不接受的教师：")
        file.write(tmpList[3] + "\n")
        tmpList[4] = input("上课时间：")
        file.write(tmpList[4] + "\n")
        tmpList[5] = input("不接受的时间：")
        file.write(tmpList[5] + "\n")
        tmpList[1] = tmpList[1].split();
        tmpList[2] = tmpList[2].split();
        tmpList[3] = tmpList[3].split();
        tmpList[4] = tmpList[4].split();
        tmpList[5] = tmpList[5].split();
        if tmpList[4] == ["*"]:
            tmpList[4] = resList[i - 2][4]
        if tmpList[5] == ["*"]:
            tmpList[5] = resList[i - 2][5]
        resList.append(copy.deepcopy(tmpList))
        i = i + 1
    file.close()
    return resList


def getInnerCourList(rwlx, xkly, kklxdm):
    # 主修课依次传入'1','1','01',校选课依次传入2,0,10，体育课依次传入2,0,05，均为str型
    resList = []
    userCour = inputWishCour(kklxdm)
    electCoursesRes = electCourses(rwlx, xkly, kklxdm)
    allCour = electCoursesRes[0]
    # print("正在处理选课志愿信息...")
    for uc in userCour:
        for i in range(0, len(uc[2])):
            for j in range(0, len(uc[4])):
                for ac in allCour:
                    Bool = True
                    for notWishTime in uc[5]:
                        if notWishTime in ac[8]:
                            Bool = False
                    # ===课程名称=========教师==================上课时间=================课程类型
                    if uc[0] == ac[5] and uc[2][i] == ac[7] and (uc[4][j] in ac[8]) and (
                            (ac[9] in uc[1]) or (not uc[1])) and Bool:
                        resList.append(copy.deepcopy(ac))
            for ac in allCour:
                Bool = True
                for notWishTime in uc[5]:
                    if notWishTime in ac[8]:
                        Bool = False
                for classTime in uc[4]:
                    if classTime in ac[8]:
                        Bool = False
                if uc[0] == ac[5] and uc[2][i] == ac[7] and ((ac[9] in uc[1]) or (not uc[1])) and Bool:
                    resList.append(copy.deepcopy(ac))
        for ac in allCour:
            Bool = True
            for notWishTime in uc[5]:
                if notWishTime in ac[8]:
                    Bool = False
            for classTime in uc[4]:
                if classTime in ac[8]:
                    Bool = False
            if uc[0] == ac[5] and (ac[7] not in uc[3]) and (ac[7] not in uc[2]) and (
                    (ac[9] in uc[1]) or (not uc[1])) and Bool:
                resList.append(copy.deepcopy(ac))
        for ac in allCour:
            Bool = True
            for notWishTime in uc[5]:
                if notWishTime in ac[8]:
                    Bool = False
            for classTime in uc[4]:
                if classTime in ac[8]:
                    Bool = False
            if (uc[0] == '' or uc[0] == '\n') and (ac[7] not in uc[3]) and (ac[7] not in uc[2]) and (
                    (ac[9] in uc[1]) or (not uc[1])) and Bool:
                resList.append(copy.deepcopy(ac))
    pass
    pass
    # print("处理完成")
    return (resList, electCoursesRes[1], electCoursesRes[2])  # 第二个返回的是postZzxk2


def REPEAT_POST_CourList(rwlx, xkly, kklxdm, xklc, interval, rantim, maxtimes):
    # 前三个参数：主修课依次传入'1','1','01',校选课依次传入2,0,10，体育课依次传入2,0,05，均为str型
    # 第四个参数xklc，可能是选课轮次，要求用户输入,str型
    # 第5,6个参数interval，重复刷新等待的固定时长，rantim,随机等待时长，单位秒，均为int型
    # 第7个参数maxtimes，最大查询次数，int
    time.sleep(3)
    urlZzxk2 = "http://jwxt2018.gxu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su=" + REALID
    urlZzxk3 = "http://jwxt2018.gxu.edu.cn/jwglxt/xsxk/zzxkyzb_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su=" + REALID
    urlZzxk4 = "http://jwxt2018.gxu.edu.cn/jwglxt/xsxk/zzxkyzb_xkBcZyZzxkYzb.html?gnmkdm=N253512&su=" + REALID
    getInnerCourListRes = getInnerCourList(rwlx, xkly, kklxdm)
    postZzxk2 = getInnerCourListRes[1]
    postZzxk3 = getInnerCourListRes[2]
    innerCourList = getInnerCourListRes[0]
    print("请确认以下课程信息，如果查询到有余量的课程将自动提交选课！")
    print("课程名", "教师", "时间", "性质", "学分", "容量", sep='\t')
    for course in innerCourList:
        print(course[5], course[7], course[8], course[9], course[10], course[6], sep='\t')
    isYes = input("确认请输入Y:")
    if isYes != 'Y':
        return
    for cour in innerCourList:
        cour[5] = "(" + cour[12] + ")" + cour[5] + " - " + cour[10] + " 学分"
    postZzxk4 = {'jxb_ids': '', 'kch_id': '', 'kcmc': '', 'xxkbj': '',
                 'cxbj': '',
                 'rwlx': rwlx, 'rlkz': postZzxk2['rlkz'], 'xkkz_id': postZzxk3['xkkz_id'],
                 'njdm_id': postZzxk2['njdm_id'], 'zyh_id': postZzxk2['zyh_id'], 'xkxnm': postZzxk2['xkxnm'],
                 'xkxqm': postZzxk2['xkxqm'],
                 'kklxdm': kklxdm, 'xklc': xklc,
                 'rlzlkz': '1', 'skbz': '1', 'qz': '0',  # 本行数据未从网页中获取到，储存的是静态数据，可能不对
                 }
    for i in range(0, maxtimes):
        print("正在进行第", str(i + 1), "次查询有无余量课程", str(time.time()))
        resZzxk2 = s.post(urlZzxk2, data=postZzxk2, headers=headers)
        optList = json.loads(resZzxk2.text)["tmpList"]
        for cour in innerCourList:
            if optList[cour[0]]['yxzrs'] != cour[6]:
                postZzxk3['kch_id'] = optList[cour[0]]['kch_id'];
                postZzxk3['cxbj'] = optList[cour[0]]['cxbj'];
                postZzxk3['fxbj'] = optList[cour[0]]['fxbj']
                resZzxk3 = s.post(urlZzxk3, data=postZzxk3, headers=headers)
                aCour = json.loads(resZzxk3.text)[0]
                postZzxk4['jxb_ids'] = aCour['do_jxb_id'];
                postZzxk4['kch_id'] = postZzxk3['kch_id'];
                postZzxk4['kcmc'] = cour[5]
                postZzxk4['xxkbj'] = cour[11];
                postZzxk4['cxbj'] = cour[3]
                time.sleep(5)  # 留出时间间隔，不抢别人换的课
                resZzxk4 = s.post(urlZzxk4, data=postZzxk4, headers=headers)
                pass  # 可在此调用打印日志，发送邮件，发送选课请求的函数
                pass  # 如果找到课就结束，在此return,否则继续循环查找
                print("发现有余量课程！已自动发送选课请求")
                print("课程信息如下：")
                print(cour[5], cour[6], cour[7], cour[8], cour[9], optList[cour[0]]['yxzrs'])
                print("请用浏览器登录教务系统确认是否选课成功！")
                return
                # if kklxdm != '01':
                #    return
        print("未查询到，稍后将重试", str(time.time()))
        time.sleep(interval + random.randint(0, rantim))


def REPEATrefreshCourList(rwlx, xkly, kklxdm, xklc, interval, rantim, maxtimes):
    # 主修课依次传入'1','1','01',校选课依次传入2,0,10，体育课依次传入2,0,05，均为str型
    isSound = input("发现课程后是否需要声音提示，Y/N\n")
    if isSound == 'Y':
        print("10秒钟后试听提示音")
        time.sleep(10)
        print("现在开始试音")
        for sounds in range(0, 3):
            winsound.Beep(2500, 2000)
            time.sleep(1)
        print("试音结束")
    time.sleep(3)
    urlZzxk2 = "http://jwxt2018.gxu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su=" + REALID
    getInnerCourListRes = getInnerCourList(rwlx, xkly, kklxdm)
    innerCourList = getInnerCourListRes[0]
    postZzxk2 = getInnerCourListRes[1]
    headersZzxk2 = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '305',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Host': 'jwxt2018.gxu.edu.cn',
        'Origin': 'http://jwxt2018.gxu.edu.cn',
        'Referer': 'http://jwxt2018.gxu.edu.cn/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su=' + REALID,
        'X-Requested-With': 'XMLHttpRequest'}
    for i in range(0, maxtimes):
        print("正在进行第", str(i + 1), "次查询有无余量课程", str(time.time()))
        resZzxk2 = s.post(urlZzxk2, data=postZzxk2, headers=headersZzxk2)
        optList = json.loads(resZzxk2.text)["tmpList"]
        for cour in innerCourList:
            if optList[cour[0]]['yxzrs'] != cour[6]:
                pass  # 可在此调用打印日志，发送邮件
                print("发现有余量课程！" + str(time.time()))
                print(cour[5], cour[6], cour[7], cour[8], cour[9], optList[cour[0]]['yxzrs'])
                if isSound == 'Y':
                    for sounds in range(0, 30):
                        winsound.Beep(2500, 2000)  # 第一个参数是频率Hz,第二个是鸣的时间毫秒
                        time.sleep(1)
                return
                # if kklxdm != '01':
                #    return
        print("未查询到，稍后将重试", str(time.time()))
        time.sleep(interval + random.randint(0, rantim))


import requests, bs4, time, rsa, base64, re, json, copy, random, winsound

REALID = input("请输入学号：\n")
REALPW = input("请输入密码：\n")
urlLogin = "http://jwxt2018.gxu.edu.cn/jwglxt/xtgl/login_slogin.html"
headers = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"}
s = requests.session()
res0 = s.get(urlLogin)
htm = bs4.BeautifulSoup(res0.text, "html.parser")
csrftoken = htm.select("#csrftoken")[0]["value"]
resPub = s.get("http://jwxt2018.gxu.edu.cn/jwglxt/xtgl/login_getPublicKey.html")
htmPub = bs4.BeautifulSoup(resPub.text, "html.parser")
modulus = re.findall('.*"modulus":"(.*)","exponent":"(.*)".*', htmPub.getText())[0][0]
exponent = re.findall('.*"modulus":"(.*)","exponent":"(.*)".*', htmPub.getText())[0][1]
b_mod = base64.b64decode(modulus)
b_exp = base64.b64decode(exponent)
d_mod = int.from_bytes(b_mod, 'big')
d_exp = int.from_bytes(b_exp, 'big')
PW_key = rsa.PublicKey(d_mod, d_exp)
b_PW = bytes(REALPW, "utf-8")
RSA_PW = base64.b64encode(rsa.encrypt(b_PW, PW_key))
postdata = {"csrftoken": csrftoken, "yhm": REALID, "mm": RSA_PW, "mm": RSA_PW}
res0 = s.post(urlLogin, data=postdata, headers=headers)
htm0 = bs4.BeautifulSoup(res0.text, "html.parser")
if re.findall("用户名或密码错误|不正确", htm0.getText()):
    print("用户名或密码错误")
    input()
    exit()
else:
    print("登录成功")
print("选课提醒20_", '自动选课2A_', '主修课2_1', '校选课2_2', '体育课2_3', '退出0')
while True:
    mainOpt = input("请输入选项：\n")
    if mainOpt == '0':
        break
    elif mainOpt[0] == '2':
        mainXklc = '3'  # 这里按说应该输入选课轮次
        mainInterval = int(input("请设置刷新固定间隔时间/秒：最少10\n"))
        mainRantim = int(input("请设置刷新随机间隔时间/秒：最少20\n"))
        mainMaxtimes = int(input("请设置最大查询次数：最多20000\n"))
        if mainInterval < 10:
            mainInterval = 10
        if mainRantim < 20:
            mainRantim = 20
        if mainMaxtimes > 20000:
            mainMaxtimes = 20000
        if mainOpt[1] == '0':
            if mainOpt[2] == '1':
                REPEATrefreshCourList('1', '1', '01', mainXklc, mainInterval, mainRantim, mainMaxtimes)
            if mainOpt[2] == '2':
                REPEATrefreshCourList('2', '0', '10', mainXklc, mainInterval, mainRantim, mainMaxtimes)
            if mainOpt[2] == '3':
                REPEATrefreshCourList('2', '0', '05', mainXklc, mainInterval, mainRantim, mainMaxtimes)
        if mainOpt[1] == 'A':
            if mainOpt[2] == '1':
                REPEAT_POST_CourList('1', '1', '01', mainXklc, mainInterval, mainRantim, mainMaxtimes)
            if mainOpt[2] == '2':
                REPEAT_POST_CourList('2', '0', '10', mainXklc, mainInterval, mainRantim, mainMaxtimes)
            if mainOpt[2] == '3':
                REPEAT_POST_CourList('2', '0', '05', mainXklc, mainInterval, mainRantim, mainMaxtimes)
    print("已回到主菜单")
s.close()
input("程序已退出")

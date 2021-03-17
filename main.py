# V1.4.2更新说明：20210219
# 换课抢课增加了退课后选课失败的处理方法
# 问题提示，Zzxk3获取不到结果多半是因为xkkz_id不对
def ScoreDetails(xnm, xqm):
    # 应传入str型参数，分别为学年名（如2019），学期名（3,12,16），如果查该学年所有学期，xqm为空可能可以
    urlScore = "http://"+host_server+"/jwglxt/cjcx/cjcx_cxXsKccjList.html?gnmkdm=N305007&su=" + REALID
    nowTime = str(int(time.time() * 1000))
    postScore = {'xnm': xnm,  # 学年名
                 'xqm': xqm,  # 后续需完善xqm，初步结论，一学年最多有三个学期，xqm分别为3,12,16
                 '_search': 'false',
                 'nd': nowTime,
                 'queryModel.showCount': '450',  # 获取的条数
                 'queryModel.currentPage': '1',
                 'queryModel.sortName': '',
                 'queryModel.sortOrder': 'asc',
                 'time': '1'}
    resScore = s.post(urlScore, data=postScore, headers=headers)
    # print(resScore.json)
    htmScore = bs4.BeautifulSoup(resScore.text, "html.parser")
    # print(str(htmScore))
    userScores = json.loads(resScore.text)  # 这是字典
    scoreList = userScores["items"]  # 这是列表
    if not scoreList:
        print("未获取到有关成绩！")
        return
    fileScoreDetailsName = "ScoreDetails" + xnm + "_" + xqm + ".txt"
    fileScoreDetails = open(fileScoreDetailsName, "w")
    fileScoreDetails.write("课程名称\t学分\t成绩分项\t成绩\n")
    xfSum = 0;
    scoreSum = 0
    for cour in scoreList:
        if cour['xmblmc'] == '总评':
            xfSum = xfSum + float(cour["xf"]);
            scoreSum = scoreSum + float(cour["xmcj"]) * float(cour["xf"])
        print(cour["kcmc"], cour["xf"], cour["xmblmc"], cour["xmcj"])
        fileScoreDetails.write(cour["kcmc"] + "\t" + cour["xf"] + "\t" + cour["xmblmc"] + "\t" + cour["xmcj"] + "\n")
        # 可能的含义解释，课程名称，学分，项目比例名称，项目成绩
    print("加权平均成绩：", scoreSum / xfSum)
    print("已输出所有成绩明细")
    fileScoreDetails.write("加权平均成绩：" + str(scoreSum / xfSum))
    fileScoreDetails.close()
    print('成绩明细已保存到' + fileScoreDetailsName)


def saveAllCoursesList(rwlx, xkly, kklxdm, isAllZxkc):
    if isAllZxkc == True:
        electCoursesRes0 = electCourses(rwlx, xkly, kklxdm, 'ALLzxkc')[0]  # zxkc,主修课程
    else:
        electCoursesRes0 = electCourses(rwlx, xkly, kklxdm)[0]
    fileAllCoursesListName = "Courses" + kklxdm + "_" + str(int(time.time())) + ".txt"
    fileAllCoursesList = open(fileAllCoursesListName, 'w')
    fileAllCoursesList.write("名称\t容量\t教师\t时间\t课程性质\t学分\t课程号\t已选人数\t教学地点\n")
    for co in electCoursesRes0:
        fileAllCoursesList.write(
            co[5] + "\t" + co[6] + "\t" + co[7] + "\t" + co[8] + "\t" + co[9] + "\t" + co[10] + "\t" + co[12] + "\t" +
            co[13] + '\t' + co[14] + "\n")  # 5 6 7 8 9 10 12 13 14
    print("已保存到文件")
    fileAllCoursesList.close()


def electCourses(rwlx, xkly, kklxdm, otherPars=''):
    # 主修课依次传入'1','1','01',校选课依次传入2,0,10，体育课依次传入2,0,05，均为str型
    # zzxk,自主选课
    print("正在初始化课程信息...,此过程可能需要较长时间", str(time.asctime()))
    urlZzxk = "http://"+host_server+"/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su=" + REALID
    resZzxk = s.get(urlZzxk, headers=headers)
    resZzxk.encoding = resZzxk.apparent_encoding
    """
    try:
        if kklxdm=="01":
            xkkz_id=re.search(r"\(this,'01','(.*?)'",resZzxk.text).group(1)#主修
        if kklxdm=="10":
            xkkz_id=re.search(r"\(this,'10','(.*?)'",resZzxk.text).group(1)#通识选修
        if kklxdm=="05":
            xkkz_id=re.search(r"\(this,'05','(.*?)'",resZzxk.text).group(1)#体育
    except:
        print(resZzxk.text)
    """
    # xkkz_id以后多个环节都要用
    """正方系统奇怪的改动，xkkz_id不保存在上面的正则表达式里了，也就是上面的try语句块匹配不到xkkz_id了
        下面又莫名多了几个name为firstKklxdm，firstXkkzId，firstNjdmId,firstZyhId的input，
        把xkkz_id存在hidden的input里
        """
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
    xkkz_id = re.search(r'<input.*?id="xkkz_id".*?value="(.*?)"/>', resZzxk.text).group(1)
    if kklxdm=="10":
        xkkz_id=re.search(r"\(this,'10','(.*?)'",resZzxk.text).group(1)#通识选修
    elif kklxdm=="05":
        xkkz_id=re.search(r"\(this,'05','(.*?)'",resZzxk.text).group(1)
    elif kklxdm=="01":
        xkkz_id=re.search(r"\(this,'01','(.*?)'",resZzxk.text).group(1)
    print(resZzxk.text)
    print(xkkz_id)
    print(re.search(r'<input.*?id="xkkz_id".*?value="(.*?)"/>', resZzxk.text))
    # sfkknj=sfkkzy='1'，#要获取所有专业的主修课程，这两个必须是1

    jspage = '400'  # jspage,和浏览器提交的数据不符,早期版本填的是200一般够用，一次性获取所有专业主修课程至少要1480
    sfkknj = sfkkzy = sfznkx = zdkxms = sfkxq = sfkcfx = kkbk = kkbkdj = sfkgbcx = sfrxtgkcxd = tykczgxdcs = "0"
    if (otherPars == 'ALLzxkc'):  # zxkc,主修课程
        sfkknj = sfkkzy = '1'
        jspage = '1800'
    xkxnm = re.search(r'<input.*?id="xkxnm".*?value="(.*?)"/>', resZzxk.text).group(1)
    xkxqm = re.search(r'<input.*?id="xkxqm".*?value="(.*?)"/>', resZzxk.text).group(1)
    rlkz = "0"
    jxbzb = ""
    # 由于未知的原因，bs4解析html会丢失hidden的<input>，被迫采用正则表达式获取数据

    # 主修课、通识选修、体育课的rwlx,xkly,kklxdm不一样
    # 主修课程rwlx为1，通识选修课、体育分项为2
    # xkly主修为1，通识选修、体育为0
    # kklxdm主修01，通识选修10，体育05
    urlZzxk2 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su=" + REALID
    postZzxk2 = {'rwlx': rwlx, 'xkly': xkly, 'bklx_id': bklx_id, 'xqh_id': xqh_id,
                 'jg_id': jg_id, 'zyh_id': zyh_id, 'zyfx_id': zyfx_id, 'njdm_id': njdm_id,
                 'bh_id': bh_id, 'xbm': xbm, 'xslbdm': xslbdm, 'ccdm': ccdm, 'xsbj': xsbj,
                 'sfkknj': sfkknj, 'sfkkzy': sfkkzy, 'sfznkx': sfznkx, 'zdkxms': zdkxms,
                 'sfkxq': sfkxq, 'sfkcfx': sfkcfx, 'kkbk': kkbk, 'kkbkdj': kkbkdj,
                 'sfkgbcx': sfkgbcx, 'sfrxtgkcxd': sfrxtgkcxd, 'tykczgxdcs': tykczgxdcs,
                 'xkxnm': xkxnm, 'xkxqm': xkxqm, 'kklxdm': kklxdm, 'rlkz': rlkz,
                 'kspage': '1', 'jspage': jspage, 'jxbzb': jxbzb
                 }

    headersZzxk2 = {
        "User-Agent": UA_headers,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '305',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Host': host_server,
        'Origin': 'http://'+host_server,
        'Referer': 'http://'+host_server+'/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su='+REALID,
        'X-Requested-With': 'XMLHttpRequest'}
    resZzxk2 = s.post(urlZzxk2, data=postZzxk2, headers=headersZzxk2)
    # print(resZzxk2.text)
    # htmZzxk2=bs4.BeautifulSoup(resZzxk2.text,"html.parser")
    optList = json.loads(resZzxk2.text)["tmpList"]
    # print(optList)
    urlZzxk3 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzbjk_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su=" + REALID
    if kklxdm=='10':
        urlZzxk3="http://"+host_server+"/jwglxt/xsxk/zzxkyzbjk_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su=" + REALID
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
                    'Host': host_server,
                    'Origin': 'http://'+host_server,
                    'Referer': 'http://'+host_server+'/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su='+REALID,
                    'User-Agent': UA_headers,
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
            time.sleep(1 + (random.randint(0, 300)) / 100)
            # time.sleep(0.5+(random.randint(0,200))/100)
            print(postZzxk3)
            resZzxk3 = s.post(urlZzxk3, data=postZzxk3, headers=headersZzxk3,timeout=None)
            print(urlZzxk3)
            print(headersZzxk3)
            print(resZzxk3.text)
            i = 0
            aCour = json.loads(resZzxk3.text)[0]
        else:
            i = i + 1
            aCour = json.loads(resZzxk3.text)[i]
        # print(resZzxk3.text)
        allCourList.append([optList.index(opt), i, kch_id, cxbj, fxbj, courName, aCour["jxbrl"], \
                            aCour["jsxx"].replace("<br/>", ",").split('/')[1], aCour["sksj"].replace("<br/>", ","),
                            aCour["kcxzmc"], courCred, xxkbj, kch, \
                            opt['yxzrs'], aCour['jxdd'].replace("<br/>", ",")])  # 0-6,7-12,13-14
        # 13,这是新加的yxzrs，仅供saveAllCoursesList函数使用，如有问题请删去
        # 14,教学地点
    # print(className,aCour["jsxx"].replace("<br/>",","),aCour["sksj"].replace("<br/>",","),aCour["jxdd"].replace("<br/>",","),aCour["kcxzmc"],chosenNum,aCour["jxbrl"],courCred)
    # fileElectCourses.write(className+"\t"+aCour["jsxx"].replace("<br/>",",")+"\t"+aCour["sksj"].replace("<br/>",",")+"\t"+aCour["jxdd"].replace("<br/>",",")+"\t"+aCour["kcxzmc"]+"\t"+chosenNum+"/"+aCour["jxbrl"]+"\t"+courCred+"\n")
    print("初始化课程信息完成", str(time.asctime()))
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
        print("警告：请检查selCourRules01/05/10.txt文件设置的选课信息是否正确,否则请立即终止程序，并删除该文件")
        isContinue = input("如果检查无误继续，输入Y:")
        if isContinue != 'Y':
            resList = []
        time.sleep(5)
        return resList
    except FileNotFoundError:
        file = open(fileName, 'w')
    print("请输入选课志愿表，排在前面的志愿将先被选择")
    print("每次只能输入一个课程名称，其他信息可以输入多项，以空格分隔")
    print("输入时间时注意：格式示例：星期日第3-4节，*号为同上号")
    print("如果您已经填写完志愿表，请在输入课程名称的时候输入#号")
    i = 1
    while True:
        print("这是您的第", str(i), "志愿：")
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
    print("正在处理选课志愿信息...")
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
    print("处理完成")
    return (resList, electCoursesRes[1], electCoursesRes[2])  # 第二个返回的是postZzxk2


def REPEAT_POST_CourList(rwlx, xkly, kklxdm, xklc, interval, rantim, maxtimes):
    # 前三个参数：主修课依次传入'1','1','01',校选课依次传入2,0,10，体育课依次传入2,0,05，均为str型
    # 第四个参数xklc，可能是选课轮次，要求用户输入,str型
    # 第5,6个参数interval，重复刷新等待的固定时长，rantim,随机等待时长，单位秒，均为int型
    # 第7个参数maxtimes，最大查询次数，int
    time.sleep(3)
    print("如果查询到有余量的课程将自动提交选课！")
    urlZzxk2 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su=" + REALID
    urlZzxk3 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzbjk_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su=" + REALID
    urlZzxk4 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzb_xkBcZyZzxkYzb.html?gnmkdm=N253512&su=" + REALID
    getInnerCourListRes = getInnerCourList(rwlx, xkly, kklxdm)
    postZzxk2 = getInnerCourListRes[1]
    postZzxk3 = getInnerCourListRes[2]
    innerCourList = getInnerCourListRes[0]
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
        print("正在进行第", str(i + 1), "次查询有无余量课程", str(time.asctime()))
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
                resZzxk4 = s.post(urlZzxk4, data=postZzxk4, headers=headers)
                pass  # 可在此调用打印日志，发送邮件，发送选课请求的函数
                pass  # 如果找到课就结束，在此return,否则继续循环查找
                print("发现有余量课程！")
                print("选课请求已经自动发送", str(time.asctime()))
                print(cour[5], cour[6], cour[7], cour[8], cour[9], optList[cour[0]]['yxzrs'])
                print("请用浏览器登录教务系统确认是否选课成功！")
                if kklxdm != '01':
                    return
        print("未查询到，稍后将重试", str(time.asctime()))
        time.sleep(interval + random.randint(0, rantim))


def CHANGE_Course(rwlx, xkly, kklxdm, xklc, interval, rantim, maxtimes):
    import winsound
    print("发现有余量课程后，将会先退掉现有的课，再选新的课")
    print("由于网络延迟等原因，可能出现退课后选不上新的课的情况，请理解")
    time.sleep(1)
    urlZzxk2 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su=" + REALID
    urlZzxk3 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzbjk_cxJxbWithKchZzxkYzb.html?gnmkdm=N253512&su=" + REALID
    urlZzxk4 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzb_xkBcZyZzxkYzb.html?gnmkdm=N253512&su=" + REALID
    urlTui1 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzb_xkJcInXksjZzxkYzb.html?gnmkdm=N253512&su=" + REALID
    urlTui2 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzb_tuikBcZzxkYzb.html?gnmkdm=N253512&su=" + REALID
    urlTui3 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzb_xkBcZypxZzxkYzb.html?gnmkdm=N253512&su=" + REALID
    getInnerCourListRes = getInnerCourList(rwlx, xkly, kklxdm)
    postZzxk2 = getInnerCourListRes[1]
    postZzxk3 = getInnerCourListRes[2]
    quitCourName = input("请输入要退掉的课的全名\n")
    quitCourClassName=input("请输入要退掉的课的【教学班名称】\n")
    resZzxk2 = s.post(urlZzxk2, data=postZzxk2, headers=headers)
    findQuitCourList = json.loads(resZzxk2.text)["tmpList"]
    for findQuitCour in findQuitCourList:
        if findQuitCour['kcmc'] == quitCourName and findQuitCour['jxbmc']==quitCourClassName:
            postZzxk3['kch_id'] = findQuitCour['kch_id']
            postZzxk3['cxbj'] = findQuitCour['cxbj']
            postZzxk3['fxbj'] = findQuitCour['fxbj']
            quit_jxb_id=findQuitCour['jxb_id']
            quitCourKchNameXf = "(" + findQuitCour['kch'] + ")" + findQuitCour['kcmc'] + " - " + findQuitCour[
                'xf'] + " 学分"
            oldxxkbj=findQuitCour['xxkbj']
            break
    time.sleep(1)
    resZzxk3 = s.post(urlZzxk3, data=postZzxk3, headers=headers)
    #aQuitCour = json.loads(resZzxk3.text)[0]
    aQuitCour=''
    for aClass in json.loads(resZzxk3.text):
        if aClass['jxb_id']==quit_jxb_id:
            if aQuitCour=='':
                aQuitCour=aClass
            else:
                print("ERROR: jxb_id重复，请立即终止程序！")
                time.sleep(1000)
    postTui1 = {'xkkz_id': postZzxk3['xkkz_id'], 'kch_id': postZzxk3['kch_id'],
                'xnm': postZzxk3['xkxnm'], 'xqm': postZzxk3['xkxqm'],  # 变量名不完全一样但应该也行
                'jxb_id': aQuitCour['do_jxb_id']
                }
    postTui2 = {'kch_id': postZzxk3['kch_id'], 'kcmc': quitCourKchNameXf, 'rwlx': rwlx, 'rlkz': postZzxk3['rlkz'],
                'xklc': xklc,
                'xkxnm': postZzxk3['xkxnm'], 'xkxqm': postZzxk3['xkxqm'],
                'jxb_ids': aQuitCour['do_jxb_id'],  # 和Tui1的jxb_id是一样的
                'rlzlkz': '1', 'txbsfrl': '0'  # 这两个在已有信息中没找到,静态数据，可能不对
                }
    postTui3 = {'zypxs': '', 'jxb_ids': ''}
    print("如果发现选课志愿单上的课程有余量，将退掉您已选的以下课程：是否继续？")
    print(quitCourKchNameXf, aQuitCour['sksj'], aQuitCour['jsxx'])
    isContinue = input("继续请输入Y，否则退出\n")
    if isContinue != 'Y':
        return
    time.sleep(3)
    innerCourList = getInnerCourListRes[0]
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
    postZzxk4Old=copy.deepcopy(postZzxk4)
    postZzxk4Old['kcmc']=quitCourName
    postZzxk4Old['xxkbj']=oldxxkbj
    postZzxk4Old['cxbj']=postZzxk3['cxbj']
    postZzxk4Old['kch_id']=postZzxk3['kch_id']
    postZzxk4Old['jxb_ids']=aQuitCour['do_jxb_id']
    stateCode=1
    for i in range(0, maxtimes):
        print("正在进行第", str(i + 1), "次查询有无余量课程", str(time.asctime()))
        resZzxk2 = s.post(urlZzxk2, data=postZzxk2, headers=headers)
        optList = json.loads(resZzxk2.text)["tmpList"]
        for cour in innerCourList:
            if optList[cour[0]]['yxzrs'] != cour[6]:
                # ------------以下是操作退课-------------
                s.post(urlTui1, data=postTui1, headers=headers)
                s.post(urlTui2, data=postTui2, headers=headers)
                resTui3=s.post(urlTui3, data=postTui3, headers=headers)
                # ----------以下是发送选课请求-----------
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
                #破坏性测试1，无法选新课，判断是否会选回旧课
                #postZzxk4={}
                #破坏性测试2，旧课已退，新课旧课都无法选，判断是否会提示
                #postZzxk4Old={}
                resZzxk4 = s.post(urlZzxk4, data=postZzxk4, headers=headers)
                #print(resTui3.text)
                #print(resZzxk4.text)
                if resTui3.text=='"success"' and json.loads(resZzxk4.text)['flag']!='1':
                    #退课成功，选课失败
                    #尝试选回刚才退掉的课
                    resZzxk4Old=s.post(urlZzxk4,data=postZzxk4Old,headers=headers)
                    #print(resZzxk4Old.text)
                    if json.loads(resZzxk4Old.text)['flag']!='1':
                        #如果尝试选回刚才退掉的课失败，再试一次
                        resZzxk4Old = s.post(urlZzxk4, data=postZzxk4Old, headers=headers)
                    if json.loads(resZzxk4Old.text)['flag']!='1':
                        #如果依然选课失败，记录状态码-1
                        stateCode=-1#原来的课被退了，新课没有选上
                    else:
                        #原来的课被退了，新课没有选上，又把原来的课选回来了
                        stateCode=0

                if stateCode==0:
                    stateCode=1
                    continue
                    #马上选回了自己刚退的课，等于什么也没发生
                elif stateCode==-1:
                    emailBody="退课成功！选课失败！请立即登录教务系统手动处理"
                    sendAnEmail(recipientEmail, '退课成功！选课失败', emailBody)
                    print("！！！非常抱歉地通知您，您的原有课程被退掉，新课程选课失败，且无法再选回原有课程，请立即登录教务系统检查")
                else:
                    emailBody = "您原有的课程 --" + quitCourKchNameXf + aQuitCour['sksj'] + aQuitCour['jsxx'] + "-- 已被退掉\n" \
                            + "发现新的有余量课程" + cour[5] + cour[6] + cour[7] + cour[8] + cour[9] + optList[cour[0]]['yxzrs'] \
                            + "\n已经尝试为您发送新的选课请求，请立即登录教务系统检查！"
                    sendAnEmail(recipientEmail, '原有课程已经退掉！请立即检查！', emailBody)
                    print("发现有余量课程！\n原有课程已经退掉，选课请求已经自动发送", str(time.asctime()))
                    print(cour[5], cour[6], cour[7], cour[8], cour[9], optList[cour[0]]['yxzrs'])
                    print("请用浏览器登录教务系统确认是否选课成功！")
                winsound.Beep(2000, 90000)
                return
                # if kklxdm != '01':#这里处理主修课程选课的时候可能有问题，会不停循环发送选课请求，建议择期连其他几个类似的函数一并处理
                #   return
        print("未查询到，稍后将重试", str(time.asctime()))
        time.sleep(interval + random.randint(0, rantim))


def REPEATrefreshCourList(rwlx, xkly, kklxdm, xklc, interval, rantim, maxtimes):
    # 主修课依次传入'1','1','01',校选课依次传入2,0,10，体育课依次传入2,0,05，均为str型
    import winsound
    time.sleep(3)
    urlZzxk2 = "http://"+host_server+"/jwglxt/xsxk/zzxkyzb_cxZzxkYzbPartDisplay.html?gnmkdm=N253512&su=" + REALID
    getInnerCourListRes = getInnerCourList(rwlx, xkly, kklxdm)
    innerCourList = getInnerCourListRes[0]
    postZzxk2 = getInnerCourListRes[1]
    headersZzxk2 = {
        "User-Agent": UA_headers,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '305',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Host': host_server,
        'Origin': 'http://'+host_server,
        'Referer': 'http://'+host_server+'/jwglxt/xsxk/zzxkyzb_cxZzxkYzbIndex.html?gnmkdm=N253512&layout=default&su='+REALID,
        'X-Requested-With': 'XMLHttpRequest'}
    for i in range(0, maxtimes):
        print("正在进行第", str(i + 1), "次查询有无余量课程", str(time.asctime()))
        resZzxk2 = s.post(urlZzxk2, data=postZzxk2, headers=headersZzxk2)
        optList = json.loads(resZzxk2.text)["tmpList"]
        for cour in innerCourList:
            if optList[cour[0]]['yxzrs'] != cour[6]:
                pass  # 可在此调用打印日志，发送邮件
                sendAnEmail(recipientEmail, '发现有余量课程！',
                            cour[5] + cour[6] + cour[7] + cour[8] + cour[9] + optList[cour[0]]['yxzrs'])
                print("发现有余量课程！" + str(time.asctime()))
                print(cour[5], cour[6], cour[7], cour[8], cour[9], optList[cour[0]]['yxzrs'])
                for sounds in range(0, 20):
                    winsound.Beep(2500, 2500)  # 第一个参数是频率Hz,第二个是鸣的时间毫秒
                    time.sleep(1.5)
                if kklxdm != '01':
                    return
        print("未查询到，稍后将重试", str(time.asctime()))
        time.sleep(interval + random.randint(0, rantim))


def sendAnEmail(recipient, subject, body):
    import smtplib
    myEmail = "sender@example.com"
    PASSWORD = "password"
    from_ = "From:Sender Name<sender@example.com>\n"
    to = "To:recipient<" + recipient + ">\n"
    subject = "Subject:" + subject + "\n"
    message = from_ + to + subject + "\n" + body
    smtpobj = smtplib.SMTP("smtp.example.com", 25)
    smtpobj.ehlo()
    smtpobj.starttls()
    try:
        smtpobj.login(myEmail, PASSWORD)
    except:
        print("SMTP登录错误！")
    return smtpobj.sendmail(myEmail, recipient, message.encode())


import requests, bs4, time, rsa, base64, re, json, copy, random, getpass

recipientEmail='recipient@example.com'
UA_headers="User-Agent Example"
host_server='jiaowuxitong.example.edu'
print("V1.4.2")
REALID = input("请输入学号：\n")
# REALPW=input("请输入密码：\n")
REALPW = getpass.getpass()
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
urlLogin = "http://"+host_server+"/jwglxt/xtgl/login_slogin.html"
headers = {
    "User-Agent": UA_headers}
s = requests.session()
res0 = s.get(urlLogin)
htm = bs4.BeautifulSoup(res0.text, "html.parser")
csrftoken = htm.select("#csrftoken")[0]["value"]
resPub = s.get("http://"+host_server+"/jwglxt/xtgl/login_getPublicKey.html")
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
res0 = s.post(urlLogin, data=postdata, headers=headers,timeout=None)
htm0 = bs4.BeautifulSoup(res0.text, "html.parser")
if re.findall("用户名或密码错误|不正确", htm0.getText()):
    print("用户名或密码错误")
    input()
    exit()
else:
    print("登录成功")
print("成绩查询1", "选课提醒20_", '自动选课2A_', '换课抢课2T_', '主修课2_1', '校选课2_2', '体育课2_3', '获取课程列表2L_','所有主修课2L1a', '退出0')
print("在下划线处填入数字或字母")
while True:
    mainOpt = input("请输入选项：\n")
    if mainOpt == '0':
        break
    elif mainOpt == '1':
        mainXnm = input("请输入学年名：\n")
        mainXqm = input("请输入学期名：\n")
        mainXqmDic = {'1': '3', '2': '12', '3': '16'}
        mainXqm = mainXqmDic[mainXqm]
        ScoreDetails(mainXnm, mainXqm)
    elif mainOpt[0] == '2':
        mainXklc = input("请输入选课轮次：\n")
        mainInterval = int(input("请设置刷新固定间隔时间：\n"))
        mainRantim = int(input("请设置刷新随机间隔时间：\n"))
        mainMaxtimes = int(input("请设置最大查询次数：\n"))
        if mainInterval < 100:
            mainInterval = 100
        if mainRantim < 500:
            mainRantim = 500
        if mainMaxtimes > 5:
            mainMaxtimes = 5
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
        if mainOpt[1] == 'T':
            if mainOpt[2] == '1':
                CHANGE_Course('1', '1', '01', mainXklc, mainInterval, mainRantim, mainMaxtimes)
            if mainOpt[2] == '2':
                CHANGE_Course('2', '0', '10', mainXklc, mainInterval, mainRantim, mainMaxtimes)
            if mainOpt[2] == '3':
                CHANGE_Course('2', '0', '05', mainXklc, mainInterval, mainRantim, mainMaxtimes)
        if mainOpt[1] == 'L':
            if len(mainOpt)==4 and mainOpt[3]=='a':
                isAllZxkc=True
            else:
                isAllZxkc=False
            if mainOpt[2] == '1':
                saveAllCoursesList('1', '1', '01', isAllZxkc)
                # saveAllCoursesList('1','1','01','2L13')
            if mainOpt[2] == '2':
                saveAllCoursesList('2', '0', '10', isAllZxkc)
            if mainOpt[2] == '3':
                saveAllCoursesList('2', '0', '05', isAllZxkc)
    print("已回到主菜单")
s.close()
input("程序已退出")

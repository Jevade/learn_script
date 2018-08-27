# coding=utf-8
"""

@author: liujiawei (Sy1507518),hanxu (Sy1507522)
@license: GPL
@contact: hanxubuaa11107@gmail.com,liujiawei0524@buaa.edu.com
@see: http://blog.csdn.net/largetalk/article/details/6950435

@version: 3.1.1
@todo[0.0.2]: StockMarketSys

@note: a comment
@attention: please attention
@bug: a exist bug
@warning: warnings
"""

import sqlite3, random, threading, time, thread
import numpy as np
from Tkinter import *
from tkMessageBox import askokcancel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class User:
    """
    @Class describe：  用户类、属于事务管理层。包含所有当前用户操作,直接与表现层链接
    @private param:     __username              用户名
                        __balance               余额
                        __totalProperty         总资产
                        __profit                盈亏
                        __stockProperty         当前用户股票资产
                        __originalProperty      用户本金
    """
    __username = ''
    __balance = 10000
    __totalProperty = 10000
    __profit = 0
    __stockProperty = 0  #
    __originalProperty = 10000  # 用户本金

    def __init__(self, name):
        self.__username = name

    def calBalance(self):
        """查询返回用户余额"""
        db = Database('testDB.db', self.__username)
        db.getLinkedUser(self.__username)
        temp = db.getUserCurrentmoney()
        return temp

    def calToatalProperty(self):
        """查询返回用户总资产"""
        db = Database('testDB.db', self.__username)
        db.getLinkedUser(self.__username)
        temp = db.getUserCurrentprop()
        return temp

    def calPrfLoss(self):
        """查询返回当前利润"""
        return self.calToatalProperty() - self.__originalProperty

    def calStockProp(self):
        """查询返回用户股票资产"""
        db = Database('testDB.db', self.__username)
        db.getLinkedUser(self.__username)
        temp = db.getUserStockprop()
        return temp

    def update(self):
        self.__balance = self.calBalance()
        self.__totalProperty = self.calToatalProperty()
        self.__profit = self.calPrfLoss()
        self.__stockProperty = self.calStockProp()
        return True

    def buyOneStock(self, stockname, stocknum):
        """买入一支股票
            :param stockname:   购买股票名称
            :param stocknum:    购买数量
            :return:            BOOL
            """
        db = Database('testDB.db', self.__username)
        money = stocknum * db.getStockPrice(stockname)
        flag1 = (bool)(db.getUserCurrentmoney() > money)
        flag2 = (bool)(db.getStockBalance(stockname) > stocknum)

        if flag1 and flag2:
            db.changeUserStocknum(self.__username, stockname, stocknum)
            db.changeStockBalance(stockname, -stocknum)
            db.changeUserCurrentmoney(-money)
            return True
        else:
            return False

    def sellOneStock(self, stockname, stocknum):
        """卖出一支股票
                :param stockname:   购买股票名称
                :param stocknum:    购买数量
                :return:            BOOL
                """
        db = Database('testDB.db', self.__username)
        money = stocknum * db.getStockPrice(stockname)
        if (bool)(db.getUserStocknum(self.__username, stockname) > stocknum):
            db.changeUserStocknum(self.__username, stockname, stocknum)
            db.changeStockBalance(stockname, -stocknum)
            db.changeUserCurrentmoney(-money)
            return True
        else:
            return False

    def getUsername(self):
        """
        :return:    string用户名
        """
        self.update()
        return self.__username

    def getBalance(self):
        """
        :return:    float用户现金余额
        """
        self.update()
        db = Database('testDB.db', self.__username)
        self.__balance = db.getUserCurrentmoney()
        return self.__balance

    def getTotalProperty(self):
        """
        :return:    float用户现有总资产
        """
        self.update()
        return self.__totalProperty

    def getProfitOrLoss(self):
        """
        :return:    float用户总资产盈亏
        """
        self.update()
        return round(self.__profit, 2)

    def getStockProp(self):
        """
        :return:    float用户股票总额
        """
        self.update()
        return self.__stockProperty

    def drawUserExchange(self, figure):
        """
        用于在屏幕上显示用户持有的股票数量，显示方式为直方图图
        :param figure:  Figure
        :return:
        """
        db = Database('testDB.db', self.__username)
        stocknamelist = db.getStocknameList()
        userstocknumlist = db.getUserStocknnumlist(self.__username)

        width = 0.5
        a = figure.add_subplot(111)
        ind = np.arange(1, len(stocknamelist) + 1, 1)
        a.cla()
        a.bar(ind - width / 2, userstocknumlist, width, color='green')
        a.set_xticks(ind)
        a.set_xticklabels(stocknamelist)
        a.set_ylabel('Stock Num')
        a.set_xlabel('Stock ID')
        a.set_ylabel('Stock Num')

    def getStockholdingMsg(self):
        """
        :return:    string 用户所有股票数量信息
        """
        db = Database('testDB.db', self.__username)
        return db.getUserStockholdingStr(self.__username)


class Stock():
    """
    @Class describe：  股票类、属于事务管理层。包含所有股票市场的操作,直接与表现层链接
    @private param:    __username  用户名
    """
    __username = ''

    def __init__(self, username):
        self.__username = username
        return

    def showStockprice(self, f):
        """
        在屏幕上用柱状图的形式显示所有股票信息价格，包含了股票价格浮动功能,并且按照股价顺序列出各项股票
        :param f:   Figure
        :return:
        """

        """
        按照股价顺序排列各个股票
        """
        db = Database('testDB.db', '')
        self.floatStock()
        stockpricelist = []
        stocknamelist = []
        dict2 = sorted(dict(zip(db.getStocknameList(), db.getStockpriceList())).iteritems(), key=lambda d: d[1],
                       reverse=True)
        for i in range(len(dict2)):
            stockpricelist.append(dict2[i][1])
            stocknamelist.append(dict2[i][0])

        a = f.add_subplot(111)
        ind = np.arange(1, len(stocknamelist) + 1, 1)
        width = 0.5
        a.cla()
        a.bar(ind - width / 2, stockpricelist, width, color='green')
        a.set_xticks(ind)
        a.set_xticklabels(stocknamelist)
        a.set_xlabel(u'Stock ID')
        a.set_ylabel(u'Stock Price')

        return True

    def floatStock(self):
        """
        对股票市场进行价格浮动，10%以内上下随机浮动
        :return:    Bool
        """
        db = Database('testDB.db', '')
        stocknamelist = db.getStocknameList()
        for n in stocknamelist:
            temp = random.uniform(random.uniform(90, 110), random.uniform(90, 110)) / 100
            price1 = ((float)(db.getStockPrice(n)))
            price = round(price1 * temp, 2)
            a = db.changeStockPrice(n, price)
        return True

    def addNewstock(self, stockname, stockprice, stocknum):
        """
        在股票市场增加一支股票
        :param stockname:   股票名称
        :param stockprice:  股票价格
        :param stocknum:    股票总数量
        :return:            Bool
        """

        db = Database('testDB.db', '')
        stocknamelist = db.getStocknameList()
        if stockname in stocknamelist:
            return False
        else:
            stocknamelist.append(stockname)
        db.addnewstock(stockname, stockprice, stocknum)
        return True

    def initStock(self):
        """
        用户股票数清零
        :param :   None
        :return:   None
        """
        db = Database('testDB.db', self.__username)
        db.initStock()

    def deleteStock(self, stockName):
        """
        在股票市场减少一支股票
        :param stockname:   股票名称
        :return:            Bool
        """

        db = Database('testDB.db', '')
        stocknamelist = db.getStocknameList()
        if stockName not in stocknamelist:
            return False
        else:
            db.deleteStock(stockName)
        return True

    def getStockPrice(self, stockName):
        """
        获取指定股票的价格
        :param :   stockName
        :return:
        """
        db = Database('testDB.db', '')
        value = db.getStockPrice(stockName)
        return value

    def getStockNum(self, stockName):
        """
        获取指定股票的市场存量
        :param :   stockName
        :return:
        """
        db = Database('testDB.db', '')
        value = db.getStockCurrentnum(stockName)
        return value


class Database():
    """
    @Class describe：    数据库操作类、属于数据管理层。包含所有数据库相关操作,与事务处理层连接链接
    @private param:     __DBname        数据库名称，统一为testDB.db
                        __username      用户名
                        conn = sqlite3.connect('')  数据库链接参数
                        curs = conn.cursor()        数据库链接参数
                        sql = ''                    数据库交互sql语句
    """
    DBname = ''
    __username = ''  # 测试专用
    conn = sqlite3.connect('')
    curs = conn.cursor()
    sql = ''

    def __init__(self, DBname, username):
        """类的初始化操作，包括链接DataBase，赋值等
        :param stockname:   数据库名称，股票名称
        :return:            float股票价格
        """
        self.DBname = DBname
        self.__username = username
        self.conn = sqlite3.connect(self.DBname)
        self.curs = self.conn.cursor()
        return

    def getLinkedStockprice(self):
        """
        链接到stockprice
        :return:
        """
        self.conn = sqlite3.connect('testDB.db')
        self.curs = self.conn.cursor()

    def getStockPrice(self, stockname):
        """
        链接stockprice表，获取某支股票价格
        :param stockname:   股票名称
        :return:            float股票价格
        """
        self.getLinkedStockprice()
        stockprice = 0.0
        sql = 'SELECT * FROM stockPri WHERE stock=? '
        self.curs.execute(sql, (stockname,))
        self.conn.commit()
        value = self.curs.fetchall()

        stockprice += value[0][1]
        self.closeDatabase()
        return round(stockprice, 2)

    def getStockTotalnum(self, stockname):
        """
        链接stockprice表，获取某支股票发行总数
        :param stockname:   股票名称
        :return:            int股票数量
        """
        self.getLinkedStockprice()
        sql = 'SELECT * FROM stockPri WHERE stock=? '
        self.curs.execute(sql, (stockname,))
        self.conn.commit()
        value = self.curs.fetchall()
        stockTotalnum = value[0][3]
        self.closeDatabase()
        return stockTotalnum

    def getStockCurrentnum(self, stockname):
        """
        链接stockprice表，获取某支股票可购买数目
        :param stockname:   股票名称
        :return:            int股票数量
        """
        self.getLinkedStockprice()
        sql = 'SELECT * FROM stockPri WHERE stock=? '
        self.curs.execute(sql, (stockname,))
        self.conn.commit()
        value = self.curs.fetchall()
        stockTotalnum = value[0][2]
        self.closeDatabase()
        return stockTotalnum

    def getStockBalance(self, stockname):
        """
        链接stockprice表，获取某支股票市场余量
        :param stockname:   股票名称
        :return:            int股票剩余数量
        """
        self.getLinkedStockprice()
        sql = 'SELECT * FROM stockPri WHERE stock=? '
        self.curs.execute(sql, (stockname,))
        self.conn.commit()
        value = self.curs.fetchall()

        stockbalance = value[0][2]
        self.closeDatabase()
        return round((float)(stockbalance), 2)

    def changeStockBalance(self, stockname, num):
        """
        链接stockprice表，更改某支股票余额数量
        :param stockname:   股票名称
        :param num:         股票数量
        :return:            Bool
        """
        temp = int(self.getStockBalance(stockname))
        temp += num
        if 0 < temp < self.getStockTotalnum(stockname):
            self.getLinkedStockprice()
            sql = 'update stockPri set num=? where stock=?'
            self.curs.execute(sql, (temp, stockname))
            self.conn.commit()
            self.closeDatabase()
            return True
        else:
            self.closeDatabase()
            return False

    def changeStockPrice(self, stockname, price):
        """
        链接stockprice表，更改某支股票价格
        :param stockname:   股票名称
        :param price:       股票价格
        :return:            Bool
        """
        self.getLinkedStockprice()
        if 0 < price:
            sql = 'UPDATE stockPri SET price=? WHERE stock=?'
            self.curs.execute(sql, (price, stockname,))
            self.conn.commit()
            self.closeDatabase()
            return True
        else:
            self.closeDatabase()
            return False

    def addnewstock(self, stockname, stockprice, stocknum):
        """
        链接stockprice表，在其中增加一支股票
        :param stockname:   股票名称
        :param stockprice:  股票价格
        :param stocknum:    股票数量
        :return:            Bool
        """
        self.getLinkedStockprice()
        sql = 'insert into stockPri (stock,price,num,totalnum) values(?,?,?,?)'
        sql1 = 'insert into jiawei (stock,num) values(?,?)'
        sql2 = 'insert into hanxu (stock,num) values(?,?)'
        self.curs.execute(sql, (stockname, stockprice, stocknum, stocknum))
        self.curs.execute(sql1, (stockname, 0))
        self.curs.execute(sql2, (stockname, 0))
        self.conn.commit()
        self.closeDatabase()
        return True

    def initStock(self):
        """
        链接userProp表，复位
        :param stockname:   None
        :param stockprice:  None
        :param stocknum:    None
        :return:            None
        """

        stocknameList = self.getStocknameList()
        self.getLinkedStockprice()
        sql0 = 'update userProp set currentProp=? where username=?'
        self.curs.execute(sql0, (10000, self.__username))

        sql2 = 'update userProp set currentMoney=10000 where username=?'
        self.curs.execute(sql2, (self.__username,))

        for n in stocknameList:

            try:
                sql5 = 'select * from ' + self.__username + ' where stock=? '
                self.curs.execute(sql5, (n,))
                value = self.curs.fetchall()
                userStockNum = value[0][1]

                sql3 = 'select *from stockPri where stock=?'
                self.curs.execute(sql3, (n,))
                value = self.curs.fetchall()

                temp = int(value[0][2]) + userStockNum
                sql4 = 'update stockPri set num=? where stock=?'
                self.curs.execute(sql4, (temp, n))
                self.conn.commit()

                sql1 = 'update ' + self.__username + ' set num=0 where stock=?'
                self.curs.execute(sql1, (n,))
                self.conn.commit()
            except:
                askokcancel('init fail')
        self.closeDatabase()

    def deleteStock(self, stockName):
        """
        链接stockprice,user表，在其中减少一支股票
        :param stockname:   股票名称
        :return:            Bool
        """
        try:
            self.getLinkedStockprice()
            """
            此处应改为admin增加或者删除股票后，每个普通用户启动时，查询stockPri表，按照此表更新各自表的信息，增删股票代码，数量置为0
            """
            sql0 = 'delete from stockPri where stock=?'
            sql1 = 'delete from jiawei where stock=?'
            sql2 = 'delete from hanxu where stock=?'
            self.curs.execute(sql0, (stockName,))
            self.curs.execute(sql1, (stockName,))
            self.curs.execute(sql2, (stockName,))
            self.conn.commit()
            self.closeDatabase()
        except:
            return False

    def getStocknameList(self):
        """
        链接stockprice表，获取名字数组
        :return:    list数组
        """
        self.getLinkedStockprice()
        sql = 'select stock from stockPri'
        self.curs.execute(sql)
        self.conn.commit()
        value = self.curs.fetchall()
        stocknameList = []
        for n in value:
            stocknameList.append(n[0])
        self.closeDatabase()
        return stocknameList

    def getStockpriceList(self):
        """
        链接stockprice表，获取价格数组
        :return:    list数组
        """

        self.getLinkedStockprice()
        sql = 'select price from stockPri'
        self.curs.execute(sql)
        self.conn.commit()
        value = self.curs.fetchall()
        stockpricelist = []
        for n in value:
            stockpricelist.append(n[0])
        self.closeDatabase()
        return stockpricelist

    """
    链接userx表相关函数
    """

    def getLinkedUser(self, username):
        """
        链接user表
        :param username:    用户名
        :return:
        """
        self.__username = username
        self.conn = sqlite3.connect('testDB.db')
        self.curs = self.conn.cursor()

    def getUserStocknum(self, username, stockname):
        """
        链接user表，获取用户某支股票的数量
        :param username:    用户名称
        :param stockname:   股票名称
        :return:            int股票数量
        """
        self.getLinkedUser(username)
        sql = 'select * from ' + self.__username + ' where stock=?'
        self.curs.execute(sql, (stockname,))
        value = self.curs.fetchall()
        userstocknum = value[0][1]
        self.closeDatabase()
        return userstocknum

    def getUserStocknnumlist(self, username):
        """
        链接user表，获取用户股票数量的数组
        :param username:    股票名称
        :return:            list数组
        """
        self.getLinkedUser(username)
        sql = 'select num from ' + self.__username + ''
        self.curs.execute(sql)
        self.conn.commit()
        value = self.curs.fetchall()
        userStocknumlist = []
        for n in value:
            userStocknumlist.append(n[0])
        self.closeDatabase()
        return userStocknumlist

    def getUserStockpricelist(self):
        """
        链接user表，获取用户股票价格的数组
        :param username:    股票名称
        :return:            list数组
        """
        self.getLinkedStockprice()
        sql = 'select price from stockPri'
        self.curs.execute(sql)
        self.conn.commit()
        value = self.curs.fetchall()
        userstockpricelist = []
        for n in value:
            userstockpricelist.append(n[0])
        self.closeDatabase()
        return userstockpricelist

    def getUserStockprop(self):
        """
        链接user表，获取用户股票总资产
        :param username:    股票名称
        :return:            float股票资产
        """
        userStockpricelist = self.getUserStockpricelist()
        userStocknumlist = self.getUserStocknnumlist(self.__username)
        money = sum(map(lambda(a,b):a*b, zip(userStockpricelist, userStocknumlist)))
        return round(money, 2)

    def changeUserStocknum(self, username, stockname, num):
        """
        链接user表，更改用户股票数量
        :param username:    用户名
        :param stockname:   股票名称
        :param num:         股票数量
        :return:            list数组
        """
        self.getLinkedUser(username)
        temp = int(num)
        temp += self.getUserStocknum(username, stockname)
        if -1 < temp < self.getStockTotalnum(stockname):
            self.getLinkedUser(username)
            sql = 'update ' + self.__username + ' set num=? where stock=?'
            self.curs.execute(sql, (temp, stockname))
            self.conn.commit()
            self.closeDatabase()
            return True
        else:
            askokcancel('交易失败', u'你股票余额不够，请重头来过！')
            self.closeDatabase()
            return False

    def getUserStockholdingStr(self, username):
        """
        链接user表，获取用户持有股票的信息
        :param username:    用户名
        :return:            string持股信息
        """
        userstocknumlist = self.getUserStocknnumlist(username)
        userstocknamelist = self.getStocknameList()
        i = 0
        str1 = ''
        for n in userstocknamelist:
            str1 = str1 + 'StockName   ' + n + '  StockNum : ' + str(userstocknumlist[i]) + '\n'
            i += 1
        return str1

    def getLinkedUserprop(self):
        """
        链接userPro表，用户资产表
        :return:
        """
        self.conn = sqlite3.connect('testDB.db')
        self.curs = self.conn.cursor()

    def updateUserCurrentprop(self):
        """
        链接userPro表，更新数据库中用户现有总资产
        :return:
        """
        temp = self.getUserCurrentmoney() + self.getUserStockprop()
        self.getLinkedUserprop()
        sql = 'update userProp set currentProp=? where username=?'
        self.curs.execute(sql, (temp, self.__username))
        self.conn.commit()
        self.closeDatabase()

    def getUserOriginalprop(self):
        """
        链接userPro表，获取用户原始资产
        :return:    float用户原始资产
        """
        self.getLinkedUserprop()
        sql = 'SELECT * FROM userProp WHERE username=? '
        self.curs.execute(sql, (self.__username,))
        self.conn.commit()
        value = self.curs.fetchall()
        originalprop = value[0][1]
        self.closeDatabase()
        return round(originalprop, 2)

    def getUserCurrentprop(self):
        """
        链接userPro表，获取用户当前资产
        :return:    float用户当前资产
        """
        self.updateUserCurrentprop()
        self.getLinkedUserprop()
        sql = 'SELECT * FROM userProp WHERE username=? '
        self.curs.execute(sql, (self.__username,))
        self.conn.commit()
        value = self.curs.fetchall()
        currentprop = value[0][2]
        self.closeDatabase()
        return round(currentprop, 2)

    def getUserCurrentmoney(self):
        """
        链接userPro表，获取用户当前资金
        :return:    float用户当前资金
        """
        self.getLinkedUserprop()
        sql = 'SELECT * FROM userProp WHERE username=? '
        self.curs.execute(sql, (self.__username,))
        self.conn.commit()
        value = self.curs.fetchall()

        originalmoney = value[0][3]

        self.closeDatabase()
        return round((float)(originalmoney), 2)

    def changeUserCurrentmoney(self, money):
        """
        链接userPro表，改变用户当前资金
        :param money:   float，改变的金钱（正为增加、负为减少）
        :return:        Bool
        """
        self.getLinkedUserprop()
        temp = money + self.getUserCurrentmoney()
        if 0 < temp:
            self.getLinkedUserprop()
            sql = 'update userProp set currentMoney=? where username=?'
            self.curs.execute(sql, (temp, self.__username))
            self.conn.commit()
            self.closeDatabase()
            return True
        else:
            self.closeDatabase()
            return False

    def getUseprofit(self):
        """
        链接userPro表，获取用户盈利
        :return:    float，用户盈利
        """
        return self.getUserCurrentprop() - self.getUserOriginalprop()

    """"
    链接namepassword表相关函数
    """

    def getLinkedNamepassword(self, name, password):
        """
        链接namepassword表，验证name和password是否匹配
        :param name:        用户名
        :param password:    密码
        :return:            Bool
        """
        self.conn = sqlite3.connect('testDB.db')
        self.curs = self.conn.cursor()
        sql = 'SELECT * FROM namePassword where name=? '
        try:
            self.curs.execute(sql, (name,))
            value = self.curs.fetchall()
            a = value[0][1]
            if a == password:
                self.__username = name
                self.closeDatabase()
                return True
            else:
                self.closeDatabase()
                return False
        except:
            self.closeDatabase()
            return -1

    def closeDatabase(self):
        self.curs.close()
        self.conn.commit()
        self.conn.close()


class ViewFrame():
    """
    @Class describe：    显示类、属于表现层。包含所有界面显示相关操作,与事务处理层链接
    @param:     __username      用户名
    """
    __username = ''

    def loginSys(self):
        """
        登录界面
        :return:
        """
        root = Tk()
        root.title("欢迎进入股票交易系统！")
        root.geometry('500x300')

        def quit():
            """
            销毁登录界面
            :return:
            """
            root.quit()
            root.destroy()

        def enter():
            """
            登陆按钮响应函数，成功则进入股票显示界面
            :return:
            """
            myName = personName.get()
            myPassword = password.get()
            myName = myName.lower()

            db = Database('testDB.db', self.__username)
            temp = db.getLinkedNamepassword(myName, myPassword)
            if 1 == temp:
                self.__username = myName
                quit()
                self.showStock()
            elif 0 == temp:
                contents.delete(1.0, END)
                contents.insert(END, u"密码错误，请输入正确密码！(●'◡'●)")
            elif -1 == temp:
                contents.delete(1.0, END)
                contents.insert(END, u"用户不存在，请核实用户名重新输入( ▼-▼ )")

        L1 = Label(root, text="用户名", font=("微软雅黑", 12), width=6, height=2)
        L1.grid(row=0, column=0, sticky=E)
        personName = Entry(root)
        personName.grid(row=0, column=1, sticky=E)

        L2 = Label(root, text="密码 ", font=("微软雅黑", 12), width=6, height=2)
        L2.grid(row=1, column=0, sticky=E)

        password = Entry(root)
        password.grid(row=1, column=1, sticky=E)
        root.bind('<Return>', enter)
        ButtonEnter = Button(root, text="登陆", command=enter, bg="grey", font=("微软雅黑", 12), width=5, height=2)
        ButtonEnter.grid(row=0, column=2, columnspan=1, rowspan=2, sticky=E, padx=30, pady=30)

        contents = Text(root)
        contents.grid(row=2, column=0, columnspan=4, rowspan=1)
        contents.delete(1.0, END)
        contents.insert(END, '请在上方输入用户名称和密码进入股票交易系统q(≧▽≦q)')
        mainloop()

    def showStock(self):
        """
        股价显示界面
        :return:
        """
        root = Tk()
        root.wm_title('股票市场     当前用户 : ' + self.__username)
        root.geometry('720x480')
        f = Figure(figsize=(5, 5), dpi=90)

        def relogin():
            """
            返回登陆界面
            :return:
            """
            quit()
            self.loginSys()

        def quit():
            """
            销毁当前窗口
            :return:
            """
            root.quit()
            root.destroy()

        def draw_picture():
            """
            绘制股票显示图表
            :return:
            """
            stk = Stock('')
            stk.showStockprice(f)
            canvas.draw()

        def addNewstock():
            """
            增加一支新股票，addnewstock的响应函数
            :return:
            """
            stockname = stock.get()
            stocknum = int(num.get())
            stockpri = float(stockprice.get())
            stk = Stock('')
            stk.addNewstock(stockname, stockpri, stocknum)
            draw_picture()

        def trade():
            """
            销毁股票显示界面，进入trade按钮的响应函数
            :return:
            ##"""
            quit()
            self.exchange()

        def deleteStock():
            """
            删除一支新股票，deleteStock的响应函数
            :return:
            """
            stockname = stock.get()
            stk = Stock('')
            stk.deleteStock(stockname)
            draw_picture()

        def findDB():
            """
            查找一支新股票，获取其市场余量和价格
            :return:
            """
            try:
                stockName = stock.get()
                stk = Stock('')
                num.delete(0, END)
                str0 = stk.getStockNum(stockName)
                num.insert(0, str0)

                stockprice.delete(0, END)
                str0 = stk.getStockPrice(stockName)
                stockprice.insert(0, str0)
            except:
                askokcancel('查询失败', u'请检查股票代码！')

        canvas = FigureCanvasTkAgg(f, root)
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, rowspan=6, sticky=W + N)

        if self.__username == 'admin':
            L1 = Label(root, text="股票代码", font=("微软雅黑", 12), width=10, height=1)
            L1.grid(row=0, column=5, sticky=E)
            stock = Entry(root)
            stock.grid(row=0, column=6, sticky=E)

            L2 = Label(root, text="股票数目", font=("微软雅黑", 12), width=10, height=1)
            L2.grid(row=1, column=5, sticky=W)
            num = Entry(root)
            num.grid(row=1, column=6, sticky=E)

            L3 = Label(root, text="股票价格", font=("微软雅黑", 12), width=10, height=1)
            L3.grid(row=2, column=5, sticky=W)
            stockprice = Entry(root)
            stockprice.grid(row=2, column=6, sticky=E)
            Button(root, text="新股发行", command=addNewstock, bg="grey", width=10, height=1).grid(row=3, column=5,
                                                                                               sticky=E)
            Button(root, text="股票退市", command=deleteStock, bg="grey", width=10, height=1).grid(row=3, column=6,
                                                                                               sticky=E)
            Button(root, text="股市刷新", command=draw_picture, bg="grey", width=10, height=1).grid(row=4, column=5,
                                                                                                sticky=E)
            Button(root, text="退出系统", command=quit, bg="grey", width=10, height=1).grid(row=4, column=6, sticky=E)
            Button(root, text="重新登录", command=relogin, bg="grey", width=10, height=1).grid(row=5, column=5, sticky=E)
            Button(root, text="股票查询", command=findDB, bg="grey", width=10, height=1).grid(row=5, column=6, sticky=E)

        if self.__username != 'admin':
            L1 = Label(root, text="股票代码", font=("微软雅黑", 12), width=10, height=1)
            L1.grid(row=0, column=5, sticky=E)
            stock = Entry(root)
            stock.grid(row=0, column=6, sticky=E)

            L2 = Label(root, text="股票余量", font=("微软雅黑", 12), width=10, height=1)
            L2.grid(row=1, column=5, sticky=W)
            num = Entry(root)
            num.grid(row=1, column=6, sticky=E)

            L3 = Label(root, text="股票价格", font=("微软雅黑", 12), width=10, height=1)
            L3.grid(row=2, column=5, sticky=W)
            stockprice = Entry(root)
            stockprice.grid(row=2, column=6, sticky=E)
            Button(root, text="用户交易", command=trade, bg="grey", width=10, height=1).grid(row=3, column=5, sticky=E)
            Button(root, text="股市刷新", command=draw_picture, bg="grey", width=10, height=1).grid(row=3, column=6,
                                                                                                sticky=E)
            Button(root, text="退出系统", command=quit, bg="grey", width=10, height=1).grid(row=4, column=5, sticky=E)
            Button(root, text="重新登录", command=relogin, bg="grey", width=10, height=1).grid(row=4, column=6, sticky=E)
            Button(root, text="股票查询", command=findDB, bg="grey", width=10, height=1).grid(row=5, column=5, sticky=E)
        draw_picture()
        askokcancel('欢迎!', '尊敬的' + self.__username + '欢迎进入股票交易系统!')
        mainloop()

    def exchange(self):
        """
        用户信息及交易显示界面
        :return:
        """
        root = Tk()
        root.resizable(width=True, height=True)
        root.wm_title("用户交易       当前用户 : " + self.__username)
        f = Figure(figsize=(7, 5), dpi=80)

        def check():
            """刷新股仓，刷新图像显示，显示用户的资产变化情况。
            :return:
            """
            stk = Stock(self.__username)
            stk.floatStock()

            user = User(self.__username)

            str1 = user.getStockholdingMsg()
            userStock.delete('1.0', END)
            userStock.selection_clear()
            userStock.insert(END, str1)

            userCurrency.delete(0, END)
            str0 = user.getBalance()
            userCurrency.insert(0, str0)

            userGain.delete(0, END)
            str0 = user.getProfitOrLoss()
            userGain.insert(0, str0)

            userallProp.delete(0, END)
            str0 = user.getTotalProperty()
            userallProp.insert(0, str0)

            userStockPro.selection_clear()
            str1 = str(round(user.getStockProp(), 2))
            userStockPro.delete(0, END)
            userStockPro.insert(0, str1)

            draw_picture()

        def __init():
            """复位
            :return:
            """
            stk = Stock(self.__username)
            stk.initStock()
            check()

        def quit():
            """退出函数，退出界面、程序,quit按钮响应函数
            :return:
            """
            root.quit()
            root.destroy()

        def back():
            """返回函数，关闭当前界面，回到股价界面，back按钮响应函数
            :return:
            """
            quit()
            self.showStock()

        def draw_picture():
            """绘制用户股票数量图像
            :return:
            """
            user = User(self.__username)
            user.drawUserExchange(f)
            canvas.draw()

        def sell():
            """卖出股票，sell按钮响应函数
            :return:         bool
            """
            try:
                stockname = exchangeStockname.get()
                stocknum = int(exchangeStocknum.get())
                user = User(self.__username)
                if user.sellOneStock(stockname, -stocknum):
                    check()
                else:
                    askokcancel('卖出失败', u'股票代码错误或仓库不足，请核对持有的股票代码及数量！')

            except:
                askokcancel('卖出失败', u'股票代码错误或仓库不足，请核对持有的股票代码及数量！')
                return False

        def buy():
            """
            购买股票，buy按钮响应函数
            :return:           bool
            """
            try:
                stockname = exchangeStockname.get()
                stocknum = int(exchangeStocknum.get())
                user = User(self.__username)
                if user.buyOneStock(stockname, stocknum):
                    check()
                else:
                    askokcancel('操作无效', '现金不足或者股票代码输入错误！')
                return True
            except:
                askokcancel('操作无效', '现金不足或者股票代码输入错误！')
                return False

        canvas = FigureCanvasTkAgg(f, root)
        canvas.get_tk_widget().grid(row=0, column=1, columnspan=5, rowspan=5, sticky=W + N)

        L1 = Label(root, text="交易股票代码", font=("微软雅黑", 11))
        L1.grid(row=0, column=6, sticky=W)
        exchangeStockname = Entry(root)
        exchangeStockname.grid(row=0, column=7, sticky=W, padx=2)

        L2 = Label(root, text="交易股票数目", font=("微软雅黑", 11))
        L2.grid(row=0, column=8, sticky=W, padx=2)
        exchangeStocknum = Entry(root)
        exchangeStocknum.grid(row=0, column=9, sticky=W)

        L3 = Label(root, text="用户当前总资产", font=("微软雅黑", 11))
        L3.grid(row=0, column=10, sticky=W, padx=2)
        userallProp = Entry(root)
        userallProp.grid(row=0, column=11, sticky=W)

        L4 = Label(root, text="用户股票资产", font=("微软雅黑", 11))
        L4.grid(row=1, column=6, sticky=W, padx=2)
        userStockPro = Entry(root)
        userStockPro.grid(row=1, column=7, sticky=W)

        L5 = Label(root, text="用户当前现金", font=("微软雅黑", 11))
        L5.grid(row=1, column=8, sticky=W, padx=2)
        userCurrency = Entry(root)
        userCurrency.grid(row=1, column=9, sticky=W)

        L6 = Label(root, text="用户当前盈亏额", font=("微软雅黑", 11))
        L6.grid(row=1, column=10, sticky=W, padx=2)
        userGain = Entry(root)
        userGain.grid(row=1, column=11, sticky=W)

        L7 = Label(root, text="用户持有股票", font=("微软雅黑", 11))
        L7.grid(row=3, column=6, sticky=W)
        userStock = Text(root)
        userStock.grid(row=3, column=7, columnspan=10, sticky=W)

        Button(root, text="刷新股仓", command=check, bg="grey", width=6, height=1, font=("微软雅黑", 11)).grid(row=2, column=6)
        Button(root, text="卖出股票", command=sell, bg="grey", width=6, height=1, font=("微软雅黑", 11)).grid(row=2, column=8)
        Button(root, text="买入股票", command=buy, bg="grey", width=6, height=1, font=("微软雅黑", 11)).grid(row=2, column=7)
        Button(root, text="退出系统", command=quit, bg="grey", width=6, height=1, font=("微软雅黑", 11)).grid(row=2, column=11)
        Button(root, text="返回市场", command=back, bg="grey", width=6, height=1, font=("微软雅黑", 11)).grid(row=2, column=9)
        Button(root, text="市场复位", command=__init, bg="grey", width=6, height=1, font=("微软雅黑", 11)).grid(row=2,
                                                                                                        column=10)

        check()
        mainloop()


if __name__ == '__main__':
    """
    主函数
    """
    window = ViewFrame()
    window.loginSys()
    raw_input()

from view import *
from tkinter import messagebox
import dbOperations as dbClient
import SetupProxy as proxy


class MainPage(object):
    @staticmethod
    def clearProxy():
        proxy.clearproxy()

    @staticmethod
    def setProxy(proxyInfo):
        if len(proxyInfo.curselection()) == 0:
            messagebox.showerror(title='错误', message="请先选择一个代理Ip地址")
            return
        else:
            proxyIp = proxyInfo.get(proxyInfo.curselection()).split(" ")[0]
            proxy.setProxy(proxyIp)

    def searchProxyIps(self, searchText):
        ipsInside = dbClient.fetchByPage(1, self.pageSize, searchText)
        self.v.set(ipsInside)
        self.pageNo += 1

    def previousProxyIps(self, searchText):
        print(self.searchBtnText, searchText)

    def nextProxyIps(self, searchText):
        pageNo1 = (self.pageNo - 1) * self.pageSize
        ipsInside = dbClient.fetchByPage(pageNo1, self.pageSize, searchText)
        if len(ipsInside) == 0:
            self.pageNo = 1
            pageNo1 = (self.pageNo - 1) * self.pageSize
            ipsInside = dbClient.fetchByPage(pageNo1, self.pageSize, searchText)
            self.v.set(ipsInside)
        else:
            self.v.set(ipsInside)
        self.pageNo += 1

    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.pageNo = 1
        self.pageSize = 10
        self.v = StringVar()
        self.previousPageText = StringVar()
        self.nextPageText = StringVar()
        self.searchBtnText = StringVar()
        self.searchtext = StringVar()
        self.previousPageText.set("上一页")
        self.nextPageText.set("下一页")
        self.searchBtnText.set("检索")
        self.root.geometry('%dx%d' % (350, 300))  # 设置窗口大小
        self.nextProxyIps(self.searchtext.get())
        self.createPage()

    def createPage(self):
        # 检索框
        searchText = Entry(textvariable=self.searchtext)
        searchText.place(x=45, y=11)

        # 检索按钮
        searchBtn = Button(self.root, textvariable=self.searchBtnText, text=self.searchBtnText,
                           command=lambda: self.searchProxyIps(searchText.get()))
        searchBtn.place(x=200, y=7)

        # 上一页按钮
        previousPageBtn = Button(self.root, textvariable=self.previousPageText, text=self.previousPageText,
                                 command=lambda: self.previousProxyIps(searchText.get()))
        previousPageBtn.place(x=35, y=40)

        # 下一页按钮
        nextPageBtn = Button(self.root, textvariable=self.nextPageText, text=self.nextPageText,
                             command=lambda: self.nextProxyIps(searchText.get()))
        nextPageBtn.place(x=200, y=40)

        # 代理ip地址
        proxyIpList = Listbox(self.root, listvariable=self.v, width=40)
        proxyIpList.selection_set(first=0)
        proxyIpList.place(x=15, y=73)

        # 设置代理按钮
        setProxyBtn = Button(self.root, text="设置代理", command=lambda: self.setProxy(proxyIpList))
        setProxyBtn.place(x=45, y=260)

        # 清楚代理按钮
        clearProxyBtn = Button(self.root, text="清除代理", command=self.clearProxy)
        clearProxyBtn.place(x=150, y=260)

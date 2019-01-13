from view import *
from tkinter import messagebox
import DBPool as Pool


class MainPage(object):
    def clearProxy(self):
        print("cleared")

    def setProxy(self, proxyInfo):
        if len(proxyInfo.curselection()) == 0:
            messagebox.showerror(title='错误', message="请先选择一个代理Ip地址")
            return
        else:
            print(proxyInfo.get(proxyInfo.curselection()))

    def fetchDb(self, searchText):
        print(searchText)
        pageNo1 = self.pageNo - 1
        pageNo1 = pageNo1 * self.pageSize
        ipsInside = Pool.funcFetch(pageNo1, self.pageSize)
        if len(ipsInside) == 0:
            self.pageNo = 1
            pageNo1 = self.pageNo - 1
            pageNo1 = pageNo1 * self.pageSize
            ipsInside = Pool.funcFetch(pageNo1, self.pageSize)
            self.v.set(ipsInside)
        else:
            self.v.set(ipsInside)
            self.pageNo += 1

    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.pageNo = 1
        self.pageSize = 10
        self.v = StringVar()
        self.nextPageText = StringVar()
        self.searchtext = StringVar()
        self.nextPageText.set("下一页")
        self.root.geometry('%dx%d' % (260, 330))  # 设置窗口大小
        self.fetchDb(self.searchtext.get())
        self.createPage()

    def createPage(self):
        text = Entry(textvariable=self.searchtext)
        text.place(x=45, y=11)
        btn1 = Button(self.root, textvariable=self.nextPageText, text=self.nextPageText,
                      command=lambda: self.fetchDb(text.get()))
        btn1.place(x=155, y=5)

        lb = Listbox(self.root, listvariable=self.v, width=35)
        lb.selection_set(first=0)
        lb.place(x=15, y=40)

        btn2 = Button(self.root, text="设置代理", command=lambda: self.setProxy(lb))
        btn2.place(x=45, y=230)
        btn3 = Button(self.root, text="清除代理", command=self.clearProxy)
        btn3.place(x=150, y=230)

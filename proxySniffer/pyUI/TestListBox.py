# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import messagebox
import DBPool as Pool

root = Tk()
pageNo = 1
pageSize = 4
v = StringVar()
nextPageText = StringVar()


def setProxy(proxyInfo):
    if len(proxyInfo) == 0:
        messagebox.showerror(title='错误', message="请先选择一个代理Ip地址")
        return
    else:
        print(lb.get(proxyInfo))


def fetchDb():
    global pageNo
    global v
    global nextPageText
    pageNo1 = pageNo - 1
    pageNo1 = pageNo1 * pageSize
    ipsInside = Pool.funcFetch(pageNo1, pageSize)
    if len(ipsInside) == 0:
        pageNo = 1
        pageNo1 = pageNo - 1
        pageNo1 = pageNo1 * pageSize
        ipsInside = Pool.funcFetch(pageNo1, pageSize)
        v.set(ipsInside)
    else:
        v.set(ipsInside)
        pageNo += 1


nextPageText.set("下一页")

fetchDb()
btn = Button(textvariable=nextPageText, text=nextPageText, command=fetchDb)
btn.pack()
btn = Button(text="设置代理", command=lambda: setProxy(lb.curselection()))
btn.pack()
lb = Listbox(root, listvariable=v, width=36)
lb.selection_set(first=0)
lb.pack()
root.mainloop()

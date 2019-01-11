from tkinter import *
import DBPool as Pool

pageNo = 1
pageSize = 4


def fetchDb():
    pageNo1 = pageNo - 1
    pageNo1 = pageNo1 * pageSize
    pageNo = pageNo1+1
    ipsInside = Pool.funcFetch(pageNo1, pageSize)
    return ipsInside


def loginCheck():
    pageNo = + 1


root = Tk()
ips = fetchDb()
v = StringVar()
v.set(ips)

btn = Button(text="下一页", command=fetchDb)
btn.pack()
lb = Listbox(root, listvariable=v)
lb.pack()
root.mainloop()

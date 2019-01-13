from MainPage import *
from CheckSign import check


class LoginPage(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.geometry('%dx%d' % (300, 180))  # 设置窗口大小
        self.root.resizable(height=False, width=False)
        self.username = StringVar()
        self.password = StringVar()
        self.createPage()

    def createPage(self):
        self.page = Frame(self.root)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Label(self.page, text='账户: ').grid(row=1, stick=W, pady=10)
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, columnspan=5, stick=E)
        Label(self.page, text='密码: ').grid(row=2, stick=W, pady=10)
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, columnspan=5, stick=E)
        Button(self.page, text='登陆', command=self.loginCheck).grid(row=3, column=1, columnspan=2)
        Button(self.page, text='退出', command=self.page.quit).grid(row=3, column=3, columnspan=4)

    def loginCheck(self):
        name = self.username.get()
        secret = self.password.get()
        if check(name, secret) is True:
            self.page.destroy()
            MainPage(self.root)
        else:
            showinfo(title='错误', message='账号或密码错误！')

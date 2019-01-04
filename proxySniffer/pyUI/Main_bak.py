from tkinter import messagebox
import tkinter as tk
from CheckSign import check

import Test

window = tk.Tk()
window.title("Welcome")
window.geometry('450x300')
window.resizable(height=False, width=False)

# welcome image
# 创建画布
canvas = tk.Canvas(window, height=200, width=500)
# 加载图片文件
image_file = tk.PhotoImage(file='3-01-02.gif')
# 将图片置于画布上
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
# 放置画布（为上端）
canvas.pack(side='top')

# user information
tk.Label(window, text='User name: ').place(x=50, y=150)
tk.Label(window, text='Password: ').place(x=50, y=190)

var_usr_name = tk.StringVar()
entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)
var_usr_pwd = tk.StringVar()
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)


def usr_login():
    user_name = var_usr_name.get()
    user_pwd = var_usr_pwd.get()
    if not check(user_name, user_pwd):
        tk.mainloop(Test)
        messagebox.showerror(title='Error', message='用户名或者密码不能为空')
    else:
        messagebox.showinfo(title='Hdddi', message=user_name + "<>" + user_pwd)


def usr_sign_up():
    window.destroy()


# login and quit button
# 定义`button`按钮: `登录`、'退出',触发命令为`usr_login`
btn_login = tk.Button(window, text='登录', command=usr_login)
btn_login.place(x=175, y=230)

btn_sign_up = tk.Button(window, text='退出', command=usr_sign_up)
btn_sign_up.place(x=250, y=230)

window.mainloop()

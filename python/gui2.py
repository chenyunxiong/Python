# -*- coding:utf-8 -*-

import tkinter as tk

root_window = tk.Tk()

root_window.title('标题')

lable = tk.Label(root_window, text = "文本aaa", bg = "yellow", fg="red", font = {'Times', 20, 'bold italic'})
lable.pack()

btn = tk.Button(root_window, text="close", command = root_window.quit())
btn.pack()

root_window.mainloop()
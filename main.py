from tkinter import *
from tkinter import messagebox
import bscscan_functions
from settings import COOKIE, USER_AGENT, SID, CHROME_LOC
import liquidity

baby_address = {
    "c_address": "0x53e562b9b7e5e94b81f10e96ee70ad06df3d2657",
    "create_address": "0x0000000000000000000000000000000000000000",
    "destroy_address": "0x000000000000000000000000000000000000dead"
}

milk_address = {
    "c_address": "0xBf37f781473f3b50E82C668352984865eac9853f",
    "create_address": "0x0000000000000000000000000000000000000000",
    "destroy_address": "0x000000000000000000000000000000000000dead"
}

def get_message(coin_choice, time_frame, info_choice):
    message = "请重新填写 cookie、sid 和 user-agent 信息"
    if coin_choice == "BABY":
        c_address = baby_address["c_address"]
        if info_choice == "create":
            w_address = baby_address["create_address"]
            message = bscscan2str(w_address, time_frame, c_address)
        elif info_choice == "destroy":
            w_address = baby_address["destroy_address"]
            message = bscscan2str(w_address, time_frame, c_address)
        else:
            message = liq2str(coin_choice, CHROME_LOC)
    elif coin_choice == "MILK":
        c_address = milk_address["c_address"]
        if info_choice == "create":
            w_address = milk_address["create_address"]
            message = bscscan2str(w_address, time_frame, c_address)
        elif info_choice == "destroy":
            w_address = baby_address["destroy_address"]
            message = bscscan2str(w_address, time_frame, c_address)
        else:
            message = liq2str(coin_choice, CHROME_LOC)

    return message


def bscscan2str(w_address, time_frame, c_address):
    account, supply, percentage = bscscan_functions.get_quantity(SID, COOKIE, USER_AGENT, c_address, w_address,
                                                                 time_frame)
    message = "过去" + time_frame +"，共产出/销毁" + str(account) + "代币，占总supply的" + str(percentage)
    return message


def liq2str(coin, chrome_loc):
    liq = liquidity.get_liquidity(coin, chrome_loc)
    message = coin + " 代币实时锁仓量为：\nUSD$" + str(liq)
    return message

root = Tk()
root.title('代币短期内产量/锁仓量/销毁量查询')

# Drop Down Boxes
def popup():
    time_frame = time_clicked.get()
    coin_choice = coin_clicked.get()
    info = type_clicked.get()
    if info == "产量":
        info_choice = "create"
    elif info == "销毁量":
        info_choice = "destroy"
    # elif info == "锁仓量(实时)":
    else:
        info_choice = "liquidity"
    message = get_message(coin_choice, time_frame, info_choice)
    #
    messagebox.showinfo("Coin info", message)

######## UI ########

#coin dropdown
coin_options = ["BABY", "MILK"]
coin_clicked = StringVar()
coin_clicked.set(coin_options[0])

coin_lable = Label(root, padx=10, text="代币选择", anchor=W)
coin = OptionMenu(root, coin_clicked, *coin_options)
coin.config(width=5)
coin_lable.grid(row=0,column=0)
coin.grid(row=1,column=0)

#time dropdown
time_options = ["24h", "48h", "72h"]
time_clicked = StringVar()
time_clicked.set(time_options[0])

time_lable = Label(root, padx=10, text="时间范围", anchor=W)
time = OptionMenu(root, time_clicked, *time_options)
time.config(width=5)
time_lable.grid(row=0,column=1)
time.grid(row=1,column=1)

#type_dropdown
type_options = ["产量", "销毁量", "锁仓量(实时)"]
type_clicked = StringVar()
type_clicked.set(type_options[2])

type_lable = Label(root, padx=10, text="所需信息", anchor=W)
type = OptionMenu(root, type_clicked, *type_options)
type.config(width=10)
type_lable.grid(row=0,column=2)
type.grid(row=1,column=2)

#button
my_button = Button(root, text="查询信息",padx=5,pady=5,bg="#696969", command=popup).grid(row=2,column=3)
button_label1 = Label(root, padx=5, bd=1, relief=SUNKEN, fg="grey", anchor=W, text="!注意!：数据爬虫需要较长时间，请耐心等待!")
button_label1.grid(row=3, column=0, columnspan=4, sticky=W+E)

root.mainloop()
from tkinter import *
from tkinter import messagebox
import bscscan_functions
from settings import COOKIE, USER_AGENT, SID, CHROME_LOC
import liquidity
import ray

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


def get_message(coin_choice, time_frame):
    message = "请重新填写 cookie、sid 和 user-agent 信息"
    if coin_choice == "BABY":
        address_choice = baby_address
    else:
        address_choice = milk_address

    c_address = address_choice["c_address"]
    create_address = address_choice["create_address"]
    destroy_address = address_choice["destroy_address"]
    cr = bscscan2str.remote(create_address, time_frame, c_address)
    de = bscscan2str.remote(destroy_address, time_frame, c_address)
    li = liq2str.remote(coin_choice, CHROME_LOC)

    try:
        create, destroy, liquid = ray.get([cr, de, li])
        message = "过去" + time_frame + "\n\n共产出" + str("%.2f" %create[0]) + "代币 (" +\
                  str(create[1]) + ")\n\n共销毁" + str("%.2f" %destroy[0]) + "代币 (" +\
                  str(destroy[1]) + ")\n\n目前锁仓量为$USD" + str(liquid)
    except:
        message = "请重新填写 cookie、sid 和 user-agent 信息"
        return message

    return message


@ray.remote
def bscscan2str(w_address, time_frame, c_address):
    quant, supply, percentage = \
        bscscan_functions.get_quantity(SID, COOKIE, USER_AGENT, c_address, w_address, time_frame)
    return [quant, percentage]


@ray.remote
def liq2str(coin, chrome_loc):
    liq = liquidity.get_liquidity(coin, chrome_loc)
    return liq


root = Tk()
root.title('代币短期内产量/锁仓量/销毁量查询')


# Drop Down Boxes
def popup():
    time_frame = time_clicked.get()
    coin_choice = coin_clicked.get()
    message = get_message(coin_choice, time_frame)
    messagebox.showinfo("Coin info", message)


######## UI ########

# coin dropdown
coin_options = ["BABY", "MILK"]
coin_clicked = StringVar()
coin_clicked.set(coin_options[0])

coin_lable = Label(root, padx=10, text="代币选择", anchor=W)
coin = OptionMenu(root, coin_clicked, *coin_options)
coin.config(width=5)
coin_lable.grid(row=0, column=0)
coin.grid(row=1, column=0)

# time dropdown
time_options = ["24h", "48h", "72h"]
time_clicked = StringVar()
time_clicked.set(time_options[0])

time_lable = Label(root, padx=10, text="时间范围", anchor=W)
time = OptionMenu(root, time_clicked, *time_options)
time.config(width=5)
time_lable.grid(row=0, column=1)
time.grid(row=1, column=1)

# type_dropdown
# type_options = ["产量", "销毁量", "锁仓量(实时)"]
# type_clicked = StringVar()
# type_clicked.set(type_options[2])
#
# type_lable = Label(root, padx=10, text="所需信息", anchor=W)
# type = OptionMenu(root, type_clicked, *type_options)
# type.config(width=10)
# type_lable.grid(row=0,column=2)
# type.grid(row=1,column=2)

# button
my_button = Button(root, text="查询信息", padx=5, pady=5, bg="#696969", command=popup).grid(row=2, column=3)
button_label1 = Label(root, padx=5, bd=1, relief=SUNKEN, fg="grey", anchor=W, text="!注意!：数据爬虫需要较长时间，请耐心等待!")
button_label1.grid(row=3, column=0, columnspan=4, sticky=W + E)

root.mainloop()

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import  datetime
import time
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    start_time = "17:30:00"
    date_time_str = "{} {}".format(today, start_time)
    date_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    if now >= date_time:
        print("Yes")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

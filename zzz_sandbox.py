from datetime import datetime

import zzz_tools as t

# dt_string = "2021-01-01 12:14"
# dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M")
#
# # if t.confirm("yes"):
# #     t.msgBox("yes")
# # print(t.getRoundedDownTime(dt, 30, 0, 0))
# # print(t.getRoundedDownTime(dt, 30, 0, 30))
# # print(t.getRoundedDownTime(dt, 30, 15, 0))
#
# print (t.inputBox("Enter a number"))


# a= t.confirm("Do you want to export df?", "Unjoined values")

# print(t.getTimebandId("Polsat", datetime.now(), 30, 0, 0))

my_dict = {"apple": 1, "banana": 2}

key = "apple"
value = 3

if key in my_dict:
    raise KeyError(f"Key '{key}' already exists in dictionary")
else:
    my_dict.__setitem__(key, value)

print(my_dict)

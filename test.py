from datetime import *

for y in range(1, 400):
    c = 5* (y//100)
    y1 = y % 100
    l = y1 // 4
    delta = (c + y1 +l) % 7
    doom = (2 + delta) % 7
    if doom == 0: doom = 7
    assert doom == date(y, 4, 4).isoweekday()

import json
from random import choice
times = [("0730", "0900"), ("0915", "1100"), ("1115", "1300"), ("1315", "1500"),
         ("1515", "1655"), ("1705", "1845"), ("1855", "2035")]
dows = list(range(1, 6))
pars = [1,2]



def s1():
    start, end = choice(times)
    return{"start": start, "end": end, "dow": choice(dows)}


def s2():
    start, end = choice(times)
    return {"start": start, "end": end, "dow": choice(dows), "par": choice(pars)}

def main():
    acc = {}
    for i in range(1,3):
        acc["O{}".format(i)] = [s1()]
    print(json.dumps(acc))

if __name__ == "__main__":
    main()

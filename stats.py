import re
with open("./trades.txt", 'r') as tradeFile:
    Lines = tradeFile.readlines()
    count = 0
    result = []
    profitSum = 0
    for line in Lines:
        count += 1
        matchObj = re.match(r'.*Profit:\s*([\-0-9.]+)', line)
        if matchObj:
            profit = float(matchObj.group(1))
            profitSum += profit

    print("profitSum:", profitSum)
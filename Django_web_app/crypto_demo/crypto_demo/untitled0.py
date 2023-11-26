

s = "AB"
numRows = 1

lists_ = [''] * numRows

print(lists_)


current_way = 1
currentindex = 0

for c in s :
    print(currentindex)
    lists_[currentindex] = lists_[currentindex] + c
    if(currentindex == 0):
        current_way = 1
    else:
        if(currentindex == numRows):
            current_way = -1
            
    currentindex += current_way

print(lists_)
    


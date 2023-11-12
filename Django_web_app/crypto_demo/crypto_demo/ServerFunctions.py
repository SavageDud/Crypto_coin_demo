# -*- coding: utf-8 -*-

# this function checks a string for potential dangerouse_characters that could end up ad xlss attack
def XSS_Sanitize(string_):
    dangerouse_chars = {">" : "tri",
                        "<" : "retri",
                        "'" : "qht",
                        '"' : "dqht"}
    new_str =""
    for x in string_:
        if(x in dangerouse_chars.keys()):
            new_str+= dangerouse_chars[x]
        else:
            new_str+= x
    return new_str
    
    


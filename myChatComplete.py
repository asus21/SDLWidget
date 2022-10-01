import readline
import re


HISTORY = '.myChat_history'

readline.parse_and_bind("tab:complete")
list=["exit","quit","close","kick","link","client","linked","linking"]

temp=[]
def func(text,state):
    global temp
    response=None
    if(state==0):
        if(text):
            temp=sorted(h for h in list if h and h.startswith(text))
        else:
            temp=[]
    try:
        response=temp[state]
    except:
        response=None
    return response
   
readline.set_completer(func)
readline.set_completer_delims("/")

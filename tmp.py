import signal
import sys
if sys.platform=="win32":
    signal.SIGINT=signal.CTRL_C_EVENT
# 自定义信号处理函数
def my_handler(signum, frame):
    global stop
    stop = True
    print("终止")
def new_handler(signum,frame):
    print("ok")
 
# 设置相应信号处理的handler
signal.signal(signal.SIGINT,my_handler)    #读取Ctrl+c信号
signal.signal(signal.SIGINT,new_handler)    #读取Ctrl+c信号
# signal.signal(signal.SIGHUP, my_handler)    
# signal.signal(signal.SIGTERM, my_handler)
 
stop = False
 
while True:
    try:
        #读取到Ctrl+c前进行的操作
        if stop:
            # 中断时需要处理的代码
            break    #break只能退出当前循坏
            #中断程序需要用 raise
    except Exception as e:
        print(str(e))
        break
'''
补充：

键盘和shell的交互：

Ctrl-c Kill foreground process 常用 ;送SIGINT信号，默认进程会结束，但是进程自己可以重定义收到这个信号的行为。

Ctrl-z Suspend foreground process;送SIGSTOP信号，进程只是被停止，再送SIGCONT信号，进程继续运行。

Ctrl-d Terminate input, or exit shell 常用 有时也会使程序退出，例如没有参数的cat命令，从终端读一行显示一行，知道Ctrl+D终结输入并终结进程;不是发送信号，而是表示一个特殊的二进制值，表示 EOF。

Ctrl-s Suspend output

Ctrl-q Resume output

Ctrl-o Discard output

Ctrl-l Clear screen

控制字符都是可以用(stty命令)更改的。可以用stty -a看看终端配置。

SIGHUP 1 A 终端挂起或者控制进程终止

SIGINT 2 A 键盘中断（如break键被按下）

SIGQUIT 3 C 键盘的退出键被按下

SIGILL 4 C 非法指令

SIGABRT 6 C 由abort(3)发出的退出指令

SIGFPE 8 C 浮点异常

SIGKILL 9 AEF Kill信号

SIGSEGV 11 C 无效的内存引用

SIGPIPE 13 A 管道破裂: 写一个没有读端口的管道  S

IGALRM 14 A 由alarm(2)发出的信号

SIGTERM 15 A 终止信号 

SIGUSR1 30,10,16 A 用户自定义信号1 

SIGUSR2 31,12,17 A 用户自定义信号2 

SIGCHLD 20,17,18 B 子进程结束信号 

SIGCONT 19,18,25 进程继续（曾被停止的进程） 

SIGSTOP 17,19,23 DEF 终止进程 

SIGTSTP 18,20,24 D 控制终端（tty）上按下停止键 

SIGTTIN 21,21,26 D 后台进程企图从控制终端读 

SIGTTOU 22,22,27 D 后台进程企图从控制终端写

处理动作一项中的字母含义如下: 

A 缺省的动作是终止进程 

B 缺省的动作是忽略此信号 

C 缺省的动作是终止进程并进行内核映像转储（dump core） 

D 缺省的动作是停止进程 

E 信号不能被捕获 

F 信号不能被忽略

参考：https://cloud.tencent.com/developer/article/1565135
'''

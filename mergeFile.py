rfile = open('shengyu.txt', 'r')
wfile = open('wangzhademadai.txt', 'a+')

for line in rfile.readlines():
    wfile.writelines(line)

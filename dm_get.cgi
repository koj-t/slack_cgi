#!/home/kojima/cgi/bin/python
# coding:utf-8

import twitter_methods as tm

if __name__ == "__main__":
    print "Content-Type: text/html\n"
    text=tm.get_dm(1,True)
    print text

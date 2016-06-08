import os
import sys

pid = os.fork()

if pid == 0:
    for i in range(50):
        print(str(i))
    print("finished")
else:
    print("this is parent")
    os.wait()
    print("parent exit")

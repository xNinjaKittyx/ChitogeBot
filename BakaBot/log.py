
from datetime import datetime
import os


def output(a):
    """ Output the string 'a' """
    today = datetime.today()
    filename = "log-{0}-{1}-{2}.log".format(str(today.month), str(today.day),str(today.year))
    prefix = "[{0}:{1}:{2}]: ".format(str(today.hour),str(today.minute),str(today.second))
    if not os.path.exists('./logs'):
        os.makedirs('./logs')
    print(prefix + a)
    with open('./logs/' + filename, 'a') as f:
        f.write(prefix + a + "\n")
        f.close()

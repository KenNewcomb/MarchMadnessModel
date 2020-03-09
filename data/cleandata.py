import os

def cleandata():
    fs = [f for f in os.listdir('data') if 'data' in f]

    for f in fs:
        print("Processing ", f)
        os.system("""vim -c ':%s///e | :wq!' data/{}""".format(f))

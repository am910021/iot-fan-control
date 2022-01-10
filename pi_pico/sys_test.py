import sys, time

if __name__ == '__main__':
    count=0
    while True:
        if count > 10:
            sys.exit(0)
        count+=1
        time.sleep(0.1)
import os

def print_general():
    fs_stat = os.statvfs('/')
    fs_size = fs_stat[0] * fs_stat[2]
    fs_free = fs_stat[0] * fs_stat[3]
    print("File System Size {:.2f} KB - Free Space {:.2f} KB".format(fs_size/1024, fs_free/1024))

def print_esp8266():
    import esp
    blksize = os.statvfs('/')[0]
    fbs = uos.statvfs('/')[3]
    print ("Avilable storage is:",(blksize*fbs)/1024, "KB", "out of:", esp.flash_size()/1024,"KB",sep=" ")

if __name__ == '__main__':
    name = os.uname()
    print('Board: %s' % (name[4]))
    print_general()
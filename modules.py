#modules.py

#STVSecuritySystem###############################

# checking drivers license of STV
def checkLicense():
    from subprocess import getstatusoutput
    uuid = (getstatusoutput('wmic csproduct get uuid /format:list')[1])
    uuid = uuid.replace('UUID=', '')
    uuid = uuid.strip()
    uuid_splitted = uuid.split('-')
    wakeupkey = 0

    for wakeupkey_elem in uuid_splitted:
        wakeupkey += int(wakeupkey_elem, 16)
    wakeupkey = str(wakeupkey * int('c0ff1e', 16) ** 3)
    try:
        with open('inifiles/_KEEP_ON_THINKING.stv', mode='r', encoding='utf-8-sig') as licensefile:
            wakeupkey_pair = licensefile.readline()
    except:
        return 0
    if wakeupkey != wakeupkey_pair:
        return -1
    else:
        return 1

#Handlers########################################

# handling dll
def dllHandler(dll_path):
    from ctypes import windll
    dll_handle = windll.LoadLibrary(dll_path)
    if dll_handle == -1:
        print(nowTime(), f'{"dllHandler":12}: ' + dll_path + ' loading failed...')
        return -1
    #print(nowTime(), f'{"dllHandler":12}: {dll_handle}')
    return dll_handle

# handling device
def devHandler(dll, dev_name, flag):
    from ctypes import c_void_p, c_char_p, c_ulong
    dev_handle = c_void_p(dll.DioOpen(c_char_p(dev_name), c_ulong(flag)))
    if dev_handle == -1:
        print(nowTime(), f'{"devHandler":12}: ' + dev_name + ' handling failed...')
        return -1
    #print(nowTime(), f'{"devHandler":12}: {dev_handle}')
    return dev_handle

#Threads#########################################

# create threads by variable name
def createThread(_target, _args):
    from threading import Thread
    if isinstance(_target, str):
        _thread = Thread(target=eval(_target), args=_args)
    else:
        _thread = Thread(target=_target, args=_args)
    _thread.setDaemon(True)
    _thread.start()
    return _thread

# event trigger by variable name
def eventTrigger(event_name):
    if not eval(event_name).is_set():
        eval(event_name).set()

#Others##########################################

# round with cut under 4 and add over 5
roundInt_core = lambda t: int((t * 2 + 1) // 2)
def roundInt(num):
    result = roundInt_core(num)
    return result

# time of time
def nowTime():
    from time import strftime, localtime
    return strftime('%H:%M:%S ', localtime())

# decimal convert to binary list
def num2binList(_num, length):
    from copy import deepcopy
    bin_list = []
    num = deepcopy(int(_num))
    while True:
        t = int(num % 2)
        bin_list.append(t)
        num = (num - t) / 2
        if num == 0:
            break
    if len(bin_list) < length:
        for _ in range(length - len(bin_list)):
            bin_list.append(0)
    return bin_list

# get my IPaddr
def getMyIP():
    import netifaces
    MyIP = '123.456.789.000'
    onetime = 1
    for interface in netifaces.interfaces():
        if not onetime:
            break
        try:
            IPaddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
        except:
            continue
        if '192.168' in IPaddr:
            MyIP = IPaddr
            onetime = 0
    return MyIP

# get my network IPaddr
def getMyNetworkIP():
    my_ip = '123.456.789.000'
    ret, netwks = readConfigSection('inifiles/networks.ini', 'MYSELF')
    if ret:
        my_ip = netwks.get('my_network_ip')
    return my_ip

# get my network Port
def getMyNetworkPort():
    my_port = 5000
    ret, netwks = readConfigSection('inifiles/networks.ini', 'MYSELF')
    if ret:
        my_port = netwks.getint('my_network_port') # int!!!
    return my_port

# get stv_id
def getStvId():
    stv_id = 'STV_ANONYMOUS'
    ret, num_plate = readDefault('inifiles/number_plate.ini')
    if ret:
        stv_id = num_plate.get('stv_id')
    return stv_id

# get stv_section
def getStvSection():
    stv_section = 'section0'
    ret, num_plate = readDefault('inifiles/number_plate.ini')
    if ret:
        stv_section = num_plate.get('stv_section')
    return stv_section

# get stv_num
def getStvNum():
    stv_num = 0
    ret, num_plate = readDefault('inifiles/number_plate.ini')
    if ret:
        stv_num = num_plate.getint('stv_num')
    return stv_num

# get stv_section
def getStvHomeNum():
    home_no = '0'
    ret, num_plate = readDefault('inifiles/number_plate.ini')
    if ret:
        home_no = num_plate.get('home_no')
    return home_no

# get server_ip
def getServerIP():
    server_ip = '123.456.789.000'
    ret, netwks = readConfigSection('inifiles/networks.ini', 'SERVER')
    if ret:
        server_ip = netwks.get('server_ip')
    return server_ip

# get wsock_port
def getWSockPort():
    wsock_port = 0
    ret, netwks = readConfigSection('inifiles/networks.ini', 'SERVER')
    if ret:
        wsock_port = netwks.getint('wsock_port')
    return wsock_port

# get sock_port
def getSockPort():
    sock_port = 0
    ret, netwks = readConfigSection('inifiles/networks.ini', 'SERVER')
    if ret:
        sock_port = netwks.getint('sock_port')
    return sock_port

def getWhiteList():
    white_list = ['all']
    ret, _white_list = readDefaultList('inifiles/white_list.ini', 'white_list')
    if ret:
        white_list = _white_list
    return white_list

# architecture check
def archiCheck():
    from sys import maxsize
    if maxsize > 2 ** 32:
        return 64
    else:
        return 32

# reading initialize file by filename RAW
def readConfigRaw(file_name):
    import configparser
    import codecs
    readed = configparser.ConfigParser(inline_comment_prefixes=(';', ))
    readed.optionxform = str
    try:
        readed.readfp(codecs.open(file_name, 'r', 'utf-8'))
    except:
        readed = {}
    return readed

# reading needed section of initialize file by filename
def readConfigSection(file_name, keyname):
    readed = readConfigRaw(file_name)
    if not len(readed):
        ret = 0
    else:
        ret = 1
        readed = readed[keyname]
    return ret, readed

# reading DEFAULT section of initialize file by filename
def readDefault(file_name):
    readed = readConfigRaw(file_name)
    if not len(readed):
        ret = 0
    else:
        ret = 1
        readed = readed['DEFAULT']
    return ret, readed

# overwrite configs by other ini files
def configOverWriter(file_name, dicts):
    ret, patch = readDefault(file_name)
    if ret:
        for key in dicts:
            value = patch.get(key)
            if patch.get(key) != None:
                dicts[key] = value

# save initializes to filename
def writeDefault(file_name, dicts):
    dicts_CP = {'DEFAULT': dicts}
    import configparser
    inits = configparser.ConfigParser()
    inits.optionxform = str
    inits.read_dict(dicts_CP)
    with open(file_name, mode='w') as fp:
        inits.write(fp)

# reading list in DEFAULT section of split by space
def readDefaultList(file_name, key_name):
    _ret, readed = readDefault(file_name)
    if _ret and readed.get(key_name) != None:
        ret = 1
        result = readed.get(key_name).split()
    else:
        ret = 0
        result = []
    return ret, result

# mode wrapper by inifiles/mode_patch.ini
def applyModepatch(settings, modepatch):
    for keyS in settings:
        for keyM in modepatch:
            if keyM == keyS:
                settings[keyS] = modepatch[keyM]
    return settings

# get initialize value by key and value type. MUST CONFIGPARSER!!
def isExtendedIni(ini_default, ini_extension, key, val_type='int'):
    val_extension = eval('ini_extension.get' + val_type + '(key)')
    val_default = eval('ini_default.get' + val_type + '(key)')
    if val_extension != None:
        return val_extension
    else:
        return val_default

# remove all A from list
def removeAllFromList(lst, key):
    while key in lst:
        lst.remove(key)
    return lst

if __name__ == '__main__':
    print('this is module')
    print(dir())

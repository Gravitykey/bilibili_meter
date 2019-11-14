import sys
from bilibili_meter.web_server.model import WebUser


def new_web_user(name, password):
    us = WebUser.findAll(where='`name`=?', args=(name, ))
    if len(us) != 0:
        return 'ERROR:USER ALREADY EXIST'
    WebUser.new(name, password)


def set_password(name, password):
    us = WebUser.findAll(where='`name`=?', args=(name, ))
    if len(us) == 0:
        return "ERROR:CAN'T FIND USER %s" % (name, )
    u = us[0]
    u.passwd = u.calc_pw(password)
    u.update()


def set_admin(name, admin):
    if str(admin).lower() == 'true':
        admin=True
    elif str(admin).lower() == 'false':
        admin=False
    else:
        return "the thrid arg must be 'true' or 'false'"
    us = WebUser.findAll(where='`name`=?', args=(name, ))
    if len(us) == 0:
        return "ERROR:CAN'T FIND USER %s" % (name, )
    u = us[0]
    u.admin = admin
    u.update()


def show_help():
    fname = sys.argv[0]
    print('Usage:\n    python %s [option] [args]...' % fname)
    print('        -add [name] [password]           create new user')
    print('        -setpassword [name] [password]   set the password')
    print('        -setadmin [name] [true/false]    set admin')


if __name__=='__main__':
    options = ['-add','-setpassword','-setadmin']
    maps = {'-add':new_web_user,
            '-setpassword':set_password,
            '-setadmin':set_admin}
    
    if len(sys.argv)!=4 or not sys.argv[1] in options:
        show_help()
    else:
        fun = maps.get(sys.argv[1],None)
        if not fun:
            print('ERROR:UNKNOWN OPTION')
        else:
            message = fun(sys.argv[2],sys.argv[3])
            if message:
                print(message)

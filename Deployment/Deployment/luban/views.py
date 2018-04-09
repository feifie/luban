from django.shortcuts import render, redirect, HttpResponse
import json
from luban import models
# from luban.plugins.runcmd import SSHConnection
from luban.plugins.runcmd import commands


# Create your views here.

def login(request):
    message = " "
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        sessiondate = request.POST.get('sessiondate')
        status = models.AdminInfo.objects.filter(username=username, password=password).first()
        print(status)
        if status:
            request.session['username'] = username
            request.session['is_login'] = True
            if sessiondate == '1':
                request.session.set_expiry(60 * 60 * 24 * 14)
            return redirect('/index.html')
        else:
            message = "用户名或者密码错误"
            return render(request, 'login.html', {'message': message})


def logout(request):
    request.session.clear()
    return redirect('/login.html/')


def auth(func):
    def inner(request, *args, **kwargs):
        se = request.session.get('is_login', None)
        if not se:
            return redirect('/login.html/')
        return func(request, *args, **kwargs)

    return inner


@auth
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


@auth
def business(request):
    if request.method == 'GET':
        business_list = models.Business.objects.all()
        return render(request, 'business.html', {'business_list': business_list})

def BusinessJson(request):
    response = {'status': False, 'message': 'None'}
    print(request.POST.get('bid'))
    print(request.POST.get('bustext'))
    bid = request.POST.get('bid')
    bustext = request.POST.get('bustext')
    print(type(bustext))
    if len(bid)<=0:
        response['message']='业务线名称不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    if len(str(bustext))<=0:
        response['message']='业务描述不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))

    models.Business.objects.create(name=bid,note=bustext)
    response['message']='数据添加成功'
    response['status']=True
    return HttpResponse(json.dumps(response,ensure_ascii=False))

def BusinessdelJson(request):
    response = {'status': False, 'message': 'None'}
    bid =request.POST.get('nid')
    if len(bid)>0:
        models.Business.objects.filter(id=bid).delete()
        response['message']='数据删除成功'
        response['status']=True
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    else:
        response['message']='删除没有成功，请检查配置'
        return HttpResponse(json.dumps(response,ensure_ascii=False))

def BusinesseditJson(request):
    response = {'status': False, 'message': 'None'}
    print(request.POST.get('uid'))
    print(request.POST.get('name'))
    print(request.POST.get('bustext'))
    uid = request.POST.get('uid')
    name = request.POST.get('name')
    bustext = request.POST.get('bustext')

    if len(str(name))==0:
        response['message']='业务线名称不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    if len(str(bustext))==0:
        response['message']='业务描述不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    else:
        models.Business.objects.filter(id=uid).update(name=name,
                                                      note=bustext)
        response['status']=False
        response['message']='数据修改成功！'
        return HttpResponse(json.dumps(response, ensure_ascii=False))


@auth
def server(request):
    if request.method == 'GET':
        serv_list = models.Server.objects.all()
        business_list = models.Business.objects.all()
        return render(request, 'server_info.html', {'serv_list': serv_list,'business_list':business_list})

def ServerCheckJson(request):
    response = {'status': False, 'message': 'None'}
    #获取前端发来的命令
    cmd = request.POST.get('cmd')
    print(cmd)
    #获取选中的所有主机的id
    hosts = request.POST.get('hosts')
    hosts_list = models.Server.objects.filter(id=hosts).all()
    print(hosts_list)
    for host in hosts_list:
        print(host.hostIP)
    from luban.plugins.test import SSHConnection
    try:
        obj = SSHConnection(hostname=host.hostname, hostip=host.hostIP, port=host.hostport, user=host.hostuser,
                            pwd=host.hostpwd)
        ret = obj.commands(cmd=cmd)
        response['status']=True
        response['message'] = '主机[%s]:状态正常 '%host.hostname
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    except Exception as e:
        response['message']='主机[%s]: %s'%(host.hostname,str(e))
        return HttpResponse(json.dumps(response,ensure_ascii=False))

def ServerSaveUserJson(request):
    response = {'status': True, 'message': 'None'}
    name = request.POST.get('sname')
    port = request.POST.get('sport')
    tag = request.POST.get('stag')
    user = request.POST.get('suser')
    pwd = request.POST.get('spwd')
    sqluser = request.POST.get('ssuser')
    sqlpwd = request.POST.get('sspwd')
    mip = request.POST.get('sip')
    sbusid = request.POST.get('sbusid')
    print(name,port,tag,user,pwd,sqluser,sqlpwd,mip,sbusid)
    if len(name)==0 or len(user)==0 or len(pwd)==0 or len(mip)==0:
        response['status']=False
        response['message']='数据不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    else:
        obj=models.Server.objects.create(hostname=name,
                                     hostuser=user,
                                     hostpwd=pwd,
                                     hostport=port,
                                     hostIP=mip,
                                     hosttag=tag,
                                     sqluser=sqluser,
                                     sqlpwd=sqlpwd,
                                     business_id=sbusid)
        if obj:
            response['message']='数据录入成功'
            return HttpResponse(json.dumps(response,ensure_ascii=False))
        else:
            response['status']=False
            response['message']='数据写入失败！'
            return HttpResponse(json.dumps(response,ensure_ascii=False))

def ServerDelServerJson(request):
    response = {'status': True, 'message': 'None'}
    sid = request.POST.get('nid')
    print(sid)
    obj=models.Server.objects.filter(id=sid).delete()
    if obj:
        response['message']='删除成功'
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        response['status']=False
        response['message']='错误，删除不成功！请联系管理员'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

def ServerEditServerJson(request):
    response = {'status': True, 'message': 'None'}
    print(request.POST)
    try:
        nid = request.POST.get('nid')
        name = request.POST.get('name')
        user = request.POST.get('user')
        ip = request.POST.get('ip')
        port = request.POST.get('port')
        pwd = request.POST.get('pwd')
        sqlpwd = request.POST.get('sqlpwd')
        sqluser = request.POST.get('sqluser')
        tag = request.POST.get('tag')
        cls_id = request.POST.get('cls_id')
        print(nid,name,user,ip,port,pwd,sqluser,sqlpwd,tag,cls_id)
        models.Server.objects.filter(id=nid).update(
            hostname=name,
            hostuser=user,
            hostpwd=pwd,
            hostport=port,
            hostIP=ip,
            hosttag=tag,
            sqluser=sqluser,
            sqlpwd=sqlpwd,
            business=cls_id
        )
        # response['message']='ok'
        # return HttpResponse(json.dumps(response, ensure_ascii=False))
    except Exception as e:
        response['status']=False
        response['message']=str(e)
    return HttpResponse(json.dumps(response, ensure_ascii=False))

@auth
def Environment(request):
    serv_type = models.ServType.objects.all()
    serv_list = models.Server.objects.all()
    t_list = models.Tools.objects.all()
    return render(request, 'Environment.html', {'serv_type': serv_type, 'serv_list': serv_list, 't_list': t_list})


def runserver(request):
    # print(request.POST)
    # print(request.POST.get('cmd'))
    response = {'status': True, 'message': 'None'}
    try:
        cmd = request.POST.get('cmd')
        hid = request.POST.get('server')
        sid = request.POST.get('software')
        print(cmd)
        print(hid)
        print(sid)
        file = models.ServType.objects.all()
        for item in file:
            print(item.software)
        obj = models.Server.objects.filter(id=hid).all()
        for row in obj:
            host = row.hostname
            ip = row.hostIP
            user = row.hostuser
            pwd = row.hostpwd
            port = row.hostport
            print(ip, user, pwd, port, cmd)
            # ret = commands(host=ip,port=port,user=user,pwd=pwd,cmd=cmd)
            # response['message']=ret
            # result = json.dumps(response)
            # return HttpResponse(result)
            from luban.plugins.test import SSHConnection
            obj = SSHConnection(hostname=host, hostip=ip, port=port, user=user, pwd=pwd)
            ret = obj.commands(cmd=cmd)
            response['message'] = ret
            result = json.dumps(response)
            return HttpResponse(result)
    except Exception as e:
        response['status'] = False
        response['message'] = '%s执行失败！错误信息：%s' % (host, e)
    result = json.dumps(response, ensure_ascii=False)
    return HttpResponse(result)

# send remote server software
def sendremoteserver(request):
    response = {'status': True, 'message': 'None'}
    from Deployment import settings
    try:
        hid = request.POST.get('remothid')
        filepath = settings.LOCAL_PATH
        filename = request.POST.get('softw')
        print(filename)
        print(filepath)
        localfile ='%s/%s'%(filepath,filename)
        print(localfile)
        sid = request.POST.get('sid')
        obj = models.Server.objects.filter(id=hid).all()
        for row in obj:
            host = row.hostname
            print(host)
            ip = row.hostIP
            user = row.hostuser
            pwd = row.hostpwd
            port = row.hostport
            from luban.plugins.test import SSHConnection
            obj = SSHConnection(hostname=host, hostip=ip, port=port, user=user, pwd=pwd)
            # 设置远程目录
            # cmd = "'remote_data='/data'\nif [ -d $mysqldir ]then\necho '目录已经创建'\nelse\nmkdir $mysqldir;fi'"
            # obj.commands(cmd)
            remote_path = '/data/%s' % filename
            # print(remote_path)
            ret = obj.transfile(localfile, remote_path)
            response['message'] = ret
            result = json.dumps(response, ensure_ascii=False)
            return HttpResponse(result)
    except Exception as e:
        response['status'] = False
        response['message'] = '执行失败！错误信息：%s' % e
        # response['message']='%s执行失败！错误信息：%s'%(host,e)
    result = json.dumps(response, ensure_ascii=False)
    return HttpResponse(result)

@auth
def software(request):
    sof = models.ServType.objects.all()
    return render(request, 'software.html', {'sof': sof})

def SoftSendFilesJson(request):
    import os
    response = {'status':True,'message':'None'}
    ServName = request.POST.get('ServName')
    # 应改为自动获取该值SoftFile.name
    SoftName = request.POST.get('SoftName')
    SoftCmd = request.POST.get('SoftCmd')
    SoftFile = request.FILES.get('SoftFile')
    print(ServName)
    print(SoftName)
    print(SoftCmd)
    # print(SoftFile)
    # print(SoftFile.name)

    if len(str(ServName)) ==0:
        response['status']=False
        response['message']='代码名称不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    if not SoftFile:
        response['status']=False
        response['message']='上传数据不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))

    file_name = SoftFile.name
    file_abs_name = os.path.join("software", file_name)
    # 上传文件大小
    file_size = SoftFile.size
    print(file_size)
    # 存储的文件名
    print(file_abs_name)
    try:
        with open(file_abs_name,'wb') as f:
            for chunk in SoftFile.chunks():
                f.write(chunk)
        response['message']='上传成功！'
    except Exception as e:
        response['status']=False
        response['message']=str(e)
        return HttpResponse(json.dumps(response,ensure_ascii=False))

    models.ServType.objects.create(name=ServName,softname=file_name,software=file_abs_name,commands=SoftCmd)
    return HttpResponse(json.dumps(response,ensure_ascii=False))

def SoftDelFilesJson(request):
    response = {'status':True,'message':'None'}
    nid = request.POST.get('nid')
    print(nid)
    if len(nid)==0:
        response['status']=False
        response['message']='数据不能为空我的哥'
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        models.ServType.objects.filter(id=nid).delete()
        response['message']='脚本删除成功！'
        return HttpResponse(json.dumps(response,ensure_ascii=False))

def SoftEditJson(request):
    response = {'status':True,'message':'None'}
    sid = request.POST.get('sid')
    name = request.POST.get('name')
    note = request.POST.get('note')
    cmd = request.POST.get('cmd')
    print(sid)
    print(name)
    print(note)
    print(cmd)
    if len(sid)==0 or len(name)==0 or len(cmd)==0:
        response['status']=False
        response['message']='数据不能为空我的哥'
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        models.ServType.objects.filter(id=sid).update(name=name,note=note,commands=cmd)
        response['message']='保存成功！'
        return HttpResponse(json.dumps(response,ensure_ascii=False))


def Toolsrunscript(request):
    serv_list = models.Server.objects.all()
    sert_list = models.Tools.objects.all()
    return render(request,'tools_runscript.html',{'sert_list':sert_list,'serv_list':serv_list})

def ToolsRunScriptJson(request):
    response = {'status':True,'message':'None'}
    hosts_list = request.POST.get('hosts')
    sid = request.POST.get('sid')
    sobj = models.Tools.objects.filter(id=sid).all()
    #获取脚本信息
    for s in sobj:
        print(s.script)
        print(s.name)
    print(sid)
    # 获取主机信息
    hobj = models.Server.objects.filter(id=hosts_list).all()
    for h in hobj:
        print(h.hostIP)
    # 引入parimiko
    from luban.plugins.test import SSHConnection
    try:
        obj=SSHConnection(hostname=h.hostname, hostip=h.hostIP, port=h.hostport, user=h.hostuser, pwd=h.hostpwd)
        cmd = "echo '%s' > /tmp/%s && sh /tmp/%s"%(s.script,s.name,s.name)
        ret = obj.commands(cmd)
        #response['message'] = ret.split('\n')
        response['message'] = str(ret) + '%s'%h.hostname
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    except Exception as e:
        response['status'] = False
        response['message'] = '%s执行失败！错误信息：%s' % (h.hostname, e)
        return HttpResponse(json.dumps(response,ensure_ascii=False))


def Batchexecution(request):
    response = {'status': True, 'message': 'None'}
    try:
        # print(request.POST)
        # print(request.POST.get('hosts'))
        # print(request.POST.get('sfid'))
        host_list = request.POST.get('hosts')
        sfid_list = request.POST.get('sfid')
        from Deployment import settings
        filepath = settings.LOCAL_PATH
        file = models.ServType.objects.filter(id=sfid_list)
        for row in file:
            from Deployment import settings
            filename = row.softname
        print(filepath)
        print(filename)
        localfile = '%s/%s'%(filepath,filename)

        obj = models.Server.objects.filter(id=host_list).all()
        for i in obj:
            print(i.hostIP, i.hostport, i.hostuser, i.hostpwd)
            print('-----------------------------------')
            from luban.plugins.test import SSHConnection
            obj = SSHConnection(hostname=i.hostname, hostip=i.hostIP, port=i.hostport, user=i.hostuser, pwd=i.hostpwd)
            # 发送文件
            remote_path = '/data/%s' % filename
            # print(remote_path)
            ret = obj.transfile(localfile, remote_path)
            response['message'] = ret
        # print(obj)
        result = json.dumps(response, ensure_ascii=False)
        return HttpResponse(result)
    except Exception as e:
        response['status'] = False
        response['message'] = '执行失败！错误信息：%s' % e
        # response['message']='%s执行失败！错误信息：%s'%(host,e)
    result = json.dumps(response, ensure_ascii=False)
    return HttpResponse(result)

def CmdShell(request):
    response = {'status': True, 'message': 'None'}
    cmd = request.POST.get('cmd')
    host_list = request.POST.get('hosts')
    print(host_list)
    hosts = models.Server.objects.filter(id=host_list).all()
    for host in hosts:
        print(host.hostIP)
        from luban.plugins.test import SSHConnection
        try:
            obj=SSHConnection(hostname=host.hostname, hostip=host.hostIP, port=host.hostport, user=host.hostuser, pwd=host.hostpwd)
            ret = obj.commands(cmd)
            response['message'] = ret.split('\n')
            return HttpResponse(json.dumps(response,ensure_ascii=False))
        except Exception as e:
            response['status'] = False
            response['message'] = '%s执行失败！错误信息：%s' % (host.hostname, e)
            return HttpResponse(json.dumps(response,ensure_ascii=False))
    result = json.dumps(response, ensure_ascii=False)
    return HttpResponse(result)

@auth
def tools(request):
    t_list = models.Tools.objects.all()
    return render(request, 'tools.html', {'t_list': t_list})


def SendScriptJson(request):
    response = {'status': True, 'message': 'None'}
    print(request.POST.get('name'))
    print(request.POST.get('script'))
    print(request.POST.get('snote'))
    name = request.POST.get('name')
    script = request.POST.get('script')
    snote = request.POST.get('snote')
    if len(name)==0 or len(script)==0:
        response['status']=False
        response['message']='数据不能为空'
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        models.Tools.objects.create(name=name,script=script,note=snote)
        response['message']='脚本添加成功！'
        return HttpResponse(json.dumps(response, ensure_ascii=False))


def DelScriptJson(request):
    response = {'status': True, 'message': 'None'}
    print(request.POST.get('nid'))
    nid = request.POST.get('nid')
    if len(nid)==0:
        response['status']=False
        response['message']='数据不能为空我的哥'
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        models.Tools.objects.filter(id=nid).delete()
        response['message']='脚本删除成功！'
        return HttpResponse(json.dumps(response))

def EditScriptJson(request):
    response = {'status': True, 'message': 'None'}
    print(request.POST.get('nid'))
    print(request.POST.get('name'))
    print(request.POST.get('script'))
    print(request.POST.get('note'))
    nid = request.POST.get('nid')
    name = request.POST.get('name')
    script = request.POST.get('script')
    note = request.POST.get('note')
    if len(name)==0 or len(script)==0:
        response['status']=False
        response['message']='数据不能为空'
        return HttpResponse(json.dumps(response, ensure_ascii=False))
    else:
        models.Tools.objects.filter(id=nid).update(name=name,
                                                   script=script,
                                                   note=note)
        response['message']='脚本修改成功！'
        return HttpResponse(json.dumps(response, ensure_ascii=False))

def Runscript(request):
    response = {'status': True, 'message': 'None'}
    hosts_list = request.POST.get('hosts')
    jf_list = request.POST.get('jid')
    jfile = models.Tools.objects.filter(id=jf_list).all()
    # 脚本文件信息
    for s in jfile:
        print(s.script)
    # 服务器信息
    hosts = models.Server.objects.filter(id=hosts_list).all()
    for h in hosts:
        print(h.hostname, h.hostIP)
        #创建并执行脚本文件
    from luban.plugins.test import SSHConnection
    try:
        obj=SSHConnection(hostname=h.hostname, hostip=h.hostIP, port=h.hostport, user=h.hostuser, pwd=h.hostpwd)
        cmd = "echo '%s' > /tmp/%s && sh /tmp/%s"%(s.script,s.name,s.name)
        ret = obj.commands(cmd)
        #response['message'] = ret.split('\n')
        response['message'] = str(ret) + '%s'%h.hostname
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    except Exception as e:
        response['status'] = False
        response['message'] = '%s执行失败！错误信息：%s' % (h.hostname, e)
        return HttpResponse(json.dumps(response,ensure_ascii=False))

@auth
def Codesinfo(request):
    sql_list = models.SqlDB.objects.all()
    code_list = models.CodesDB.objects.all()
    business_list = models.Business.objects.all()

    return render(request, 'Codes_info.html',{'sql_list':sql_list,'code_list':code_list,
                                              'business_list':business_list})

def CodesSendFilesJson(request):
    import os
    response = {'status':True,'message':'None'}
    codename = request.POST.get('codesname')
    busid = request.POST.get('busid')
    codesfile = request.FILES.get('codefile')
    print(busid)
    print(codename)
    print(codesfile)
    #print(request.body)
    print(request.FILES)
    if len(str(codename)) ==0:
        response['status']=False
        response['message']='代码名称不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    if not codesfile:
        response['status']=False
        response['message']='上传数据不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))

    file_name = codesfile.name
    file_abs_name = os.path.join("CodeDB", file_name)
    # 上传文件大小
    file_size = codesfile.size
    print(file_size)
    # 存储的文件名
    print(file_abs_name)
    try:
        with open(file_abs_name,'wb') as f:
            for chunk in codesfile.chunks():
                f.write(chunk)
        response['status']=True
        response['message']='上传成功！'
    except Exception as e:
        response['message']=str(e)
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    #存储到数据库
    models.CodesDB.objects.create(name=codename,codename=file_name,codefile=file_abs_name,business_id=busid)
    return HttpResponse(json.dumps(response,ensure_ascii=False))

def CodesSendSqlJson(request):
    response = {'status':True,'message':'None'}
    print(request.POST)
    sqlname = request.POST.get('sqlname')
    sqlcode = request.POST.get('sqlcode')
    uid = request.POST.get('buid')
    if len(sqlname)==0 or len(sqlcode)==0 or len(uid)==0:
        response['status']=False
        response['message']='数据不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    else:
        try:
            models.SqlDB.objects.create(name=sqlname,sqltext=sqlcode,business_id=uid)
            response['message']='数据添加成功'
            return HttpResponse(json.dumps(response,ensure_ascii=False))
        except Exception as e:
            response['status']=False
            response['message']=str(e)
            return HttpResponse(json.dumps(response,ensure_ascii=False))

def CodesDelSqlJson(request):
    response = {'status':True,'message':'None'}
    print(request.POST.get('nid'))
    nid = request.POST.get('nid')
    if nid == 0:
        response['status']=False
        response['message']='数据不能为空，请联系管理员！'
    else:
        models.SqlDB.objects.filter(id=nid).delete()
        response['message']='数据删除成功'
        return HttpResponse(json.dumps(response,ensure_ascii=False))

def CodesDelCodJson(request):
    response = {'status':True,'message':'None'}
    print(request.POST.get('nid'))
    nid = request.POST.get('nid')
    if nid == 0:
        response['status']=False
        response['message']='数据不能为空，请联系管理员！'
    else:
        models.CodesDB.objects.filter(id=nid).delete()
        response['message']='数据删除成功'
        return HttpResponse(json.dumps(response,ensure_ascii=False))

def CodesBackSqlJson(request):
    response = {'status':True,'message':None}
    print(request.POST)
    hid = request.POST.get('hid')
    obj = models.Server.objects.filter(id=hid).all()
    for i in obj:
        print(i.sqluser,i.sqlpwd)
    # backsql='--all-databases > /tmp/all.sql  && echo $? && netstat -ntpl | grep 3306'
    # cmd='mysqldump -h%s -u%s -p%s %s'%(i.hostIP,i.sqluser,i.sqlpwd,backsql)
    cmd = 'netstat -ntpl | grep 3306'
    print(cmd)
    from luban.plugins.test import SSHConnection
    try:
        obj=SSHConnection(hostname=i.hostname, hostip=i.hostIP, port=i.hostport, user=i.hostuser, pwd=i.hostpwd)
        ret = obj.commands(cmd)
        print(ret)
        response['message']=str(ret)
    except Exception as e:
        response['status']=False
        response['message']=str(e)
    return HttpResponse(json.dumps(response,ensure_ascii=False))

@auth
def CodesRelease(request):
    code_list = models.CodesDB.objects.all()
    host_list = models.Server.objects.all()
    host_db_list = models.Server.objects.filter(hosttag='mysql').all()
    print(host_db_list)
    sql_list = models.SqlDB.objects.all()
    return render(request,'Codes_Release.html',{'code_list':code_list,'host_list':host_list,
                                                'sql_list':sql_list,'host_db_list':host_db_list})

def CodesJsonRelease(request):
    response = {'status':True,'message':'None'}
    print(request.POST)
    hid_list = request.POST.get('hosts')
    hobj = models.Server.objects.filter(id=hid_list).all()
    for h in hobj:
        print(h.hostIP,h.hostuser,h.hostport)
    cid = request.POST.get('cid')
    cobj = models.CodesDB.objects.filter(id=cid).first()
    # filepath = str(cobj.codefile)
    # #linux
    # filename = str(cobj.codefile).split('/')[1]
    from Deployment import settings
    filepath = settings.LOCAL_CODE_PATH
    filename = cobj.codename
    from Deployment.settings import REMOTE_WEBROOT_PATH
    remote_path = REMOTE_WEBROOT_PATH+'%s'%filename
    print(remote_path)
    localpathname='%s/%s'%(filepath,filename)
    from luban.plugins.test import SSHConnection
    try:
        obj = SSHConnection(hostname=h.hostname, hostip=h.hostIP, port=h.hostport, user=h.hostuser, pwd=h.hostpwd)
        # 打包的命令
        #cmd = 'cd /data/nginx/html/;touch `date+%Y%m%d`.txt; tar -czf `date +%Y-%m-%d_%H_%M_%S`.old.tar.gz * && mv * /tmp/'
        cmd = 'cd /data/nginx/html/&&tar -czf `date +%Y-%m-%d_%H_%M_%S`.old.tar.gz * ; mv * /tmp/'
        retcmd = obj.commands(cmd)
        ret = obj.transfile(localpathname, remote_path)
        # 解压缩的命令
        cmd2 = 'cd /data/nginx/html/&&tar xf %s && rm -rf %s && /data/nginx/sbin/nginx -s reload'%(filename,filename)
        obj.commands(cmd2)
        response['message']=ret
    except Exception as e:
        response['status']=False
        response['message']= '主机[%s]'%h.hostname + str(e)
    #链接服务器

    print(response)
    return HttpResponse(json.dumps(response,ensure_ascii=False))

def CodesJsonRestartNginx(request):
    response = {'status':True,'message':'None'}
    print(request.POST.get('hosts'))
    cmd = '/data/nginx/sbin/nginx -s reload&&netstat -ntpl | grep nginx '
    #cmd = 'uname -a'
    #获取到服务器
    hid_list = request.POST.get('hosts')
    hobj = models.Server.objects.filter(id=hid_list).all()
    for h in hobj:
        print(h.hostIP,h.hostuser,h.hostport)
    from luban.plugins.test import SSHConnection
    obj = SSHConnection(hostname=h.hostname, hostip=h.hostIP, port=h.hostport, user=h.hostuser, pwd=h.hostpwd)
    try:
        ret = obj.commands(cmd=cmd)
        print(ret)
        response['message'] = "主机[%s]"%h.hostname + ret
        result = json.dumps(response)
        return HttpResponse(result)
    except Exception as e:
        response['status']=False
        response['message']='主机[%s]：'%h.hostname + str(e)
    return HttpResponse(json.dumps(response,ensure_ascii=False))

def usermanage(request):
    user_list = models.UserProfile.objects.all()
    for u in user_list:
        print(u.name)
        print(u.email)
        print(u.wiexin)
    return render(request,'user_manage.html',{'user_list':user_list})

def UserManageJson(request):
    response = {'status': False, 'message': 'None'}
    print(request.POST.get('name'))
    name = request.POST.get('name')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    wiexin = request.POST.get('wiexin')
    if len(name)==0 or len(email)==0 or len(mobile)==0 or len(wiexin)==0:
        response['message']='数据不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    # if len(email)==0:
    #     response['message']='邮箱不能为空'
    # if len(mobile)==0:
    #     response['message']='联系方式不能为空'
    # if len(wiexin)==0:
    #     response['message']='微信不能为空'
    else:
        models.UserProfile.objects.create(name=name,email=email,mobile=mobile,wiexin=wiexin)
        response['status']=True
        response['message']='用户添加成功'

        return HttpResponse(json.dumps(response,ensure_ascii=False))

def DelUserJson(request):
    response = {'status':True,'message':'None'}
    print(request.POST.get('uid'))
    uid = request.POST.get('uid')
    try:
        models.UserProfile.objects.filter(id=uid).delete()
        response['message']='成功删除！'
    except Exception as e:
        response['status']=False
        response['message']='删除失败：%s'%str(e)
    return HttpResponse(json.dumps(response,ensure_ascii=False))

def EditUserJson(request):
    response = {'status': False, 'message': 'None'}
    print(request.POST.get('name'))

    uid = request.POST.get('uid')
    name = request.POST.get('name')
    email = request.POST.get('email')
    mobile = request.POST.get('mobile')
    wiexin = request.POST.get('wiexin')
    if len(name)==0 or len(email)==0 or len(mobile)==0 or len(wiexin)==0:
        response['message']='数据不能为空'
        return HttpResponse(json.dumps(response,ensure_ascii=False))
    else:
        models.UserProfile.objects.filter(id=uid).update(name=name,email=email,mobile=mobile,wiexin=wiexin)
        response['status']=True
        response['message']='用户添加成功'
        return HttpResponse(json.dumps(response,ensure_ascii=False))
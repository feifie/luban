from django.db import models

# Create your models here.


class Business(models.Model):
    name = models.CharField(max_length=32,verbose_name='业务线名称')
    note = models.TextField(null=True,blank=True,verbose_name='业务线说明')

    class Meta:
        verbose_name_plural = '业务线表'

    def __str__(self):
        return self.name




class Server(models.Model):
    hostname = models.CharField(max_length=32,verbose_name='服务器名称')
    hostuser = models.CharField(max_length=32,verbose_name='服务器管理用户')
    hostpwd = models.CharField(max_length=32,verbose_name='服务器密码')
    hostport = models.IntegerField(default=22,verbose_name='服务器端口')
    hostIP = models.GenericIPAddressField(verbose_name='服务器管理IP地址')
    hosttag = models.CharField(max_length=64,default='nginx',verbose_name='标签')
    sqluser = models.CharField(max_length=32,blank=True,null=True,verbose_name='sql用户')
    sqlpwd = models.CharField(max_length=64,blank=True,null=True,verbose_name='sql用户密码')
    business = models.ForeignKey('Business',related_name='business',verbose_name='所属业务')

    class Meta:
        verbose_name_plural = '服务器信息'

    def __str__(self):
        return self.hostname

class ServType(models.Model):
    name = models.CharField(max_length=32,verbose_name='服务名称')
    # 解决部署问题
    softname = models.CharField(blank=True,null=True,max_length=32,verbose_name='软件名称')
    software = models.FileField(upload_to='software')
    commands = models.TextField(verbose_name='命令')
    note = models.CharField(max_length=256,blank=True,null=True,verbose_name='软件描述')


    class Meta:
        verbose_name_plural = '服务信息'

    def __str__(self):
        return self.name

class Tools(models.Model):
    name = models.CharField(max_length=32,verbose_name='工具名称')
    #location = models.FileField(upload_to='tools',verbose_name='工具所在位置')
    script = models.TextField(blank=True,null=True,verbose_name='脚本')
    note = models.TextField(verbose_name='功能描述')

    class Meta:
        verbose_name_plural='工具信息表'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    name = models.CharField(max_length=32, verbose_name='姓名')
    email = models.EmailField(verbose_name='邮箱')
    mobile = models.CharField(max_length=32, verbose_name='手机')
    wiexin = models.CharField(max_length=64, null=True, blank=True, verbose_name='微信')

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.name


class AdminInfo(models.Model):
    user_info = models.OneToOneField("UserProfile")
    username = models.CharField(max_length=64, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')

    class Meta:
        verbose_name_plural = 'cmdb系统管理员'

    def __str__(self):
        return self.user_info.name


class SqlDB(models.Model):
    name = models.CharField(max_length=32,verbose_name='sql代码名称')
    sqltext = models.TextField(verbose_name='sql语句')
    business = models.ForeignKey('Business',verbose_name='所属业务')

    class Meta:
        verbose_name_plural='sql代码信息'

    def __str__(self):
        return self.name

class CodesDB(models.Model):
    # 存储位置在配置文件中定义
    name = models.CharField(max_length=32,verbose_name='显示名称')
    codename = models.CharField(blank=True,null=True,max_length=64,verbose_name='代码名称')
    codefile = models.FileField(upload_to='CodeDB', verbose_name='代码文件')
    business = models.ForeignKey('Business',verbose_name='所属业务')

    class Meta:
        verbose_name_plural='代码信息'

    def __str__(self):
        return self.name


# class Loginfo(models.Model):
#     username = models.ForeignKey('UserProfile',related_name='user',verbose_name='操作用户')
#     hostname = models.ForeignKey('Server',related_name='server',verbose_name='主机')
#     note = models.TextField(verbose_name='记录信息')
#     data = models.DateTimeField(auto_now_add=True,verbose_name='记录时间')
#
#     class Meta:
#         verbose_name_plural='日志信息表'
#     def __str__(self):
#         return "%s-%s"%(self.hostname,self.note)

"""Deployment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from luban import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login.html/', views.login),
    url(r'^logout.html/', views.logout),
    url(r'^index', views.index),
    url(r'^business.html/', views.business),
    url(r'^Business_Json/', views.BusinessJson),
    url(r'^Business_del_Json/', views.BusinessdelJson),
    url(r'^Business_edit_Json/', views.BusinesseditJson),
    url(r'^server_info.html/', views.server),
    url(r'^Server_CheckJson/', views.ServerCheckJson),
    url(r'^Server_SaveUserJson/', views.ServerSaveUserJson),
    url(r'^Server_Del_ServerJson/', views.ServerDelServerJson),
    url(r'^Server_Edit_ServerJson/', views.ServerEditServerJson),
    url(r'^run-server/', views.runserver),
    url(r'^send-remoteserver/', views.sendremoteserver),
    url(r'^Environment.html/', views.Environment),
    url(r'^software.html/', views.software),
    url(r'^Soft_SendFilesJson/', views.SoftSendFilesJson),
    url(r'^Soft_DelFilesJson/', views.SoftDelFilesJson),
    url(r'^Soft_Edit_Json/', views.SoftEditJson),
    url(r'^Batch_execution/', views.Batchexecution),
    url(r'^AllRun_CmdShell/', views.CmdShell),
    url(r'^tools.html/', views.tools),

    url(r'^tools_runscript.html/', views.Toolsrunscript),

    url(r'^Tools_SendScriptJson/', views.SendScriptJson),
    url(r'^Tools_Del_ScriptJson/', views.DelScriptJson),
    url(r'^Tools_Edit_ScriptJson/', views.EditScriptJson),

    url(r'^Tools_Run_ScriptJson/', views.ToolsRunScriptJson),

    url(r'^Run_script/', views.Runscript),
    url(r'^Codes_info.html/', views.Codesinfo),
    url(r'^Codes_SendFilesJson/', views.CodesSendFilesJson),
    url(r'^Codes_SendSqlJson/', views.CodesSendSqlJson),
    url(r'^Codes_del_SqlJson/', views.CodesDelSqlJson),
    url(r'^Codes_del_CodJson/', views.CodesDelCodJson),
    url(r'^Codes_Release.html/', views.CodesRelease),
    url(r'^Send_CodesJsonRelease/', views.CodesJsonRelease),
    url(r'^Send_Back_SqlJson/', views.CodesBackSqlJson),
    url(r'^Send_CodesJsonRestartNginx/', views.CodesJsonRestartNginx),
    url(r'^user_manage.html/', views.usermanage),
    url(r'^Send_UserManageJson/', views.UserManageJson),
    url(r'^del_user/', views.DelUserJson),
    url(r'^UserManage_edit_Json/', views.EditUserJson),
]

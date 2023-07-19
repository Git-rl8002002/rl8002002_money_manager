#!/usr/bin/python3

# Author   : JasonHung
# Date     : 20230220
# Update   : 20230220
# Function : money manager

###########
# tinfar
###########
tinfar_VM = {'host':'61.220.205.143','port':5306,'user':'backup','pwd':'SLbackup#123','db':'money_manager', 'charset':'utf8'}
tinfar_NB = {'host':'61.220.205.143','port':3306,'user':'backup','pwd':'SLbackup#123','db':'database_system', 'charset':'utf8'}

################
# tinfar sftp
################
tinfar_sftp = {'host':'61.220.205.143','port':5906,'user':'jason-tinfar','pwd':'1qaz#123','path':'/var/www/html'}

########
# txt
########
txt = {'mac_path':'/Users/user/eclipse-workspace/tinfar/money_manager/txt/' ,
       'win_path':'d:/money_manager/txt/'
      }
#!/usr/bin/bash

# ========================================================================================
# version: v.1.0
# author: mingliang.gao
# time: 2020/12/15 23:56:28
# mail: mingliang.gao@163.com
# summary: bash script template
# crontab: 30 02 * * * bash /home/mingliang.gao/crontab/bash_template.sh > /dev/null 2>&1
#
#           Enjoy the good time everyday！！!
#
# usage template:
#   # command parameters
#   find=$(which find)
#   if [ $? -eq 0 ];
#     then
#       echo -e "Find command: ${FGREEN}$find${NOC}"
#     else
#       echo -e "${FRED}Not found find, exit.${NOC}"
#       exit 1
#   fi
# ========================================================================================
# color print parameters
FBLACK='\033[30m'	# 黑
FRED='\033[31m' 	# 红
FGREEN='\033[32m' 	# 绿
FYELLOW='\033[33m'	# 黄
FBLUE='\033[34m'  	# 蓝
FPURPLE='\033[35m' 	# 紫
FSKYBLUE='\033[36m'	# 天蓝
FWHITE='\033[37m' 	# 白
# background font
FBBLACK='\033[40m'	 # 黑
FBRED='\033[41m' 	 # 红
FBGREEN='\033[42m' 	 # 绿
FBYELLOW='\033[43m'	 # 黄
FBBLUE='\033[44m'  	 # 蓝
FBFPURPLE='\033[45m' # 紫
FBSKYBLUE='\033[46m' # 天蓝
FBWHITE='\033[47m' 	 # 白
# no color
NOC='\033[0m'  	# 清除颜色
# others
UNDERLINE='\033[4m'


echo "***************************************************************"
echo -e "------------------${FBSKYBLUE} Server Host: 121.4.56.169 ${NOC}------------------"
echo "------------------------=====start=====------------------------"

# base paramters


# command paramters


# other paramters
cur_time="$(date +"%Y-%m-%d %H:%M:%S")"
start_seconds=$(date +%s)




end_seconds=$(date +%s)
echo -e "${FBRED}${cur_time}本次运行时间："$((end_seconds-start_seconds))"s ${NOC}"
echo "------------------------======end======------------------------"
echo -e "--------------------${FBSKYBLUE} Author: mingliang.gao ${NOC}--------------------"
echo "***************************************************************"
exit 0

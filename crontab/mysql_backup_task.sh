#!/usr/bin/bash

# ========================================================================================
# version: v.1.0
# author: mingliang.gao
# time: 2020/12/15 23:56:28
# mail: mingliang.gao@163.com
# summary: This script daily use to backup database
# crontab: 30 02 * * * bash /home/mingliang.gao/crontab/mysql_backup_task.sh > /dev/null 2>&1
#
#           Enjoy the good time everyday！！!
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


# db parameters
db_user="mingliang.gao"
db_passwd="910809ecb44c92db12ad5fa369375d00"
db_host="127.0.0.1"
db_port=3306
db_backup_dir="/home/mingliang.gao/db_backup/"
db_names=""
db_names=(twtoolbox_isapi)   # config dbs

# base command
rm=$(which rm)
find=$(which find)
mkdir=$(which mkdir)
touch=$(which touch)

# dir parameters
cur_time="$(date +"%Y-%m-%d %H:%M:%S")"
cur_date="$(date +"%Y%m%d")"
backup_history_file="${db_backup_dir}backup_history.log"
today_backup_dir="${db_backup_dir}${cur_date}"
if [ ! -d "$today_backup_dir" ];then
    $mkdir -p "$today_backup_dir"
fi
if [ ! -e "$backup_history_file" ];then
    $touch "$backup_history_file"
fi

# other parameters
backup_keep_days=1
start_time="$(date +"%Y-%m-%d %H:%M:%S")"

# mysql command
mysql=$(which mysql)
if [ $? -eq 0 ]; then
    echo -e "Mysql command: ${FGREEN}${mysql}${NOC}"
else
    echo -e "${FRED}Not found mysql, exit.${NOC}"
    exit 1
fi
mysqldump=$(which mysqldump)
if [ $? -eq 0 ]; then
    echo -e "Mysqldump command: ${FGREEN}${mysqldump}${NOC}"
else
    echo -e "${FRED}Not found mysqldump, exit.${NOC}"
    exit 1
fi

if [ -z "$db_names" ]
  then
    db_names=$(mysql -h$db_host -P$db_port -u$db_user -p$db_passwd -e 'show databases'| grep -vE 'Database|information_schema|mysql|performance_schema')
fi

for db in ${db_names[*]}; do
  echo -e "=============: ${FBGREEN} ${db} ${NOC}"
  $mysqldump -h$db_host -P$db_port -u$db_user -p$db_passwd $db > "${today_backup_dir}/${db}.sql"
done

# delete db backup dir
$find $db_backup_dir -type d -mtime +$backup_keep_days -exec $rm -rf {} \;

# record history
end_time="$(date +"%Y-%m-%d %H:%M:%S")"
start_seconds=$(date --date="$start_time" +%s)
end_seconds=$(date --date="$end_time" +%s)
echo "${cur_time}: $((end_seconds-start_seconds))" >> $backup_history_file

echo -e "${FBRED}${cur_time}本次运行时间："$((end_seconds-start_seconds))"s ${NOC}"
echo "------------------------======end======------------------------"
echo -e "--------------------${FBSKYBLUE} Author: mingliang.gao ${NOC}--------------------"
echo "***************************************************************"
exit 0

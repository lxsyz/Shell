#!/bin/bash
#echo 'start... '
#sleep 20
#echo "doing"
#sleep 12
#echo 'done'

FILE='conf.sh'
VAR=DAY
VALUE='2018-05-13'


for ((i=0;i<=2;i++))
do
    # 每次将conf.sh中的变量增加3个月
	NEW_DAY=$(date -d "$VALUE +3 months" +"%Y-%m-%d")
	VALUE=$NEW_DAY
    # c指令 修改值，引用变量需要双引号
	sed -i "/${VAR}/c\\${VAR}='${VALUE}'" $FILE
	sleep 9
done



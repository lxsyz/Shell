#!/bin/bash
total_port_num=`netstat -alp | wc -l`
echo $total_port_num
# generate random number
res=$(( RANDOM%total_port_num ))
echo $res

# 获取进程的id号/path
pid_info=`netstat -alp | sed -n "$res p"`
pid_info=`echo $pid_info | awk '{print $NF}'`
echo $pid_info
# 提取出pid号
substr=${pid_info%%/*}

for pid in `ps -e | grep $substr | awk '{print $1}'`;
do
	echo -n "${pid}"
	ls -l /proc/${pid}/exe | awk '{print $11}'
done

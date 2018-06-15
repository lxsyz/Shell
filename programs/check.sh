#!/bin/bash
# 判断参数是否存在
function check_param() {
	option=$1
	case $option in
		-p) FILE=$2
			if [ -z $2 ]
			then
				echo "lack param"
				echo "`basename $0`: usage:  [-p port]"
				exit 1
			fi
			;;
		-d) FILE=$2
			echo "directory name is $FILE";;
		*)
			echo "`basename $0`: usage:  [-p port]"
			exit 1;;
	esac
}

# 判断端口号是否被占用
function check_port() {
	check_param $1 $2
	res=`netstat -anl | grep $2`
	echo $res
	if [ -n "$res" ]
	then
		echo "invalid"
		pid_info=`netstat -alnp | grep $2 | awk '{print $NF}'`
		pid_num=${pid_info%%/*}
		echo "the pid is: $pid_num"
	else
		echo "valid"
	fi
}

check_port $1 $2

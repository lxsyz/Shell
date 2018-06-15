#/bin/bash
function check_ip2() {
	echo $1
	# 分成两部分， 前面的部分都要带上.， 后面的最后一部分不用带.
	if [[ $1 =~ ^((25[0-5]|2[0-4][0-9]|((1[0-9]{2})|([1-9]?[0-9])))\.){3}(25[0-5]|2[0-4][0-9]|((1[0-9]{2})|([1-9]?[0-9]))) ]] 
	then
		echo "success"
	else
		echo "fail"
	fi
}

function check_ip3(){
	echo $1
	# 分成两部分， 前面的部分都要带上.， 后面的最后一部分不用带.
	if [[ $1 =~ ^\d$ ]] 
	then
		echo "success"
	else
		echo "fail"
	fi
}
check_ip3 $1  

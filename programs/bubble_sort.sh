#!/bin/bash
# read -a arr
# arr=(5 2 3 4 9 8 7 6 3 2 7 8)
function bubbleSort(){
	echo "do function"
	flag=1
	arr=$1
	length=${#arr[@]}
	i=$length-1
	while (($i > 0));
	do 
		pos=0
		for(( j=0; j < $i; j++))
		do
			if [ ${arr[$j]} -gt ${arr[$j+1]} ]
        		then
            		temp=${arr[$j]}
            		arr[$j]=${arr[$j+1]}
            		arr[$j+1]=$temp
            		pos=$j
        	fi
		done
		i=$pos
	done
	for (( i=0; i < $length; i++ ))
	do
    	echo -e "${arr[$i]} "
	done
}
arr=(5 4 2 3 8 7 9 7 8 2)
bubbleSort ${arr[*]}

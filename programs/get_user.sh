#!/bin/bash
# who | cut -d ' ' -f1 | sort | uniq

sum() {
#	echo "this is "
	echo $(( $1+$2 )) $(( $1 * $2 ))
}
re=`sum 2 5`
sum=`echo "$re" | awk '{print $1}'`

echo $sum

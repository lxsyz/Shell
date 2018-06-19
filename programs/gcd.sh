#!/bin/bash
ARGS=2

if [ $# -ne "$ARGS" ]
then
	echo "Usage: `basename $0` first-number second-number"
fi

check()
{
	re='^[0-9]+$'
	if ! [[ $1 =~ $re ]]; then
		echo "error: not a number" >&2;exit 1
	fi
}

gcd()
{
	dividend=$1
	divisor=$2
	
	check $1
	check $2

	remainder=1
	until [ "$remainder" -eq 0 ]
	do
		let "remainder=$dividend % $divisor"
		dividend=$divisor
		divisor=$remainder
	done
}

gcd $1 $2
echo; echo "GCD of $1 and $2 = $dividend"; echo

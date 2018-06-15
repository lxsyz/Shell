#/bin/bash
# 对第二列进行排序和去重
# 然后再统计
if [ $# -ne 1 ]
then
	echo "usage: `basename $0` filename"
	exit 0
fi
cat $1 |sort -k 2 |uniq |awk '{a[$2]+=1;}END{for (i in a){print i,a[i]}}' 

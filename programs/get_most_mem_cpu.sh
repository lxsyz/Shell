#!/bin/bash
most_memory_pid=`ps -aux | sort -k4nr | head -1 | awk '{print $2}'`
echo "most memory pid is : ${most_memory_pid}"

most_cpu_pid=`ps -aux | sort -k3nr | head -1 | awk '{print $2}'`
echo "most cpu pid is : ${most_cpu_pid}"

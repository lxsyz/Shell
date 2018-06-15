#!/bin/bash
nowpt=$(date  +%Y%M%d'000000')

hive --hivevar nowpt=${nowpt} -f test.sql > /output.txt

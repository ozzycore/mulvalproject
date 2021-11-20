#!/bin/sh

export MALLOC_CHECK_=0
CLASSPATH=$CLASSPATH:$MULVALROOT/lib/dom4j-1.6.1.jar:$MULVALROOT/lib/jaxen-1.1.1.jar:$MULVALROOT/bin/adapter
ADAPTERSRCPATH=$MULVALROOT/src/adapter

#TODO: Test database connection

java -cp $CLASSPATH NessusXMLParser $1

if grep -qF "CVE" vulInfo.txt; then
    echo 'vulnerability(ies) detected'
else
 echo 'no vulnerability detected'
 exit 1
fi


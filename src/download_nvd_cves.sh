#!/bin/sh

#TODO:
# 1. Use meta NVD data before download.
# 2. Configure cron job for syncing nvd data feeds.

NVDPATH=nvd_json_files

# Check if 'NVDPATH' exists
if [ ! -d $NVDPATH ]; then
    mkdir $NVDPATH
fi

rm -rf $NVDPATH/*

current_year=`date +"%Y"`
year_i=2002

while [ $year_i -le $current_year ]; do
      wget https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-$year_i.json.zip --directory-prefix=$NVDPATH
      unzip $NVDPATH/nvdcve-1.1-$year_i.json.zip -d $NVDPATH
      year_i=`expr $year_i + 1`
done

rm -rf $NVDPATH/*.zip

echo "Downloaded all NVD data feed, check $NVDPATH directory"

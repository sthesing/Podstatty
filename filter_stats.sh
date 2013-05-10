#!/bin/sh
for f in $*;
do
  BaseName=${f##*/}
  BaseName=${BaseName%.*}
  gunzip ${BaseName}.gz
  grep 'GET /upload/' ${BaseName} | cut -d ' ' -f 7,10 | sort > ${BaseName}_filtered.txt
  rm ${BaseName}
done

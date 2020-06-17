#!/bin/bash
fileid="15p9ApVJFQu0KC4IxusVxza5A3KhLtTrA"
filename="expran.zip"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}

unzip ${filename}

rm ${filename}
rm cookie
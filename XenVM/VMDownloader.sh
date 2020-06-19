#!/bin/bash
fileid="1S7OwQZEvCwPEQxL7dm7Zz14YN1bOo2mX"
filename="expran.zip"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}

unzip ${filename}

rm ${filename}
rm cookie
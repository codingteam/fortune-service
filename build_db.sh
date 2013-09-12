#!/bin/sh

DATABASE_NAME="fortunes.db"

if [ ! -z $2 ]; then
    DATABASE_NAME=$2
fi

for i in fortunes/*; do
    echo $i
    ./fortune_to_sqlite3.py $i $DATABASE_NAME
done

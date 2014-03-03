#!/bin/sh

cp ./config/production.cfg /etc/fortune_service.cfg

cp ./fortune_service.py /var/www/fortune_service/fortune_service.py
cp ./fortune_service.fcgi /var/www/fortune_service/fortune_service.fcgi
cp ./fortune_schema.py /var/www/fortune_service/fortune_schema.py

if [ ! -f fortunes.db ]; then
    ./build_db.sh
fi

cp ./fortunes.db /var/www/fortune_service/fortunes.db

chown -R nginx:nginx /var/www/fortune_service/

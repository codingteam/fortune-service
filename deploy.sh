#!/bin/sh

cp ./config/production.cfg /etc/fortune_service.cfg

rm -rv /var/www/fortune_service/
mkdir /var/www/fortune_service/

cp -v ./fortune_service.py /var/www/fortune_service/fortune_service.py
cp -v ./fortune_service.fcgi /var/www/fortune_service/fortune_service.fcgi
cp -rv ./fortune/ /var/www/fortune_service/

if [ ! -f fortunes.db ]; then
    ./build_db.sh
fi

cp -v ./fortunes.db /var/www/fortune_service/fortunes.db

chown -Rv nginx:nginx /var/www/fortune_service/

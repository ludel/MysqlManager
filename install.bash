#!/bin/bash
# script for ubuntu 16.04 lts server
# authors : Dorian Wilhelm & Ludovic Delsol

# update repos && upgrade soft
apt update && apt upgrade -y;
apt autoremove -y;


# install all services for web server
apt install wget unzip git nginx php-fpm php-mysql mysql-server -y;


# enable&start all services
systemctl enable mysql && systemctl start mysql;
systemctl enable nginx && systemctl start nginx ;
systemctl enable php7.0-fpm && systemctl start php7.0-fpm ;


# PhpMyAdmin
cd /var/www/html && rm -rf * --no-preserve-root;
wget https://files.phpmyadmin.net/phpMyAdmin/4.7.9/phpMyAdmin-4.7.9-all-languages.zip;
unzip phpMyAdmin-4.7.9-all-languages.zip;
mv phpMyAdmin-4.7.9-all-languages/* /var/www/html;


# give permissions
chown -R www-data:www-data /var/www;
chmod -R 755 /var/www;


# clone project and move files config
cd ~ && git clone https://github.com/ludel/postgresql.git;
mv ~/postgresql/install/main-config /etc/nginx/sites-available;
rm -rf /etc/nginx/sites-enabled/default;
rm -rf /etc/nginx/sites-available/default;
ln -s /etc/nginx/sites-available/main-config /etc/nginx/sites-enabled/;
rm -rf /etc/nginx/nginx.conf && mv ~/postgresql/install/nginx.conf /etc/nginx/;
rm -rf /etc/php/7.0/fpm/php.ini && mv ~/postgresql/install/php.ini /etc/php/7.0/fpm/;

systemctl restart mysql;
systemctl restart nginx;
systemctl restart php7.0-fpm;
clear;
echo "Script Effectue, vous pouvez acceder a Php My Admin via l'adresse ip du serveur, Port 80 ;)"

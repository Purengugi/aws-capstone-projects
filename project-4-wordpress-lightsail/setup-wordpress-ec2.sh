#!/bin/bash
set -e

dnf update -y
dnf install -y httpd mariadb105-server php php-cli php-mysqlnd php-pdo php-gd php-mbstring php-xml php-fpm wget tar

systemctl start httpd
systemctl enable httpd
systemctl start mariadb
systemctl enable mariadb

DB_NAME="wordpress_db"
DB_USER="wp_user"
DB_PASS="CloudSecure2026!#"

mariadb -u root <<EOF
CREATE DATABASE ${DB_NAME} DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
CREATE USER '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

cd /tmp
wget https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
cp -r wordpress/* /var/www/html/

chown -R apache:apache /var/www/html
chmod -R 755 /var/www/html

cp /var/www/html/wp-config-sample.php /var/www/html/wp-config.php
sed -i "s/database_name_here/${DB_NAME}/g" /var/www/html/wp-config.php
sed -i "s/username_here/${DB_USER}/g" /var/www/html/wp-config.php
sed -i "s/password_here/${DB_PASS}/g" /var/www/html/wp-config.php

systemctl restart httpd

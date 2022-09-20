# NGINX

## Installation / désinstallation

```sh
# Installation
sudo apt install nginx

# Déinstallation
sudo apt remove nginx

# Déinstallation avec suppression des fichiers de configuration
sudo apt purge nginx
```

## Commandes de configuration

* Activer un site

Les sites disponibles se trouvent dans le répertoire `/etc/nginx/sites-available/`.

```sh
ln -s /etc/nginx/sites-available/<site> /etc/nginx/sites-enabled/

# Exemple
ln -s /etc/nginx/sites-available/exemple.org.conf /etc/nginx/sites-enabled/
```

* Vérifier la validité de la configuration

```sh
nginx -t
```

* Démarrer Nginx

```sh
systemctl start nginx
```

* Stopper Nginx

```sh
systemctl stop nginx
```

* Redémarrer Nginx

```sh
systemctl restart nginx
```

* Recharger Nginx

```sh
systemctl reload nginx
```

## Fichiers de configuration

* Exemple de VirtualHost basique avec HTTPS et PHP-FPM

```
server {
        listen 80;
        listen [::]:80;

        server_name www.exemple.org exemple.org web.exemple.org;

        root /var/www/exemple.org;

        index index.php index.html index.htm index.nginx-debian.html;

        location / {
                try_files $uri $uri/ =404;
        }

        location ~ \.php$ {
               include snippets/fastcgi-php.conf;
               fastcgi_pass unix:/run/php/php7.0-fpm.sock;
        }
}

server {
        listen 443 ssl;
        listen [::]:443 ssl;

        server_name www.exemple.org exemple.org web.exemple.org;

        ssl_certificate      /etc/ssl/certs/exemple.org_cert.pem;
        ssl_certificate_key  /etc/ssl/private/exemple.org_privkey.pem;

        root /var/www/exemple.org;

        index index.php index.html index.htm index.nginx-debian.html;

        location / {
                try_files $uri $uri/ =404;
        }

        location ~ \.php$ {
               include snippets/fastcgi-php.conf;
               fastcgi_pass unix:/run/php/php7.0-fpm.sock;
        }
}
```

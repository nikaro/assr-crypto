# Apache

## Installation / désinstallation

```sh
# Installation
sudo apt install apache2

# Déinstallation
sudo apt remove apache2

# Déinstallation avec suppression des fichiers de configuration
sudo apt purge apache2
```

## Commandes de configuration

* Activer un module

Les modules disponibles se trouvent dans le répertoire `/etc/apache2/mods-available/`.

```sh
a2enmod <module>

# Exemple
a2enmod ssl
```

* Activer une configuraton

Les configurations disponibles se trouvent dans le répertoire `/etc/apache2/conf-available/`.

```sh
a2enconf <config>

# Exemple
a2enconf php7.0-fpm
```

* Activer un site

Les sites disponibles se trouvent dans le répertoire `/etc/apache2/sites-available/`.

```sh
a2ensite <site>

# Exemple
a2ensite default-ssl.conf
```

* Vérifier la validité de la configuration

```sh
apachectl configtest
```

* Démarrer Apache

```sh
systemctl start apache2
```

* Stopper Apache

```sh
systemctl stop apache2
```

* Redémarrer Apache

```sh
systemctl restart apache2
```

* Recharger Apache

```sh
systemctl reload apache2
```

## Fichiers de configuration

* Exemple de VirtualHost basique avec HTTPS activé

```xml
<VirtualHost *:80>
    ServerName  www.exemple.org
    ServerAlias exemple.fr web.exemple.org
    ServerAdmin admin@exemple.fr

    DocumentRoot /var/www/exemple.org

    <Directory /var/www/exemple.org>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>

<VirtualHost *:443>
    ServerName  www.exemple.org
    ServerAlias exemple.fr web.exemple.org
    ServerAdmin admin@exemple.fr

    DocumentRoot /var/www/exemple.org

    <Directory /var/www/exemple.org>
        AllowOverride All
        Require all granted
    </Directory>

    SSLEngine on
    SSLCertificateKeyFile /etc/ssl/private/exemple.org_priv_key.pem
    SSLCertificateFile    /etc/ssl/certs/exemple.org_cert.pem
</VirtualHost>
```

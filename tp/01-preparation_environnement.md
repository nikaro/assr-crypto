# Préparation de l'environnement de travail

Pour réaliser de TP dans des conditions optimales, vous aurez besoin des outils suivants :
* Git
* Docker
* Docker-Compose

Si vous n'êtes pas à l'aise avec ces outils, vous pouvez utiliser des machines virtuelles avec l'outil de votre choix (par exemple VirtualBox).
Il faudra au moins deux VM, une pour l'autorité de certification, une pour le serveur Nginx.
Vous pouvez créer une troisième VM pour servir de client Web (curl, firefox, etc.), si vous souhaitez pas utiliser votre ordinateur comme client.

## Utilisation

```
# copier les fichiers du TP
git clone https://gitlab.com/assr/crypto-tp <chemin-vers-un-dossier>
cd <chemin-vers-un-dossier>

# lancer les conteneurs en arrière plan
docker-compose up -d

# ouvrir un shell dans l'autorité de certification
docker-compose exec ca bash

# ouvrir un shell dans l'autorité de certification
docker-compose exec nginx bash

# dans le shell du serveur web, recharger la configuration de nginx
nginx -s reload

# ouvrir un shell dans l'autorité de certification
docker-compose exec client bash

# dans le shell du client, faire une requête vers le serveur Nginx avec curl en lui indiquant le certificat de la CA
curl --cacert /usr/local/share/ca-certificates/cacert.crt https://assr.google.com

# dans le shell du client, tester la configuration TLS
testssl.sh --add-ca /usr/local/share/ca-certificates/cacert.crt https://assr.google.com

# arrêter les conteneurs
docker-compose down
```

## En cas de problème

Vous êtes (ou allez devenir) des informaticiens (technicien, adminsys, développeur, etc.), votre métier va donc certainement consister à résoudre des problèmes. C'est l'occasion de commencer, débrouillez-vous en cherchant sur internet, en demandant de l'aide à vos collègues/camarades. Si vous bloquez réellement, postez un message sur le forum.

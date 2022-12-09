# Consignes du TP

Pour mettre en œuvre ce TP vous pouvez vous aider des mémos OpenSSL et NGINX fournis, vous êtes également encouragés à chercher de la documentation sur internet.

En résumé, dans un premier temps, vous mettrez en place votre propre Autorité de certification (CA) afin de pouvoir signer des certificats qui seront reconnus dans le(s) navigateur(s) dans le(s)quel(s) elle est installée. Ensuite, sur votre serveur Web vous génèrerez une demande de certificat, que vous signerez grâce à votre CA. Pour terminer, vous installerez et configurerez le serveur Web pour servir un site Web grâce à TLS (en HTTPS) et vos certificats signés.

Je vais vous détailler précisément les étapes à suivre, mais ce sera à vous de trouver les bonnes commandes à exécuter.

## Informations

Si vous utilisez Docker avec la configuration fournie, les programmes nécessaires sont déjà installés. Et les fichiers sont au bon endroit, il ne reste plus qu'à les modifier/remplacer.

## Autorité de certification

Sur votre CA :

1. Générez un clé privée (`/etc/ssl/ca/ca.privkey.pem`). Ce sera la clé privée de la CA.
2. Générez le certificat associé à cette clé privée (`/etc/ssl/ca/ca.cert.pem`). La CA étant un tiers de confiance, son certificat sera auto-signé.

Sur votre client (si vous utilisez votre ordinateur ou une VM) :

3. Installez le certificat de la CA dans votre navigateur. Ainsi, tous les certificats qui seront signés par votre CA seront reconnus comme valides par votre navigateur.

## Demande de signature de certificat

Sur votre serveur Web :

1. Générez une clé privée (`/etc/ssl/assr/web.privkey.pem`). Ce sera la clé privée de votre site Web.
2. Générez une CSR (`/etc/ssl/assr/web.csr.pem`) avec votre clé, pour le nom de domaine `assr.google.com`. C'est ce qui va permettre à la CA de signer votre certificat.

Sur votre CA :

3. Signer la CSR (`/etc/ssl/ca/web.csr.pem`) grâce à la clé privée de la CA. En sortie vos obtiendrez un certificat signé (`/etc/ssl/ca/web.cert.pem`).

## Mise en place de HTTPS

Sur votre client (si vous utilisez votre ordinateur ou une VM) :

1. Dans votre fichier `hosts` faites pointer `assr.google.com` vers l'adresse IP de votre serveur Web.

Sur votre serveur Web :

2. Installez et configurez NGINX pour servir une page HTML via HTTPS grâce à votre clé privée et votre certificat signé.

Sur votre client :

3. Vérifiez que vous accédez en HTTPS au site de votre serveur Web à l'adresse <https://assr.google.com>. Si vous avez correctement généré vos certificats et configuré votre serveur Web, le navigateur ne doit afficher aucun avertissement.
4. Améliorez la configuration TLS de votre server jusqu'à ce que l'utilitaire [testssl.sh](https://testssl.sh/) ne renvoie aucun avertissement avec la commande : `testssl.sh https://assr.google.com` (utilisez le paramètre `--add-ca` pour renseigner le fichier de votre autorité de certification à utiliser)

## Consignes de rendu

Créez un répertoire sur le modèle `NOM_Prenom` (sans espaces et/ou caractères accentués). Dans ce dossier copiez les éléments suivants :

* `config/nginx.conf` : doit contenir l'intégralité de votre configuration Nginx
* `certs/*.pem` : tous les certificats utilisé durant le TP

Compressez au format ZIP le répertoire, avec le même nom de fichier que pour le répertoire.

```
NOM_Prenom.zip
└── NOM_Prenom
    ├── docker-compose.yml
    ├── certs
    │   ├── ca.cert.pem
    │   ├── ca.privkey.pem
    │   ├── web.cert.pem
    │   ├── web.csr.pem
    │   ├── web.csr.conf
    │   └── web.privkey.pem
    └── config
        └── nginx.conf
```

**Respectez scrupuleusement ces consignes, la correction est semi-automatique, si le script de correction échoue parce que vous n'avez pas nommé un fichier correctement vous n'aurez pas les points.**

ce travail peut être fait individuellement ou par groupe de 2 ou 3 personnes. Pensez à ajouter les noms de chacun des membres du groupe dans le nom du fichier de rendu.

Vous serez noté sur la validité de vos clés et certificats et sur la qualité de votre configuration NGINX.

# OpenSSL

## Générer une clé privée

```
openssl genrsa -out <clé_priv> <taille>

# Exemple
openssl genrsa -out priv_key.pem 2048
```

Détail des arguments de la commande :

* `genrsa` : utilitaire OpenSSL permettant de générer des clés RSA
* `-out <clé_priv>` : indique le fichier de sortie dans lequel va être enregistrée la clé privée
* `<taille>` : défini la taille de la clé privée

## Générer un certificat auto-signé

```bash
openssl req -new -x509 -days <durée> -key <clé_priv> -out <cert>

# Exemple
openssl req -new -x509 -days 365 -key ca_priv_key.pem -out ca_cert.pem

Country Name (2 letter code) [AU]:FR
State or Province Name (full name) [Some-State]:Ile-de-France
Locality Name (eg, city) []:Lieusaint
Organization Name (eg, company) [Internet Widgits Pty Ltd]:ASSR
Organizational Unit Name (eg, section) []:SECU
Common Name (e.g. server FQDN or YOUR name) []:ASSR_CA
Email Address []:
```

Détail des arguments de la commande :

* `req` : utilitaire OpenSSL permettant de générer des demandes de signature et des certificats
* `-new` : indique qu'on veut générer une demande de signature de certificat
* `-x509` : indique qu'on veut autosigner notre demande de certificat
* `-days <durée>` : indique la durée de validité de notre certificat
* `-key <clé_priv>` : indique la clé privée qu'on utilise
* `-out <clé_priv>` : indique le fichier de sortie dans lequel va être enregistrée le certificat

## Générer une demande de signature de certificat (CSR)

```bash
openssl req -new -key <clé_priv> -out <csr>

# Exemple
openssl req -new -key monsite_priv_key.pem -out monsite_csr.pem

Country Name (2 letter code) [AU]:FR
State or Province Name (full name) [Some-State]:Ile-de-France
Locality Name (eg, city) []:Lieusaint
Organization Name (eg, company) [Internet Widgits Pty Ltd]:ASSR
Organizational Unit Name (eg, section) []:SECU
Common Name (e.g. server FQDN or YOUR name) []:web.assr.iutsf.org
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
```

Détail des arguments de la commande :

* `req` : utilitaire OpenSSL permettant de générer des demandes de signature et des certificats
* `-new` : indique qu'on veut générer une demande de signature de certificat
* `-key <clé_priv>` : indique la clé privée qu'on utilise
* `-out <clé_priv>` : indique le fichier de sortie dans lequel va être enregistrée la demande de signature de certificat

Pour information, le champ `commonName` (CN) est déprécié par les navigateurs Web, pour qu'un certificat soit considéré comme valide par ceux-ci il doit posseder l'extension `subjectAltName` (SAN).

## Signer une demande de certificat

```bash
openssl x509 -req -days <durée> -in <csr> -out <cert> -CA <cert_ca> -CAkey <clé_priv_ca> -CAcreateserial

# Exemple
openssl x509 -req -days 90 -in monsite_csr.pem -out monsite_cert.pem -CA ca_cert.pem -CAkey ca_priv_key.pem -CAcreateserial
```

Détail des arguments de la commande :

* `x509` : utilitaire OpenSSL permettant d'afficher ou de signer des certificats
* `-req` : indique qu'on veut utiliser une demande de signature de certificat
* `-days <durée>` : indique la durée de validité du certificat
* `-in <csr>` : indique la demande signature de certificat qu'on utilise
* `-out <clé_priv>` : indique le fichier de sortie dans lequel va être enregistrée le certificat signé
* `-CA <cert_ca>` : indique le certificat de la CA qu'on utilise
* `-CAkey <clé_priv_ca>` : indique la clé privée de la CA qu'on utilise
* `-CAcreateserial` : créer le fichier de numéro de série de la CA, il n'est obligatoire que la première fois qu'on signe un certificat

## Générer une demande de signature de certificat (CSR) avec subjectAltName (SAN)

Creation du fichier de configuration :

```bash
cat <<EOF > monsite_csr.conf
[ req ]
prompt = no
distinguished_name = dn
req_extensions = req_ext

[ dn ]
CN = exemple.com
emailAddress = admin@exemple.com
O = ASSR
OU = SECU
L = Lieusaint
ST = France
C = FR

[ san ]
subjectAltName = DNS: www.exemple.com
EOF

openssl req -new -config monsite_csr.conf -key monsite_priv_key.pem -out monsite_csr.pem
```

## Signer une demande de certificat avec SAN

```bash
openssl x509 -req -extfile certs/web/csr/conf -extensions san -days 90 -in monsite_csr.pem -out monsite_cert.pem -CA ca_cert.pem -CAkey ca_priv_key.pem -CAcreateserial
```

## Quelques commandes en vrac

Analyser le contenu d'un certificat : `openssl x509 -noout -text -in <cert>`

Voir le certificat d'un serveur : `openssl s_client -connect <serveur>:<port>`

Analyser le contenu d'un certificat envoyé par un serveur : `openssl s_client -connect <serveur>:<port> | openssl x509 -noout -text -in <cert>`

Vérifier qu'un certificat est bien signé par une CA : `openssl verify -CAfile <cert_ca> <cert>`

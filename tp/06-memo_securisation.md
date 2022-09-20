# Sécurisation

[Mozilla](https://www.mozilla.org/fr/) fournit un générateur de configuration TLS qui permet d'avoir facilement une sécurité convenable. Il faut savoir que plus vous durcissez la configuration TLS de vos sites, plus ceux-ci deviennent inaccessibles aux vieux clients. En fonction de votre contexte et votre modèle de menace, il va vous falloir trouver le bon compris entre sécurité renforcée et accessbilité.

<https://mozilla.github.io/server-side-tls/ssl-config-generator/>

Si vous voulez durcir vos configurations TLS au maximum, [BetterCrypto](https://bettercrypto.org/) fournit une documentation indiquant les paramètres à mettre en place pour différents services (Apache, NGINX, Postfix, Dovecot, etc.).

Si vous voulez tester la robustesse de votre configuration TLS, vous pouvez utiliser l'outil [testssl.sh](https://testssl.sh/) ou [l'observatoire de Mozilla](https://observatory.mozilla.org/).

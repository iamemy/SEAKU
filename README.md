# SEAKU

Base logicielle nécessaire pour interfacer le casque SEAKU

## INSTRUCTIONS DE SETUP DE LA RASPBERRY DANS LE CADRE DU PROJET SEAKU

1. Telecharger Raspberry Pi imager ici: https://www.raspberrypi.com/software/ (**Download for Windows/Mac OS/Ubuntu for x86**)
2. Installer **Raspberry Pi imager**.
3. Ouvrir **Raspberry Pi imager**, et selectionner:
    1. Le **Modèle de la Raspberry Pi**: **Raspberry Pi 3**
    2. Le **Sytème d'exploitation**: **Raspberry Pi OS (Legacy, 32-bit)** 
    3. Le **Stockage**: **La carte Micro SD ou clef USB à formatter**
4. Cliquer sur **Suivant**
5. A la question **Voulez-vous appliquer les réglages de personalisation de l'OS**, cliquer sur **Modifier réglages**, puis:
    1. Dans l'onglet **Général**:
	    1. **Nom d'hôte**: **Cocher** puis **raspberrypi**
	    2. **Définir nom d'utilisateur et mot de passe**: **Cocher** puis:
	        - **Nom d'utilisateur**: **emy**
	        - **Mot de passe**: **raspberry**
	    3. **Configurer le Wi-Fi**: **Cocher** puis:
	        - **SSID**: **Nom du point d'accès Wi-Fi**
	        - **Mot de passe**: **Mot de passe du point d'accès Wi-Fi** 
	        - **Pays Wi-Fi**: **FR**
	    4. **Définir les réglages locaux**: **Cocher** puis:
	        - **Fuseau horaire**: **Europe/Paris**
	        - **Type de clavier**: **fr**
	2. Ne pas toucher aux onglets **Services** et **Options**.
	3. Cliquer sur **Enregistrer**.
6. A la question **Voulez-vous appliquer les réglages de personalisation de l'OS**, cliquer sur **OUI**.
7. Cliquer à nouveau sur **Oui**.

Le **lecteur externe** (carte Micro SD ou clef USB) est en cours de **formattage**.
Attender jusqu'à la fin **sans débrancher le périphérique**, puis éjecter le pour l'insérer dans la Raspberry Pi.
Alimenter la Raspberry Pi, puis brancher un écran en HDMI à cette dernière ainsi qu'une souris et un clavier en USB.
Lorsque le bureau de Raspberry Pi OS s'affiche sur l'écran, suivez les instructons suivantes:

1. Cliquer sur le menu **Application** au logo **Raspberry** en haut à gauche de l'écran.
2. Cliquer sur **Preferences**.
3. Cliquer sur **Raspberry Py Configuration**, puis, dans l'onglet **Interface**:
    1. Activer l'interface **VNC**.
    2. Activer l'interface **I2C**.
    3. Activer l'interface **I2C**.
4. Cliquer sur **Ok** en bas à droite du menu **Raspberry Py Configuration**.
5. Cliquer sur l'application **Terminal** en haut à gauche de l'écran, à la droite du menu **Application** précédemment ouvert.
6. Entrer la commande suivante:
`sudo raspi-config`
7. Naviguer à l'aide de la flèche du bas jusqu'à **3. Interface Options**.
8. Appuyer sur **Entrée**.
9. Ré-appuyer sur **Entrée** sur le menu **I1. Legacy camera**.
10. Déplacer vous à l'aide de la flèche de gauche jusqu'à **Yes**.
11. Appuyer sur **Entrée**.
12. Ré-appuyer sur **Entrée**.
13. Appuyer sur **Echap**.
14. Une fois sorti du menu **raspi-config**, redémarrer la Raspberry Pi à l'aide de la commande suivante:
`sudo reboot`

Attendre que la Raspberry Pi se réallume et prenne en compte les modifications effectuées.
Lorsque la Raspberry Pi est allumée, brancher un câble ethernet entre votre ordinateur et la Raspberry Pi.
Finalement, rendez-vous sur votre PC pour installer de quoi utiliser votre Raspberry Pi à distance.
Vous aurez besoin du logiciel **RealVNC Viewer** pour contrôler votre Raspberry Pi depuis votre ordinateur.
Suivez les instructions suivantes:

1. Telecharger RealVNC ici: https://realvnc.com/fr/connect/download/viewer/raspberrypi/ (**Download RealVNC Viewer**)
2. Installer **RealVNC**.
3. Ouvrir **RealVNC**.
4. S'il vous est demandé de vous connecter, refuser tout: **Use without signing**.
5. Dans la barre de connexion **RVNC Connect**, renseigner l'IP locale de votre Rasperry Pi: **raspberrypi.local**
6. Cliquer sur **Oui**.
7. Renseigner maintenant les identifiants de votre compte utilisateur Raspberry Pi. Si vous avez suivi les instructions, remplir comme suit:
    - **Nom d'utilisateur**: **emy**
    - **Mot de passe**: **raspberry**
    - Cocher la case **Mémoriser le mot de passe**.
8. Cliquer sur **Ok**.

La Raspberry Pi est désormais entièrement contrôlable depuis votre ordinateur.
Vous pouvez débrancher l'écran HDMI de votre Raspberry pi, ainsi que votre souric et clavier USB.
Il va maintenant falloir installer les différentes dépendances du projet.
L'utilisation de la Raspberry Pi Camera ne nécessitel l'installation d'aucun paquets supplémentaires.
Suiver les instructions suivantes:

1. Ouvrir un terminal en cliquant surl l'onglet **Terminal** en haut à gauche.
2. Entrer la commande suivante pour cloner le répertoire **SEAKU**:
`git clone https://<TOKEN>@github.com/iamemy/SEAKU.git`
Le token n'est évidemment pas donné ici.
3. Deplacer-vous dans ce répertoire à l'aide de la commande suivante:
`cd SEAKU`
4. Mettez à jour votre package manager à l'aide des deux commandes suivantes:
`sudo apt-get update`
`sudo apt-get upgrade`
5. Il est maintenant possible de procéder à l'installation des différentes dépendances du projet:
    - Librairie d'utilisation de l'écran:
        1. Utiliser la commande suivante pour cloner le répository git d'Adafruit:
		`git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git`
        2. Déplacer vous dans le répository cloné à l'aide de la commande:
		`cd Adafruit_Python_SSD1306`
        3. Installer la bibliothèque à l'aide de la commande suivante:
		`sudo python3 setup.py install`
		4. Sortir du répertoire de la bibliothèque d'Adafruit à l'aide de la commande suivante:
		`cd -`
		5. Supprimer le répertoire cloné qui n'est désormais plus utile en entrant la commande:
		`sudo rm -rf Adafruit_Python_SSD1306`
	- Librairie d'utilisation du capteur barométrique BMP280:
        1. Utiliser la commande suivante pour installer la bibliothèque d'Adafruit:
		`sudo pip3 install adafruit-circuitpython-bmp280`
	- Librairie d'utilisation du ruban de led WS2812B :
        1. Utiliser les commandes suivantes pour installer la bibliothèque d'Adafruit:
		`sudo pip3 install rpi_ws281x`
		`sudo pip3 install adafruit-circuitpython-neopixel`
		`sudo python3 -m pip install --force-reinstall adafruit-blinka`
6. Tout est prêt pour l'execution du software, à l'aide de la commande suivante:
`./main.sh`
7. Bravo! Il est désormais possible d'interragir avec le casque SEAKU grâce au Dashboard sous vos yeux.

## Remerciements

Nous tenons à remercier **rravivarman** pour sa bibliothèque [RaspberryPi/MAX30102 library](https://github.com/rravivarman/RaspberryPi/tree/master/MAX30102).
Nous remercions également **Tim** de https://core-electronics.com pour son article, ses instructions et ses examples d'implémentatons des librairies **rpi_ws281x** et **adafruit-circuitpython-neopixel**.

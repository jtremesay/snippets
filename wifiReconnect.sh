#!/bin/bash

# wifiReconnect.sh
# (c) Copyright 2007-2008, killruana <killruana@gmail.com>
#
# Script de reconnection automatique
#  en cas de deconnection du wifi.
#
# Utilisation :
#  - configurez le script
#  - crontabez le
#
# Dépendances :
#  - fping
#
# Création : 10 novembre 2007
#
# Changelog :
#  6 février 2008 :
#   - corrections mineurs
#
# ToDo :
#  - Un switch/case pour reconfigurer le reseau en fonction de la distrib

#################
# Configuration #
#################
GATEWAY=192.168.1.1	# La chose à pinguer pour vérifier votre connexion au réseau WiFi (e.g. votre passerelle réseau)
INTERFACE=wlan0		# L'interface à vérifier
LOG_PATH=/var/log/wifiReconnect/	# Le dossier de log


#################
#   Fonctions   #
#################
# Fonction pour écrire les fichiers journaux
Log()
{
    echo `date +%b` `date +%d` `date +%H:%M:%S` `uname -n` $0 "Passerelle : $GATEWAY - $1" >> ${LOG_PATH}${INTERFACE}.log
}

# Fonction pour tester la connection
TestConnection()
{
   fping $GATEWAY > /dev/null
   ETAT=$?
}


#################
#     Main      #
#################
TestConnection
if [ $ETAT = 1 ]; then
    Log "déconnecté"

    #ifdown ${INTERFACE} &> /dev/null && ifup ${INTERFACE} # %*$! de RaLink rt61 qui marche pas comme les autres -_-'    

    /etc/rc.d/net-profiles restart 	# Pour Arch Linux
    #/etc/init.d/networking restart	# Pour Debian et Debian-like
fi
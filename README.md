# Cours : Postgresql
### By **Ludovic Delsol** & **Dorian Wilhelm**

|Techno.            |Version |
|----------------   |-------------------------------|
|OS - Ubuntu        |16.0.4 Lts                     |
|PhpMyAdmin         |4.7.9                          |
|Php - fpm          |7.0                            |
|Python             |3.6                            |

## Ce que fait mon script d'installation
Ce script permet de deployer rapidement:
- un serveur http **nginx**
- un serveur **php-fpm**
- un serveur de base de donnée **mariadb**
- le site **PhpMyAdmin**
- injecter 1000 entrées la base de donnée *(au nom de **app_data** table **data**)*

## Comment utiliser / run le script
![premier gif](./pictures/script-in-server.gif)

Comme l'exemple ci-dessus le montre , </br>
Pour lancer le script, il faut se connecter en ssh sur la machine cible, puis copier le [code ici](https://github.com/ludel/mysqlManager/blob/master/install.bash), dans un editeur de text en cli (***vim*** / ***nano***) comme dans l'exemple juste au dessus ***VIM*** . Et pour finir lancer le fichier bash</br> 


![seconde gif](./pictures/demo-script.gif)

![troisieme gif](./pictures/acces-site.gif)

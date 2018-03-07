import mysql.connector
from mysql.connector import errorcode
import os
import time


def main():
    database_name = "test"  # input("Database name (default:test) : ")
    user = "root"  # input("User (default:root) : ")
    password = "lolilol47"  # input("Password (default:lolilol47) : ")
    host = "localhost"  # input("host (default:localhost): ")
    choice = int(input("Choice your process : "))

    con = connection(user, password, database_name, host)
    cursor = con.cursor()

    if choice == 0:
        show_tables(cursor, input("Nom de la table : "))
    elif choice == 1:
        create_backup(user, password, database_name, input("Dossier de destination : "))
    elif choice == 2:
        restore_backup(user, password, database_name, input("Path sql file : "))
    elif choice == 3:
        delete_old_backup(input("Backups directory : "))

    print("Process end")


def connection(user, password, database_name, host):
    """Connexion à la base de donnée mysql"""
    con = None
    try:
        con = mysql.connector.connect(user=user, password=password, host=host, database=database_name)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            exit("Error: Bad user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            exit("Error: Database does not exist")
        else:
            exit(err)
    return con


def show_tables(cursor, table_name):
    """Affiche toute une table"""
    cursor.execute("SELECT * FROM {}".format(table_name))
    rows = cursor.fetchall()
    for row in rows:
        print('{0} - {1} '.format(row[0], row[1]))


def create_backup(user, password, database_name, path_file):
    """Créer un backup d'une base de donnée spécifique"""
    file = path_file + str(time.time()) + ".sql"
    directory = file + ".gz"
    try:
        os.popen("mysqldump -u {0} -p{1} {2}  | gzip > {4} ".format(user, password, database_name, file, directory))
    except PermissionError:
        print("PermissionError: bad permission in path {0}".format(path_file))
    except:
        print("Error: dump error")


def restore_backup(user, password, database_name,  file):
    """Restore une backup de la base de donnée"""
    try:
        os.popen("gunzip < {3} | mysql -u {0] -p{1} {2}".format(user, password, database_name, file))
    except PermissionError:
        print("PermissionError: bad permission {0} file".format(file))
    except:
        print("Error: restore failed. Check path sql file.")


def delete_old_backup(directory):
    """Supprimer un backup datant de plus 1 semaine"""
    for i in os.listdir(directory):
        lastweek = time.time() - 7
        if os.path.getmtime(directory+i) < lastweek:
            os.remove(directory+i)


main()

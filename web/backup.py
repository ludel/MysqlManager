import mysql.connector
from mysql.connector import errorcode
import os
import time


def main():
    database_name = checker_value(input("Database name (default:test) : "), "test")
    user = checker_value(input("User (default:root) : "), "root")
    password = checker_value(input("Password (default:lolilol47) : "), "lolilol47")
    host = checker_value(input("host (default:localhost): "), "localhost")
    text = "0 : "+str(show_tables.__doc__)+"\n" \
           "1 : "+str(create_backup.__doc__)+"\n" \
           "2 : "+str(restore_backup.__doc__)+"\n"\
           "3 : "+str(delete_old_backup.__doc__)+"\n"

    print(text)

    choice = int(checker_value(input("Choix (0) : "), 0))

    con = connection(user, password, database_name, host)
    cursor = con.cursor()

    if choice == 0:
        show_tables(cursor, input("Nom de la table : "))
    elif choice == 1:
        create_backup(user, password, database_name, input("Dossier de destination : "))
    elif choice == 2:
        restore_backup(user, password, database_name, input("Chemin du fichier sql : "))
    elif choice == 3:
        delete_old_backup(input("Dossier contenant les backups : "))

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
    except:
        exit("Unknown error: What the fuck")
    return con


def show_tables(cursor, table_name):
    """Affiche toute une table"""
    cursor.execute("SELECT * FROM {}".format(table_name))
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def create_backup(user, password, database_name, path_file):
    """Créer un backup d'une base de donnée spécifique"""
    file = path_file + str(time.time()) + ".sql"
    directory = file + ".gz"
    try:
        os.popen("mysqldump -u {0} -p{1} {2}  | gzip > {4} ".format(user, password, database_name, file, directory))
        print("Dump de la base de donnée réussit")
    except PermissionError:
        exit("PermissionError: bad permission in path {0}".format(path_file))
    except:
        exit("Error: dump error")


def restore_backup(user, password, database_name,  file):
    """Restore une backup de la base de donnée"""
    try:
        os.popen("gunzip < {3} | mysql -u {0] -p{1} {2}".format(user, password, database_name, file))
        print("Restoration de la base de donnée réussit")
    except PermissionError:
        exit("PermissionError: bad permission {0} file".format(file))
    except:
        exit("Error: restore failed. Check path sql file.")


def delete_old_backup(directory):
    """Supprimer un backup datant de plus 1 semaine. Attention le programme supprime automatiquement"""
    has_old_directory = False
    for i in os.listdir(directory):
        lastweek = time.time() - 7
        if os.path.getmtime(directory+i) < lastweek:
            os.remove(directory+i)
            print("{} remove".format(directory+i))
            has_old_directory = True
    if not has_old_directory:
        print("Rien à supprimer")


def checker_value(value, default):
    if value == '':
        value = default
    return value


main()

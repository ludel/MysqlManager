import mysql.connector
from mysql.connector import errorcode
import os
import time


def main():
    print("================================", end="\n")
    print("--- === Database manager === ---", end="\n")
    print("================================", end=2 * "\n")

    database_name = checker_value(input("Database name (test) : "), "test")
    user = checker_value(input("User (root) : "), "root")
    password = checker_value(input("Password (lolilol47) : "), "lolilol47")
    host = checker_value(input("host (localhost): "), "localhost")

    show_info()

    choice = int(checker_value(input("Choix (0) : "), 0))

    con = connection(user, password, database_name, host)
    cursor = con.cursor()

    if choice == 0:
        show_tables(cursor, input("Nom de la table : "))
    elif choice == 1:
        create_backup(user, password, input("Dossier de destination : "),
                      input("Base de donnée (laisser vide pour dump toute la bdd) : "), input("Tables :"))
    elif choice == 2:
        restore_backup(user, password, database_name, input("Chemin du fichier sql : "))
    elif choice == 3:
        delete_old_backup(input("Dossier contenant les backups : "))
    else:
        exit("InvalidCharacter")

    print("Process end")


def show_info():
    text = {
        0: show_tables,
        1: create_backup,
        2: restore_backup,
        3: delete_old_backup,
    }

    for key, value in text.items():
        print(key, value.__doc__, sep=" : ")


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
        print(row)


def create_backup(user, password, path_file, database="", table=""):
    """Créer un backup d'une base de donnée ou d'une table spécifique"""
    archive_path = path_file + str(time.time()) + ".sql.gz"
    if database:
        command = "mysqldump -u {} -p{} {} {} | gzip > {} ".format(user, password, database, table, archive_path)
    else:
        command = "mysqldump -u {} -p{} --all-databases | gzip > {} ".format(user, password, archive_path)
    try:
        os.popen(command)
        print("Dump de la base de donnée réussit")
    except PermissionError:
        exit("PermissionError: bad permission in path {}".format(path_file))
    except:
        exit("Error: dump error")


def restore_backup(user, password, database_name, file):
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
        last_week = time.time() - 7
        if os.path.getmtime(directory + i) < last_week:
            os.remove(directory + i)
            print("{} remove".format(directory + i))
            has_old_directory = True
    if not has_old_directory:
        print("Nothing to delete")


def checker_value(value, default):
    if not value:
        value = default
    return value


if __name__ == '__main__':
    main()

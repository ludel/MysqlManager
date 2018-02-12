import os


def savedatabase():

    path_save = input("Path to save ")
    try:
        os.popen("pg_dump appli_web  | gzip > {}".format(path_save))
    except PermissionError:
        exit("PermissionError: You have no right on " + path_save)
    except:
        exit("Error: Dump failled")

    print("Save file create")



def restoredatabase():
    path_save = input("Path of save file ")
    try:
        os.popen("createdb appli_web")
        os.popen("gunzip -c path_save | psql appli_web")
    except PermissionError:
        exit("PermissionError: You have no right on " + path_save)
    except:
        exit("Error: restore failled")


print("Finish")
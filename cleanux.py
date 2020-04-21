#!/usr/bin/env python3

from pathlib import Path
import os
import hashlib
import sqlite3


def remove(path,password, conn):
    c = conn.cursor()
    path = Path(path)

    list = path.glob("*")
    for x in list:

        if x.is_symlink():
            continue
        
        if x.is_dir():
            remove(x,password,conn)
        else:
            genHash = hashlib.sha384(x.read_bytes()).hexdigest()
        
            getHashes(c,genHash,x,password)


def dbConnect():
    if not os.path.exists("fileHashes.db"):
        conn = sqlite3.connect("fileHashes.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE hashTable (hash text primary key not null,
                                            path text not null)''')
    else:
        conn = sqlite3.connect("fileHashes.db")
    
    return conn
                                    


def getHashes( c, fHash,fPath,password):

    try:
        c.execute("SELECT * FROM hashTable WHERE hash = ?",(fHash,))
        fhash,fpath, = c.fetchone()
        fPath = str(fPath)

        if fpath != fPath:

            try:
                os.remove(fPath)
    
            except:
                os.system("echo %s sudo -S rm %s" %(password,x))


            os.symlink(fpath,fPath)


    except:
        c.execute("INSERT INTO hashTable VALUES(?,?)",(fHash,str(fPath),))
        conn.commit()

        


def banner():
    logo = '''
                        \033[1;34m$$$
                         $$$
                          $$$
                           $$$
                            $$$
                             $$$
                              $$$
                               $$$
                     \033[1;31m$$$$$$$$$$$$$$$$$$$$$$
                      $$$$$$$$$$$$$$$$$$$$$$
                       $$$$$$$$$$$$$$$$$$$$$$
                        \033[1;33m$$ $$$ $$$ $$ $$ $ $$ $
                         4 $$ $ $$ $$ $$ $$ $$ $$ 
                        $ $$ $$$ $ $$$$ $ $ $ $$ $

                   \033[1;31m
                    *********** CLEANUX ********** 
                     REDUDANT FILE REMOVER FOR LINUX
                         by DALI HILLARY ( HIX )
**************************************************************************
                     \033[0;37m
                '''
    print(logo)

if __name__ == "__main__":
    
    dir = "/home/hix/Documents/"
    conn = dbConnect()
    banner()

    dir = input("\033[1;32mENTER path to clean e.g Desktop or Downloads (default is entire Pc): \033[0;37m")

   
    while(True):
        path = Path(dir)
        homeDir = path.home()
        path = str(homeDir)
        if len(dir) < 1:
            break

        path = path +"/" +dir
        dirPath = Path(path)
        if not dirPath.exists():
            dir = input("\n\033[1;31mEnter correct path: \033[0;37m")
        
        else:
            break
    
    print("\nTo \033[1;31mremove adminstrator\033[0;37m files")
    password = input("\033[1;32mEnter Password: \033[0;37m")

    print(''' \033[1;34m      
             ....................................................... 
                   WE ARE TAKING CARE OF THINGS FOR YOU
                RELAX AND HAVE A CUP OF COFFEE AS WE WORK
             .......................................................\033[0;31m
                            PLEASE WAIT !!!!
            \033[1;34m........................................................\033[0;37m
             ''')


    
    remove(path,password,conn)

    print("\n\n\033[1;32m               OPERATION COMPLETE THANK FOR USING CLEANUX\n\n\n")


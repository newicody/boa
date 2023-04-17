#!/usr/bin/env python3
import sys
import select
import os
import json
import threading
import asyncio

from logg import logg
from poool import poool
from errors import errors


import multiprocessing

from myoptions import myoptions
from myoptions.config_parse import config_parse

from sidewinder.sidewinder import sidewinder

from network import network




if __name__ == '__main__':

    port_value = 8081
    path_value = "./"

    conf=path_value=install=uninstall=name=ssll=ssl_file=port_value=venv_path=interface=dhcp=ip=log=poopool=github=user=init=boot=peers=False


    timetowait = 0.05 # seconds:

    options = iter(sys.argv)
    arg = next(options)
    arg = next(options)

    while arg!="main.py":
        if (arg == "-v") or (arg == "--venv_path"):
             try:
                 venv_path = next(options)
             except StopIteration as e:
                 print("Missing parameter after -v/--venv_path")
        if (arg == "-p") or (arg == "--port"):
             try:
                 port_value = int(next(options))
             except StopIteration as e:
                 print("Missing parameter after -p/--port")
        if (arg == "-r") or (arg == "--root"):
             try:
                 path_value = next(options)
             except StopIteration as e:
                 print("Missing parameter after -r/--root")
        if (arg == "-u") or (arg == "--user"):
             try:
                 user = next(options)
             except StopIteration as e:
                 print("Missing parameter after -u/--user")
        if (arg == "-t") or (arg == "--timing"):
             try:
                 timetowait = next(options)
             except StopIteration as e:
                 print("Missing parameter after -t/--timing")
        if (arg == "-s") or (arg == "--ssl"):
             try:
                 ssll = next(options)
             except StopIteration as e:
                 print("Missing parameter after -s/--ssl")
        if (arg == "-c") or (arg == "--ssl_file"):
             try:
                 ssl_file = next(options)
             except StopIteration as e:
                 print("Missing parameter after -c/--ssl_file")
        if (arg == "-i") or (arg == "--iface"):
             try:
                 interface = next(options)
             except StopIteration as e:
                 print("Missing parameter after -i/--iface")
        if (arg == "-P") or (arg == "--pool"):
             try:
                 poopool = next(options)
             except StopIteration as e:
                 print("Missing parameter after -P/--pool")
        if (arg == "-o") or (arg == "--peers"):
             try:
                 peers = next(options)
             except StopIteration as e:
                 print("Missing parameter after -o/--peers")
        if (arg == "-a") or (arg == "--ip"):
             try:
                 ip = next(options)
             except StopIteration as e:
                 print("Missing parameter after -a/--ip")
        if (arg == "-l") or (arg == "--log"):
             try:
                 log = next(options)
             except StopIteration as e:
                 print("Missing parameter after -l/--log")
        if (arg == "-G") or (arg == "--github"):
             try:
                 github = next(options)
             except StopIteration as e:
                 print("Missing parameter after -G/--github")
        if (arg == "-B") or (arg == "--boot"):
             try:
                 boot = next(options)
             except StopIteration as e:
                 print("Missing parameter after -B/--boot")
        if (arg == "-U") or (arg == "--THISHIT"):
             try:
                 uninstall = next(options)
             except StopIteration as e:
                 print("Missing parameter after -U/--THISHIT")
        if (arg == "-I") or (arg == "--install"):
             try:
                 install = next(options)
             except StopIteration as e:
                 print("Missing parameter after -I/--install")
        if (arg == "-n") or (arg == "--name"):
             try:
                 name = next(options)
             except StopIteration as e:
                 print("Missing parameter after -n/--name")
        if (arg == "-m") or (arg == "--macaddress"):
             try:
                 macaddress = next(options)
             except StopIteration as e:
                 print("Missing parameter after -m/--macaddress")
        if (arg == "-R") or (arg == "--runfromconf"):
             try:
                 conf = next(options)
             except StopIteration as e:
                 print("Missing parameter after -R/--runfromconf")
        if (arg == "-h") or (arg == "--help"):
             print("Merci de tester/utiliser mon serveur web.\n\n"
"Il n'est qu\'au début de son dévelopement. Il ne fonctionne"
"pour le moment qu\'en standalone et permet de :\n - lister le"
"contenu d\'un répertoire\n - afficher des pages html et php\n\n ")
             print("Utilisation : python3 socket_one2.py [OPTION]")
             print("(B.O.A est un serveur web écrit grâce à Python.\r")
             print("-v, --venv_path         Change defaut path(./)\r")
             print("-p, --port         Change defaut port(8081)\r")
             print("-s, --ssl          use https\r")
             print("-c, --sslcert          \r")
             print("-t, --timing       Change time to wait between each waiting connection(0.05)\r")
             print("-i, --iface        Select the principal interface (eth0)  and create/usefree virtueliface (eth0:0)\r")
             print("-a, --ip           \r")
             print("-l, --log          Choose the log's path and file (/var/log/boa1.log)\r")
             print("-G, --github       Github repo sync\r")
             print("-h, --help         Print this help\r")
             print("-S, --init            \r")
             print("-I, --INSTALL      Modify systemd/openrc/upstart/sysvinit to startup a webserver or a coupled client/server service pool - arg : web,pool \r")
             print("-U, --THISHIT      Uninstall the worst service\r")   # /!\ will never works
             print("-n, --name          \r")
             print("-R, --runfromconf   Run installed service, with name runing specific server, without name runing all servers (used by init apps) \r")
             print("Exemples")
             print("Standalone exemple : # python3 socket_one2.py -r /home/user/www/ -p 80 -i eth0 -l /home/user/var/log/ -t 0.05 \r")
             print("--------------------------------------------existing-path----^                                ^-existing-path---")
             print("Deamon exemple : # python3 socket_one2.py -I -r /home/user/mynewvenv/ -p 80 -l /home/user/var/log/ -t 0.05 \r")
             print("-------------------------------------creating venv here--------^ in case of error you need to edit manually conf")

             quit()
        try:
            arg = next(options)
        except StopIteration as e:
            arg = "main.py"
    if conf != False and install == "web" and name != False and venv_path != False and port_value != False and interface != False and uninstall == False: # install name, add section in config
        print("Start installation de " + name)
        configure = config_parse(conf,name)
        for elt in configure.config:
            if elt.name == [name]:
                print("'" + name + "'" + "is in config, choose an another name, aborted installation.")
                quit()
            elif elt.name == ["init"]:
                elt.assign()
                cfinit = elt

        cfg=myoptions.myoptions(name,conf,timetowait,venv_path,ssll,ssl_file,port_value,interface,ip,log,github,init,boot,user)
        cfg.localpool_newpart()
        print("configuration")
        cfg.writeconfig()
        if cfg.search_venv() is not True:
            print("l'environnement virtuel n'existe pas : création")
            cfg.configvenv() # a modifier : classe
        print("configuration de l'init")
        cfg.configinitinit(cfinit) # a modifier : classe

        print("Configuration de " + cfg.interface)
        netcfg = network.network(cfg.interface,cfg.ip,cfg.ssll,cfg.port)
        if netcfg.search_same_ip() is not True:
            print("searching slot")
            netcfg.search_virtual(cfg.interface)
            print("slot :" + str(netcfg.slot))
            print("reconstruction du fichier de config")
            netcfg.cur_conf = netcfg.readconf()
            netcfg.new_elt2 = netcfg.modconf()
            netcfg.writeconf()
            print("demarrage de l'interface reseau sur " +  cfg.interface+":"+str(netcfg.slot))
            netcfg.upforever()

    if conf != False and (install == "wwwpool" or install == "localpool") and name != False and port_value != False and interface != False and uninstall == False and poopool != False: # install name, add section in config
        print("Start installation de pool pour le server web : " + name)
        configure = config_parse(conf,name)
        for elt in configure.config:
            if elt.name == [name]:
                print("'" + name + "'" + " server exist, now pool's configuration")
            elif elt.name == ["init"]:
                elt.assign()
                cfinit = elt

        cfg=myoptions.myoptions(name,conf,timetowait,venv_path,ssll,ssl_file,port_value,interface,ip,log,github,init,boot,user,poopool)
        cfg.wwwpool_newpart()
        print("configuration")
        cfg.writeconfigpool()
        print("configuration de l'init")
        cfg.configinitinit(cfinit,install) # a modifier : classe

        print("Configuration de " + cfg.interface)
        netcfg = network.network(cfg.interface,cfg.ip,cfg.ssll,cfg.port)
        print(cfg.ip)
        if netcfg.search_same_ip() is not True:
            print("searching slot")
            netcfg.search_virtual(cfg.interface)
            print("slot :" + str(netcfg.slot))
            print("reconstruction du fichier de config")
            netcfg.cur_conf = netcfg.readconf()
            netcfg.new_elt2 = netcfg.modconf()
            netcfg.writeconf()
            print("demarrage de l'interface reseau sur " +  cfg.interface+":"+str(netcfg.slot))
            netcfg.upforever()

    elif uninstall == True and install == False and name != False: # uninstall from name delete section in config
        uninstall = config(name)
        uninstall.uninstallconf()
        uninstall.uninstallinit()
    elif install == False and name == False and venv_path != False and port_value != False and interface != False: # standalone from arg
        manager = multiprocessing.Manager()

        myerrors = errors.errors(manager)
        mylog = logg.logg(manager)
        mypool = poool.poool(manager)

        pool = multiprocessing.Pool()

        reserrors = pool.apply_async(myerrors.mainprocess)
        reslogs = pool.apply_async(mylog.mainprocess)
        respool = pool.apply_async(mypool.mainprocess)

        if poopool == "localpool":
            print("starting localpool")
            p = multiprocessing.Process(target=mypool.localpool_srv,args=(port_value,timetowait,interface,ip,myerrors,mylog,mypool,))
            p.start()
        elif poopool == "webpool":
            p = multiprocessing.Process(target=mypool.extpool_srv,args=(port_value,timetowait,interface,ip,myerrors,mylog,mypool,))
            p.start()
        elif poopool == False:
            event = sidewinder(port_value,venv_path,timetowait,interface,ip,peers)
            p = multiprocessing.Process(target=event.fire(myerrors,mylog,mypool))
            p.start()

    elif name != False and conf != False: # standalone from conf
        configure = config_parse(conf,name) # configure.options
        for elt in configure.config:
            if elt.name == [name]:
                elt.assign()

                manager = multiprocessing.Manager()

                myerrors = errors.errors(manager)
                mylog = logg.logg(manager)
                mypool = poool.poool(manager)

                pool = multiprocessing.Pool()

                reserrors = pool.apply_async(myerrors.mainprocess)
                reslogs = pool.apply_async(mylog.mainprocess)
                respool = pool.apply_async(mypool.mainprocess)
                
                event = sidewinder(elt.port,elt.venv_path,elt.timing,elt.interface,elt.ip,myerrors,mylog,mypool,elt.ssll,elt.ssl_file)
                p = multiprocessing.Process(target=event.fire)
                p.start()

    elif conf != False and name == False: # launch all servers from conf
        configure = config_parse(conf,name) # configure.options
        server = []
        th=[]
        for elt in configure.config:
            if elt.name != ["init"]:
                elt.assign()

                manager = multiprocessing.Manager()

                myerrors = errors.errors(manager)
                mylog = logg.logg(manager)
                mypool = poool.poool(manager)

                pool = multiprocessing.Pool()

                reserrors = pool.apply_async(myerrors.mainprocess)
                reslogs = pool.apply_async(mylog.mainprocess)
                respool = pool.apply_async(mypool.mainprocess)


                server.append(sidewinder(elt.port,elt.venv_path,elt.timing,elt.interface,elt.ip,myerrors,mylog,mypool,elt.ssll,elt.ssl_file))
                th.append(threading.Thread(target=server[-1].fire))
                th[-1].start()

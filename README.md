# proxySniffer
You can get the proxy IP from the free agent IP website


```sh
> git clone https://github.com/josexy/proxySniffer.git
> cd proxySniffer/proxySniffer
> ./proxySniffer.py --help
```


```sh
========================================
=======             =    = 
==   == proxySniffer =  =   **   ** 
==   ==               $      ** **
======= ===   +++     $       *** 
==      =  = +   +   = =      *** 
==      =    +   +  =   =     ***
==      =     +++  =     =    ***
===========2018:07:26 14:53:56==========

Usage: proxySniffer.py [-s [-o OFILE]] [-c -f FILE -o OFILE] [-u]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  --author              show the author info
  -u                    show the support proxy ip website
  -r MAXNUM, --reconnect=MAXNUM
                        test the proxy ip reconnect maximumn
  -c, --check           check the reporter proxies was available
  -f FILE, --filename=FILE
                        specify a host proxy file
  -o OFILE, --output=OFILE
                        output the file to disk,defalut:[stdout]
  -s, --search          search the free proxy on website

  Export SQL Database:
    You can export the proxy info to database

    --sqlite3=PATH      Export proxy to sqlite3 database 
```

#/usr/bin/python
import logging

logfile = "/data/fuliao_cmdb/logs/cmdb.log"

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a %d %b %Y %H:%M:%S',
                filename=logfile,
                filemode='a+')

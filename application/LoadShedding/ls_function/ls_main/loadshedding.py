#!/bin/python3.6
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
# System
import os 
import sys
import time
import argparse
import logging
import logging.handlers
# Non-System
from acsprism import rtdb_init


__author__ = 'Wilson Kuo'

LOG_FILENAME = 'load_shedding.log'
LOG_FORMAT   = '%(asctime)s [%(process)d] %(levelname)s %(name)s: %(message)s'

logger = logging.getLogger(__name__)

def setup_logger():
    #=====================================================================
    # Logging setup
    #=====================================================================
    # Set the logging level of the root logger
    # logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)

    # This sets timestamp for logging to UTC, otherwise it is local
    # logging.Formatter.converter = time.gmtime

    # Set up the console logger
    stream_handler = logging.StreamHandler()
    stream_formatter = logging.Formatter(LOG_FORMAT)
    stream_handler.setFormatter(stream_formatter)

    logging.getLogger().addHandler(stream_handler)

    # Set up the file logger
    log_dir = '/home/acs/tmp'
    log_filename = os.path.abspath(os.path.join(log_dir, LOG_FILENAME))
    max_bytes = 1 * 1024 * 1024  # 1 MB
    file_handler = logging.handlers.RotatingFileHandler(log_filename, maxBytes=max_bytes, backupCount=1)
    file_formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logging.getLogger().addHandler(file_handler)
    logger.info("Logging to file '%s'", log_filename)

def get_parser():
    """ The argument parser of the command-line version """
    parser = argparse.ArgumentParser(description="Loadshedding")
    parser.add_argument("-Amode"     , "--Amode"    , help="AMODE") 
    parser.add_argument("-mode"     , "--mode"      , help="MODE") 
    parser.add_argument("-group"    , "--group"     , help="GROUP") 
    parser.add_argument("-demand"   , "--demand"    , help="DEMAND") 
    parser.add_argument("-tablename", "--tablename" , help="TABLENAME") 
    parser.add_argument("-colname"  , "--colname"   , help="COLNAME") 
    parser.add_argument("-equip_num", "--equip_num" , help="EQUIP_NUM") 
    parser.add_argument("-rtdbtype" , "--rtdbtype"  , help="RTDBTYPE") 
    parser.add_argument("-station"  , "--station"   , help="STATION") 
    parser.add_argument("-category" , "--category"  , help="CATEGORY") 
    parser.add_argument("-point"    , "--point"     , help="POINT") 
    parser.add_argument("-attribute", "--attribute" , help="ATTRIBUTE") 
    parser.add_argument("-value"    , "--value"     , help="VALUE") 

    return {
        "Amode"     : args.Amode,
        "mode"      : args.mode,
        "group"     : args.group,
        "demand"    : args.demand,
        "tablename" : args.tablename,
        "colname"   : args.colname,
        "equip_num" : args.equip_num,
        "rtdbtype"  : args.rtdbtype,
        "category"  : args.category,
        "point"     : args.point,
        "attribute" : args.attribute,
        "value"     : args.value,
    }


def main(args):
    rtdb_init()

    error = False
    process = None


    if args['Amode'] in (0, 1):
        if args['mode'] == "0":
            if args['group'] is None:
                logger.critical("group is none")
                logger.critical("fail to start mode 0")
                return
            else:
                from loadshedding.restore import Restore
                process = Restore(args['Amode'], args['group'])

        elif args['mode'] == "1":
            if args['group'] is None:
                logger.critical("group is none")
                return
                
            if args['demand'] is None:
                logger.critical("demand is none")
                return

            else:
                try:
                    int(args['demand'])
                except:
                    logger.critical("demand is not number")
                    return

            if error:
                logger.critical("fail to start mode 1")
                return

            else:
                from loadshedding.bydemand import Bydemand
                process = Bydemand(args['Amode'], args['group'], int(args['demand']))
                
        elif args['mode'] == "2":
            if args['group'] is None:
                logger.critical("group is none")
                return
            if args['demand'] is None:
                logger.critical("demand is none")
                return
            else:
                try:
                    int(args['demand'])
                except:
                    logger.critical("demand is not number")
                    return
            if error:
                logger.critical("fail to start mode 2")
                return
            else:
                from loadshedding.rotating import Rotating
                process = Rotating(args['Amode'], args['group'])
        elif args['mode'] == "3":
            from loadshedding.uf import UF
            process = UF(args['Amode'])            

        else:
            raise NotImplementedError("rotating_mode {0} not implemented".format(args['mode'])

    if process:
        # process.start()
        return process


    
if __name__ == "__main__":
    setup_logger()
    parser = get_parser()
    args, unknown = parser.parse_known_args()
    p = main(args)  
          
    if p != None:
        p.start()


#python3 ls_main.py -mode 3 -tablename SWITCHINPUT -colname STASTATUS -equip_num WN_SBK -rtdbtype S -station 4001 -category P -point 5490 -attribute CS -value 1

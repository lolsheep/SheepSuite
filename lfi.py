#!/usr/bin/env python3

import sys
import argparse
import urllib
import urllib.request
import urllib.error
import time
import threading
import curses 
import requests 
from queue import Queue

from util import progress_bar
from args import *



q = Queue()


class sheep:

    def __init__(self,args=args_p):

        self.url = args.url
        self.wordlist = args.wordlist
        self.wl_content = []
        self.showHTTPErrorCode = args_p.show_all_http_requests
        self.threads = []




        # See if url is actually set
        if self.url == None:
            print("Must specify target url - http://<host_addr>/")
            sys.exit(0)
        # Test if host is actually up 
        
        if self.url[-1:] != "/":
            self.url += "/"

        try:

            test_req = urllib.request.urlopen(self.url)

        except ValueError as e:

            print("Please use a valid URL format - http://<host_addr>/ ")
            sys.exit(0)

        except urllib.error.HTTPError as e:

            pass

        except urllib.error.URLError as e:

            print(e.reason," No route to host.. Maybe it's down or something?")

            sys.exit(0)

        # Set wordlist to default if not specified

        if self.wordlist == None:
            
            print("Using default wordlist common.txt")
            self.wordlist = "wordlists/dirb/common.txt"


        # See if wordlist exists
        
        try:
            
            with open(self.wordlist, "r") as f:

                self.wl_content.append(f.read().splitlines())


        except OSError:

            print("File not found or readable. Exiting..")

            sys.exit(0)


        threading.Thread(target=self.send_req, daemon=True)


        self.send_tasks()


    def send_tasks(self):

        for i in self.wl_content[0]:
            q.put(i)

        self.send_req()
    

    def send_req(self):


        while True:
            i = q.get()
            code = 0


            req = requests.get(self.url+urllib.parse.quote(i))
            code = str(req.status_code) + "   " + req.reason
            # if code == 200:
            #     code = str(req.status_code) + "  OK       "
            # elif code == 404:
            #     code = str(req.status_code) + " NOT FOUND "



            print(f"{(self.url+i).ljust(46)}{code.rjust(0)}", end="\r")
            progress_bar(self.wl_content[0].index(i),len(self.wl_content[0]),str(self.wl_content[0].index(i))+"/"+str(len(self.wl_content[0])))

            q.task_done()
            time.sleep(1)
q.join()




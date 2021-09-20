#!/usr/bin/env python3


import urllib
import sys
import argparse
import time
import sys
import argparse
import urllib
import urllib.request
import urllib.error
import time
import threading
import queue
import requests 
import atexit
import signal
import traceback
import os
from termcolor import colored

from args import *
from util import *




class sheep:

	def __init__(self,args=args_p):

		self.url = args.url
		self.wordlist = args.wordlist
		self.wl_content = []
		self.quiet = args.quiet
		self.threads = []
		self.i = 0
		self.last_size = 0
		self.valid_results = []
		self.valid_lfi = []

		if args.ext:
			self.ext = "."+args.ext
		else:
			self.ext = ""
		if args_p.lfi:
			self.param = "?"+args_p.lfi+"="
		else:
			self.param = ""

		if self.url == None:
			print("Must specify target url - http://<host_addr>/")
			sys.exit(0)
			
		if self.url[-1:] != "/":
			self.url += "/"

		try:
			urllib.request.urlopen(self.url)
		except ValueError as e:
			print("Please use a valid URL format - http://<host_addr>/ ")
			sys.exit(0)
		except urllib.error.HTTPError as e:
			pass
		except urllib.error.URLError as e:
			print(e.reason," No route to host.. Maybe it's down or something?")
			sys.exit(0)


		try:
			r = requests.get(self.url)
			self.content_norm_size = len(r.content)

		except Exception:
			print("Unknown error (I guess)")
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


		self.wl_content = self.wl_content[0]


	def send_req(self):

		time.sleep(0.5)

		while not q.empty():

			i = self.param+q.get()
			code = 0
			bigger = ""

			if args_p.lfi:

				req = requests.get(self.url+self.param+urllib.parse.quote(i))
				content_size = len(req.content)

				if content_size > self.content_norm_size:

					content_size_str = "Size: "+str(content_size)
					bigger = True

				else: 
					content_size_str = "Size: "+str(content_size)
			else:

				req = requests.get(self.url+urllib.parse.quote(i)+self.ext)
				content_size_str = ""

			if req.status_code == 200:
				code = colored(str(req.status_code) + "   "+req.reason,"green")
				if args_p.lfi and content_size > self.content_norm_size:
					self.valid_lfi.append(req)
				else:
					self.valid_results.append(req)
			elif req.status_code == 403:
				code = colored(str(req.status_code) + "   "+req.reason,"red")
				self.valid_results.append(req)
			else:
				code = colored(str(req.status_code) + "   " + req.reason,"yellow")


			print(f"{(self.url+i+self.ext).ljust(65)}{code.rjust(30)}{content_size_str.rjust(20)}{colored('!!','red') if bigger else ''}")
			
			q.task_done()
			time.sleep(0.1)

	def after(self):

		if args_p.lfi:
			print("\n\nFound LFI results. Would you like to print here[p], save to file[s], or quit[q]?")
		elif len(s.valid_results) > 0:
			print("\n\nFound valid HTTP responses. Would you like to print here[p], save to a file[s], or quit[q]?")

		opt = input()

		if opt == "p":

			if args_p.lfi:
				for i in s.valid_lfi:
					print(i.content,'\n\n')
			else:
				for i in s.valid_results:
					print(i.content,'\n\n')


		elif opt == "s":

			path = "logs/lfi/"+return_date()

			if args_p.lfi:

				print("Saving..")

				for i in s.valid_lfi:

					if not os.path.exists(path):
						os.makedirs(path)


					with open(path+"/"+return_datetime()+".txt","w") as f:

						f.write(str(i.content)+"\n\n")

				print("Done. Saved to "+ path)

			else:

				path = "logs/http/"+return_date()
				fname = return_datetime()

				for i in s.valid_results:

					if not os.path.exists(path):
						os.makedirs(path)

					with open(path+"/"+fname+".txt","a") as f:
						f.write(str(i.url) + "  " + str(i.reason)+'\n\n')

				print("Done. Saved to "+ path)

		elif opt == "q":

			sys.exit(0)


if __name__ == '__main__':


	print(return_date())
	s = sheep()
	q = queue.Queue()
	th = []

	try:

		for j in s.wl_content:
			q.put(j)

		if args_p.t > 5:

			print(colored("WARNING: Program can behave unexpectedly if you use more than 5 threads!!!","red"),end="\n\n")
		
		if args_p.lfi:

			print("Starting in LFI mode. We search for results in LFI mode by matching the size of each response with the size of the response from the root URL. If the file is larger than others, then that means a result has been found.")

		for i in range(args_p.t):
			t = threading.Thread(target=s.send_req)
			t.daemon=True
			th.append(t)
			t.start()

		for t in th:
			t.join()

		q.join()
		s.after()

	except KeyboardInterrupt:
		
		print("",end='\r')
		q.queue.clear()
		time.sleep(1)
		s.after()
		pass

	else:

		pass








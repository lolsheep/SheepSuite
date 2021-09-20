#!/usr/bin/env python3
import argparse
import pyfiglet
from termcolor import colored
sheep_ascii = """         
	,ww
   wWWWWWWW_)
   `WWWWWW\'
    II  II
"""
ascii_banner1 = pyfiglet.figlet_format("Sheep Suite")

print(colored("===================================================","magenta"))
print(colored(ascii_banner1+sheep_ascii,"blue"))
print(colored("===================================================","magenta"))

# Init argument parser
parse = argparse.ArgumentParser(description="Welcome to sheep suite! I'm currently still developing this suite of scripts (alone), but I'm sure it'll be pretty dope when it's done."
	, prefix_chars="-")
# URL parser
urlparse = parse.add_argument("-u","--url", help= "Specify URL to attack",required=True)
#Wordlist parser
wlistparse = parse.add_argument("-w", "--wordlist", help="Specify a wordlist. If none is specified, will use default",required=False)

quiet = parse.add_argument("-q, ", "--quiet", help="Shows all http request codes for each item in wordlist",action="store_true",required=False)

threads = parse.add_argument("-t", help="Number of threads to use.", type=int, default=2)

http_param = parse.add_argument("-lfi", help="\nSwitch to LFI mode using HTTP params. Will use supplied wordlist.")

ext = parse.add_argument("-ext", help="\nSpecify which extension to look for (strict).")

args_p = parse.parse_args()


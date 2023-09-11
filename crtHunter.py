#!/usr/bin/env python3
# coding: utf-8
# crtHunter v2.0

# By Hazem El-Sayed - twitter.com/algohazm
# Import required libraries
import re
import requests
from bs4 import BeautifulSoup
import argparse
import sys
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

# Define the banner to be displayed when the script is run
BANNER = r'''

                  _     _                             
             _   | |   | |            _               
  ____  ____| |_ | |__ | |_   _ ____ | |_  ____  ____ 
 / ___)/ ___|  _)|  __)| | | | |  _ \|  _)/ _  )/ ___)
( (___| |   | |__| |   | | |_| | | | | |_( (/ /| |    
 \____|_|    \___|_|   |_|\____|_| |_|\___\____|_|    
                                                      

               Coded by : Hazem Elsayed
               Contributor : Yousef Mohamed
               @algohazm && @y0usSs3F
'''

# Function to extract subdomains using RegEx
def extract_subdomains(text, domain):
    subdomains = set()
    regex = re.compile(r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+' + re.escape(domain) + r'\b')
    matches = regex.findall(text)
    for match in matches:
        subdomains.add(match)
    return subdomains

# Function to get subdomains from crt.sh
def get_subdomains_crtsh(domain):
    subdomains = set()
    url = f"https://crt.sh/?q={domain}"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error: {str(e)}")
        return subdomains

    subdomains.update(extract_subdomains(response.text, domain))
    return subdomains

# Function to save subdomains to a file
def save_subdomains(subdomains, output_file):
    with open(output_file, "a") as f:
        for subdomain in subdomains:
            f.write(subdomain + "\n")

# Function to process multiple domains from a file
def process_domains_from_file(domain_file, output_file):
    with open(domain_file, "r") as f:
        domains = f.readlines()

    for domain in domains:
        domain = domain.strip()
        subdomains = get_subdomains_crtsh(domain)

        subdomain_count = len(subdomains)

        if subdomain_count > 0:
            print(Fore.GREEN + f"[§]Found {subdomain_count} unique subdomains for {domain}")

            if output_file:
                save_subdomains(subdomains, output_file)
                print(Fore.GREEN + f"[§]Subdomains saved to {output_file}")
            else:
                print(Fore.RED + "Subdomains:")
                for subdomain in subdomains:
                    print(Fore.GREEN + subdomain)
        else:
            print(Fore.RED + f"No subdomains found for {domain}")

        print(Fore.CYAN + f"Total number of subdomains: {subdomain_count}")
        print()

# Main function that runs the script
def main(domain, output_file, domain_file):
    if domain_file:
        print(Fore.CYAN + f"Processing domains from file {domain_file}...")
        process_domains_from_file(domain_file, output_file)
        return

    print(Fore.CYAN + "Extracting subdomains from crt.sh now...")
    subdomains = get_subdomains_crtsh(domain)

    subdomain_count = len(subdomains)

    if subdomain_count > 0:
        print(Fore.GREEN + f"[§]Found {subdomain_count} unique subdomains for {domain}")

        if output_file:
            save_subdomains(subdomains, output_file)
            print(Fore.GREEN + f"[§]Subdomains saved to {output_file}")
        else:
            print(Fore.RED + "Subdomains:")
            for subdomain in subdomains:
                print(Fore.GREEN + subdomain)
    else:
        print(Fore.RED + f"No subdomains found for {domain}")

    print(Fore.CYAN + f"Total number of subdomains: {subdomain_count}")

# The entry point of the script
if __name__ == "__main__":
    print(Fore.CYAN + BANNER)

    # Define command-line argument parser
    parser = argparse.ArgumentParser(description=Fore.YELLOW + Style.BRIGHT + "Find subdomains of a domain.")
    parser.add_argument("-d", "--domain", required=not bool(sys.stdin.isatty()), help=Fore.YELLOW + "The target domain.")
    parser.add_argument("-l", "--domain_file", required=False, help=Fore.YELLOW + "A file containing a list of domains to process (optional).")
    parser.add_argument("-o", "--output_file", required=False, help=Fore.RED + "The file to store subdomains into (optional).")
    

    # Check if there are any arguments provided
    if len(sys.argv) == 1 and sys.stdin.isatty():
        print(Fore.YELLOW + parser.description)
        print(Fore.CYAN + "Usage: python crtHunter.py -d DOMAIN OR -l DOMAINS_LIST [-o OUTPUT_FILE] ")
        sys.exit(1)

    # Parse the command-line arguments and run the main function
    args = parser.parse_args()

    if not args.domain and not args.domain_file:
        print(Fore.RED + "Error: you must provide either a target domain (-d) or a file containing a list of domains (-l)")
        sys.exit(1)

    main(args.domain, args.output_file, args.domain_file)

#!/usr/bin/env python3
# Import required libraries
import requests
from bs4 import BeautifulSoup
import argparse
import sys
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init(autoreset=True)

# Define the banner to be displayed when the script is run
BANNER = r'''
                           _______    _                 _                     
                   _      (_______)  (_)               | |                    
  ____     ____   | |_     _____      _    ____      _ | |    ____     ____   
 / ___)   / ___)  |  _)   |  ___)    | |  |  _ \    / || |   / _  )   / ___)  
( (___   | |      | |__   | |        | |  | | | |  ( (_| |  ( (/ /   | |      
 \____)  |_|       \___)  |_|        |_|  |_| |_|   \____|   \____)  |_|      
                                                                              
 _    _     __          ______                                                
| |  | |   /  |        / __   |                                               
| |  | |  /_/ |       | | //| |                                               
 \ \/ /     | |       | |// | |                                               
  \  /      | |   _   |  /__| |                                               
   \/       |_|  (_)   \_____/                                                
                                                                              
'''

# Function to get subdomains from crt.sh
def get_subdomains(domain):
    subdomains = set()
    url = f"https://crt.sh/?q=%.{domain}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table")
    if len(tables) >= 2:
        table = tables[1]
        rows = table.find_all("tr")[1:]
        for row in rows:
            tds = row.find_all("td")
            if len(tds) >= 5:
                subdomain = tds[4].text.strip()
                if subdomain.startswith("*."):
                    subdomain = subdomain[2:]
                if not subdomain.startswith("."):
                    subdomains.add(subdomain)
    return subdomains

# Function to save subdomains to a file
def save_subdomains(subdomains, output_file):
    with open(output_file, "w") as f:
        for subdomain in subdomains:
            f.write(subdomain + "\n")

# Main function that runs the script
def main(domain, output_file):
    print(Fore.CYAN + "Extracting subdomains from crt.sh now...")
    subdomains = get_subdomains(domain)
    if output_file:
        save_subdomains(subdomains, output_file)
        print(f"{Fore.GREEN}Subdomains saved to {output_file}")
    else:
        print(Fore.YELLOW + "Subdomains:")
        for subdomain in subdomains:
            print(Fore.GREEN + subdomain)

# The entry point of the script
if __name__ == "__main__":
    print(Fore.GREEN + BANNER)

    # Define command-line argument parser
    parser = argparse.ArgumentParser(description=Fore.YELLOW + Style.BRIGHT + "Get subdomains of a domain.")
    parser.add_argument("-d", "--domain", required=True, help=Fore.YELLOW + "The domain to search for subdomains.")
    parser.add_argument("-o", "--output_file", required=False, help=Fore.RED + "The file to store subdomains into (optional).")

    # Check if there are any arguments provided
    if len(sys.argv) == 1:
        print(Fore.YELLOW + parser.description)
        print(Fore.CYAN + "Usage: python crt.py -d DOMAIN [-o OUTPUT_FILE]")
        sys.exit(1)

    # Parse the command-line arguments and run the main function
    args = parser.parse_args()
    main(args.domain, args.output_file)
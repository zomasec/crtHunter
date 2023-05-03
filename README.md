# crtHunter.py V 1.1
there was previous version but i modify it to be petter
A Python script to extract subdomains for a given domain using the crt.sh website. This script utilizes `requests`, `BeautifulSoup`, `argparse`, and `colorama` libraries to fetch and parse the data and provide a user-friendly command-line interface with colored output.

## Features

- Extract subdomains for a given domain using crt.sh

- Save extracted subdomains to a text file (optional)

- Colored terminal output for better readability

## Prerequisites

Before running the script, you need to install the required libraries. You can do this by running:

```bash
pip install requests beautifulsoup4 colorama
```
## Usage

To use the script, run the following command in your terminal:

```bash
python crtHunter.py -d DOMAIN [-o OUTPUT_FILE]
```

- Replace `DOMAIN` with the domain you want to search for subdomains.

- The `-o OUTPUT_FILE` flag is optional. If provided, the script will save the extracted subdomains to the specified `OUTPUT_FILE`.
### Example

```bash

python crtHunter.py -d example.com -o subdomains.txt

```

This command will extract subdomains for `example.com` and save them to a file named `subdomains.txt`.

import sys
import argparse
import locale
import urllib

import requests
import BeautifulSoup

args = None
locale.setlocale( locale.LC_ALL, '' )
STANDARD_PATHS = ["Magic%202014%20(M14)", "Return%20to%20Ravnica", "Gatecrash", "Theros", "Dragon's%20Maze"]
BASIC_LANDS = ["Swamp", "Mountain", "Plains", "Island", "Forest"]
ROOT_URL = "http://magic.tcgplayer.com/db/price_guide.asp?setname="

def pull_lists(price_index):
    pricemap = {}

    for path in STANDARD_PATHS:
            dat = requests.get("%s%s" % (ROOT_URL, path))
            print "Fetched %s list" % urllib.unquote(path)
            soup = BeautifulSoup.BeautifulSoup(dat.text)
            table = soup.contents[11]
            pricemap = dict(
                pricemap.items() +
                {
                    a.contents[0].text.replace("&nbsp;", ""):
                    float(
                        a.contents[price_index].text
                        .replace("&nbsp;", "")
                        .replace("$", "")
                    )
                    for a in table.contents
                    if hasattr(a, 'contents')
                }.items()
            )
    return pricemap

def calculate_price(fname, pricemap, price_bracket, include_lands=False):
    total = 0
    with open(fname, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            if not line: continue
            cardname = " ".join(line.split()[1:])
            amount = int(line.split()[0].strip("x"))
            if cardname in BASIC_LANDS and not include_lands:
                continue
            to_add = pricemap[cardname]*amount
            total += to_add
            print "%s(%s/u): %s" % (line,
                locale.currency(pricemap[cardname], grouping=True),
                locale.currency(to_add, grouping=True))
        print "Total: %s (at %s price bracket)" % (locale.currency(total, grouping=True), price_bracket)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate cumulative price from a Magic .dec file')
    parser.add_argument('-f', '--file', type=str, nargs='+', help='.dec file to read')
    parser.add_argument('-p', '--price', type=str, nargs='+', help='The price bracket [low|mid|high]')
    parser.add_argument('-l', '--lands', action="store_true", help='Include the price of basic lands')
    args = parser.parse_args()

    if not args.file:
        raise ValueError("No file specified")

    price_bracket = args.price[0] if args.price else 'mid'
    if price_bracket == 'low':
        price_index = 7
    elif price_bracket == 'mid':
        price_index = 6
    elif price_bracket == 'high':
        price_index = 5

    pricemap = pull_lists(price_index)
    calculate_price(args.file[0], pricemap, price_bracket, include_lands=args.lands)

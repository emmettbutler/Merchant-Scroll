Merchant Scroll
===============

![](http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=2951&type=card)

A script that reads the
[tcgplayer.com card price lists](http://magic.tcgplayer.com/magic_price_guides.asp)
and calculates deck prices from .dec files.

File format
-----------

.dec is a simple plaintext file format that looks like this:

    2 Lightning Bolt
    2 Giant Growth
    4 Unsummon
    3 Storm Crow
    2 Jace, Memory Adept

Each line in the file references one card in the deck. The number indicates
how many of that card are included, and the name of the card is the official
ascii name of the card. For official name reference, use
[these lists](http://magic.tcgplayer.com/magic_price_guides.asp).

.dec files are exported from the deckbuilder on
[tappedout](http://tappedout.net).

Usage
-----

First, install dependencies with

    pip install -r requirements.txt

To use this script, simply invoke the python interpreter

    python merchant_scroll.py -f path/to/my/deck.dec

To see available command options, use

    python merchant_scroll.py --help

Notes
-----

Currently, Merchant Scroll only works for Standard-legal decklists. This is
because it reads card prices *per set* from the tcgplayer data, and pulling
all existing sets from the web is quite time-consuming.

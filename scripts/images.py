#!/usr/bin/env python
"""
Query MediaWiki API for article images

pageimages is typically what you want

References
    https://www.mediawiki.org/wiki/API:Images
    https://www.mediawiki.org/wiki/Extension:PageImages
    https://www.mediawiki.org/wiki/Extension:Popups
"""

from __future__ import print_function

import argparse
import os
import sys
import time

import wptools


def wpimages(title, source, test, verbose, wiki):
    start = time.time()
    data = wptools.get_images(title, source,
                              lead=False, test=test,
                              wiki=wiki, verbose=verbose)
    if test:
        print(data)
        sys.exit(os.EX_OK)

    data = wptools.extract.qry_images(data, source)
    print(data)

    print("%5.3f seconds" % (time.time() - start), file=sys.stderr)


def main():
    desc = "Query MediaWiki API for article images"
    epig = ("source=infobox is experimental\n"
            "you probably want source=pageimages")
    argp = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc,
        epilog=epig
    )
    argp.add_argument("title",
                      help="article title")
    argp.add_argument("source", choices=['images', 'pageimages', 'infobox'],
                      help="API entrypoint")
    argp.add_argument("-t", "-test", action='store_true',
                      help="show query and exit")
    argp.add_argument("-v", "-verbose", action='store_true',
                      help="HTTP status to stdout")
    wiki = wptools.fetch.WPToolsFetch.ENDPOINT
    argp.add_argument("-w", "-wiki", default=wiki, help="wiki (%s)" % wiki)

    args = argp.parse_args()

    wpimages(args.title, args.source, args.t, args.v, args.w)


if __name__ == "__main__":
    main()

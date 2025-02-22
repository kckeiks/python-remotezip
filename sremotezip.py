#!/usr/bin/env python
from datetime import datetime

from tabulate import tabulate
from remotezip import RemoteZip


def list_files(url, filenames):
    with RemoteZip(url, headers={'User-Agent': 'remotezip'}) as zip:
        if len(filenames) == 0:
            filenames = zip.namelist()
        data = [('Length', 'DateTime', 'Name')]
        for fname in filenames:
            zinfo = zip.getinfo(fname)
            dt = datetime(*zinfo.date_time)
            data.append((zinfo.file_size, dt.strftime('%Y-%m-%d %H:%M:%S'), zinfo.filename))
        print(tabulate(data, headers='firstrow'))


def extract_files(url, filenames, path):
    with RemoteZip(url, headers={'User-Agent': 'remotezip'}) as zip:
        if len(filenames) == 0:
            filenames = zip.namelist()
        for fname in filenames:
            print('Extracting {0}...'.format(fname))
            zip.extract(fname, path=path)


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description="Safe Unzip remote files")
    parser.add_argument('url', help='Url of the zip archive')
    parser.add_argument('filename', nargs='*', help='File to extract')
    parser.add_argument('-l', '--list', action='store_true', default=False, help='List files in the archive')
    parser.add_argument('-d', '--dir', default=f'{os.getcwd()}/output', help='Extract directory, default current directory')

    args = parser.parse_args()
    if args.list:
        list_files(args.url, args.filename)
    else:
        extract_files(args.url, args.filename, args.dir)
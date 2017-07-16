# -*- coding: utf-8 -*-

import sys
import optparse

def start_bot():
    from bot import updater
    updater.start_polling()
    updater.idle()




def run():

    appname = 'onobot'
    usage = '%prog'
    __version__ = '0.0.1'
    description = 'Description'
    epilog = 'Epilog'

    parser = optparse.OptionParser(
        prog=appname,
        usage=usage,
        version=__version__,
        description=description,
        epilog=epilog
    )

    parser.add_option(
        '--run',
        help='Start bot',
        action='store_true',
        default=False
    )

    opts, args = parser.parse_args(sys.argv[1:])
    if opts.run is True:
        start_bot()



if __name__ == '__main__':
    run()

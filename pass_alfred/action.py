import re
import os
import sys

import sh
import alp
from alp import Item, Notification


def main():
    query = ' '.join(alp.args()).strip()
    try:
        if query.startswith('pass '):
            _pass = sh.Command('pass')
            output = _pass(query.split(' ')[1:])
            output = output.split('\n')[1].strip()[9:-4]
        else:
            output = query
        sys.stdout.write(output)
    except:
        pass


if __name__ == '__main__':
    main()

import os

import sh
import alp
from alp import Item, Notification


def show(query):
    _pass = sh.Command('pass')
    try:
        output = _pass.show(query)
        output = output.strip()
        if '\n' in output:
            return None
        else:
            return output
    except sh.ErrorReturnCode_1:
        return None


def find(query):
    query = query.lower()
    matches = []
    store = os.environ['PASSWORD_STORE_DIR']
    for (root, dirs, files) in os.walk(store):
        r = root.replace(store, '', 1).lstrip('/')
        for f in [f[:-4] for f in files if f .endswith('.gpg')]:
            path = os.path.join(r, f)
            if query in path.lower():
                matches.append(path)
    return matches


def main():
    query = ' '.join(alp.args()).strip()
    items = []
    password = show(query)
    if password is not None:
        items.append(Item(
            title=password,
            subtitle='Press enter to copy',
            valid=True,
            arg=password))
        items.append(Item(
            title='Update: %s' % query,
            subtitle='Randomly generate a 32 character password',
            valid=True,
            arg='pass generate --in-place --no-symbols %s 32' % query))
        items.append(Item(
            title='Remove: %s' % query,
            subtitle='Delete this password from the store',
            valid=True,
            arg='pass rm --force %s' % query))
    else:
        for m in find(query):
            try:
                subtitle, title = m.rsplit('/', 1)
            except:
                title = m
                subtitle = ''
            items.append(Item(
                title=title,
                subtitle=subtitle,
                valid=False,
                autocomplete=m))
        items.append(Item(
            title='Insert: %s' % query,
            subtitle='Randomly generate a 32 character password',
            valid=True,
            arg='pass generate --no-symbols %s 32' % query))
    alp.feedback(items)


if __name__ == '__main__':
    main()

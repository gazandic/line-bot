from __future__ import unicode_literals


class Action:
    def dispatch(self, *args):
        return self.act(*args)

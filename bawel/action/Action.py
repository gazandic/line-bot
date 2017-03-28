from __future__ import unicode_literals

class Action:
    def dispatch(self, *args):
        return self.act(*args)

def dispatch_action(action, state, *args):
    return action().dispatch(state, *args)

# dispatch_action(Action(), {}, (jancok, makanbeling,))
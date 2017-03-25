from __future__ import unicode_literals

class Action:
    def dispatch(self, state, *args):
        self.act(state, *args)

def dispatch_action(action, state, *args):
    return action().dispatch(state, *args)

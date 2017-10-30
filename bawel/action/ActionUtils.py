from bawel.constant.StateConstant import (
    STATE_ADD_JADWAL,
    STATE_DELETE_JADWAL,
    STATE_ADD_PENGELUARAN,
    STATE_DELETE_PENGELUARAN,
    STATE_SHOW_PENGELUARAN,
    ACTION_MAPPER
)
from bawel.util.RequestParser import RequestParser


def dispatch_action(action, *args):
    return action().dispatch(*args)


def handle_action(raw_text, text, state, reminder, nlptext, gmaps):
    parser = RequestParser()
    state, param = parser.parse(text, state)
    if STATE_ADD_JADWAL <= state['state_id'] <= STATE_DELETE_JADWAL:
        param.append(reminder)
    if state['state_id'] == STATE_ADD_PENGELUARAN:
        param.insert(3, state)
    elif state['state_id'] == STATE_DELETE_PENGELUARAN:
        param.insert(1, state)
    elif state['state_id'] == STATE_SHOW_PENGELUARAN:
        param.insert(0, state)
    else:
        param.append(state)

    if state['state_id'] == STATE_ADD_JADWAL:
        ent = nlptext.getEntities(raw_text)
        loc_name = list(ent.filter(lambda e: e['entity'] == "LOCATION").map(lambda e: e["fragment"]))
        loc_coord = gmaps.searchLoc(loc_name)
        param.append(loc_coord)

    return dispatch_action(ACTION_MAPPER[state['state_id']], *param)

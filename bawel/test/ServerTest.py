from bawel.util.RequestParser import RequestParser
from bawel.test.mock.ActionMapperMock import ACTION_MAPPER

parser = RequestParser()
state = { 'id': 123 }

while (True):
    text = input()
    state, param = parser.parse(text, state)
    param.append(state)

    # TEST ONLY
    print(ACTION_MAPPER[state['state_id']], *param)

    # THIS IS THE REAL THING
    # state, output = ACTION_MAPPER[state['state_id']](*param)
    # print(output)
    
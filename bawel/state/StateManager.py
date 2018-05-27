from typing import Dict, Optional, Union

from bawel.model.State import State

class StateManager:

    @staticmethod
    def fetch(uid: str) -> Optional[State]:
        st = State()
        return st.search_one({"uid": uid})

    @staticmethod
    def update(uid: str, updated_state: Dict) -> State:
        st = State()
        st = st.search_one({"uid": uid})
        if st is None:
            st = State(uid, updated_state)
            return st.create()
        else:
            st.set_state(updated_state)
            return st.update()

# print(StateManager.fetch("abc"))
# StateManager.update("abc", [123])
# print(StateManager.fetch("abc"))
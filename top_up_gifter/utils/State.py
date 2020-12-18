class State:
    
    START = 10
    LINK = 20
    CHOOSE_OPERATOR = 30
    GET_PHONE = 40
    CLAIMED = 50

    STATE_QUERIES = {
        START: ['link', 'fa', 'en'],
        LINK: ['choose_operator','back'],
        CHOOSE_OPERATOR: ['get_phone', 'back'],
        GET_PHONE: ['back'],
        CLAIMED: []
    }

    @staticmethod
    def get_previous_state(state):

        if state == State.LINK:
            return State.START
        if state == State.CHOOSE_OPERATOR:
            return State.LINK
        if state == State.GET_PHONE:
            return State.CHOOSE_OPERATOR

    @staticmethod
    def is_valid_query(state, action: str):
        return action in State.STATE_QUERIES[state]
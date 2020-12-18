class User:
    def __init__(self, user_info:dict):

        self.id = user_info['id']
        self.context_id = user_info['contextId']
        self.language = user_info['lang']
        self.state = user_info['state']
        self.current_message_id = user_info['currentMessageId']
        self.is_waiting_for_phone = user_info['isWaitingForPhone']
        self.operator = user_info['operator']
        self.is_awarded = user_info['isAwarded']
        self.ref_code = user_info['refCode']
        self.last_interaction = user_info['lastInteraction']
        # for key in user_info:
        #     setattr(self, key, user_info[key])

    def to_dict(self):
        return dict(
                    id=self.id,
                    contextId=self.context_id,
                    lang=self.language,
                    state=self.state,
                    currentMessageId=self.current_message_id,
                    isWaitingForPhone=self.is_waiting_for_phone,
                    operator=self.operator,
                    isAwarded=self.is_awarded,
                    refCode=self.ref_code,
                    lastInteraction=self.last_interaction
                )
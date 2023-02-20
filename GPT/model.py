class param:
    def __init__(self, temp, max_tokens, top_p, frequency_penalty, present_penalty, chunk_count, chunk_size):
        self.temp = temp
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.present_penalty = present_penalty
        self.chunk_count = chunk_count
        self.chunk_size = chunk_size


class Model:
    def __init__(self, question_model, other_models):
        self.question_model = question_model
        self.other_models = other_models


class Operation:
    def __init__(self, operations, operations_no_question):
        self.operations = operations
        self.operations_no_question = operations_no_question

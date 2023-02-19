class param:
    def __init__(self, temp, max_tokens, top_p, frequency_penalty, present_penalty, chunk_count, chunk_size):
        self.temp = temp
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.present_penalty = present_penalty
        self.chunk_count = chunk_count
        self.chunk_size = chunk_size

from jamo import h2j, j2hcj


class Bigram(dict):
    def __init__(self, word):
        self.node = word
        self.bg = self.getBigram(word)

        super().__init__({"node": self.node, "bg": self.bg})

    def getBigram(self, word):
        word = "^" + j2hcj(h2j(word)) + "$"
        result = []
        for i, j in zip(word, word[1:]):
            txt = i + j
            result.append(txt)

        return result

    def __repr__(self):
        return f"node: {self.node}\nbg: {self.bg}\n"

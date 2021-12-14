from jamo import h2j, j2hcj


class Node(dict):
    def __init__(self, word):
        self.node = word
        self.neighbors = []
        self.bg = self.getBigram(word)

        if isinstance(word, dict):
            for key in word:
                if key != "neighbors":
                    setattr(self, key, word[key])
                else:
                    neighbor = []
                    for nei in word[key]:
                        neighbor.append(Neighbor(nei))

                    setattr(self, key, neighbor)

        super().__init__(
            {"node": self.node, "neighbors": self.neighbors, "bg": self.bg}
        )

    def getBigram(self, word):
        word = "^" + j2hcj(h2j(word)) + "$"
        result = []
        for i, j in zip(word, word[1:]):
            txt = i + j
            result.append(txt)

        return result

    def edit_node(self, word):
        self.node = word

    def append_neighbors(self, word_list: list):
        self.neighbors += word_list

    def add_neighbors(self, word, weight=0):
        neigh = Neighbor(word, weight)
        self.neighbors.append(neigh)

    def set_neighbors(self, data: list):
        setattr(self, "neighbors", data)

    def update_neighbors(self, word, weight):
        for n in self.neighbors:
            if n.node == word:
                print("update ", word, weight)
                setattr(n, "weight", weight)
                # n.update_weight(weight)

        return self

    def delete_neighbors(self, neighbor_word):
        for idx, n in enumerate(self.neighbors):
            if n.node == neighbor_word:
                del self.neighbors[idx]
                break

    def get_neighbors(self):
        return self.neighbors

    def __repr__(self):
        return f"node: {self.node}\nneighbors: {self.neighbors}\n"


class Neighbor(dict):
    def __init__(self, word, weight=0):
        self.node = word
        self.weight = weight
        if isinstance(word, dict):
            for key in word:
                setattr(self, key, word[key])
        super().__init__({"node": self.node, "weight": self.weight})

    def update_weight(self, weight):
        setattr(self, "weight", weight)

    def __repr__(self):
        return "{" + f"node: {self.node}\nweight: {self.weight}\n" + "}"

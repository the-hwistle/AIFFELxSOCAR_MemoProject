from soynlp.noun import LRNounExtractor


def noun_extractor(data: list):
    noun_extractor = LRNounExtractor()
    nouns = noun_extractor.train_extract(data)
    nouns = sorted(nouns.items(), key=(lambda x: x[1].frequency), reverse=True)
    return nouns

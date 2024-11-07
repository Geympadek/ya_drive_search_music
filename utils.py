def count_deviations(word: str, sentence: str) -> int:
    '''
    Count the difference between word and the closest thing to it in the sentence
    '''
    word = word.lower()
    sentence = sentence.lower()

    word_len = len(word)

    filler = '\0' * max(0, word_len - len(sentence))
# костыль. allows for the use of shorter sentence than word
    sentence = f"{filler}{sentence}{filler}"

    min_deviations = word_len

    # iterate through every possible match
    for i in range(len(sentence) - word_len + 1):
        slice = sentence[i : i + word_len]

        deviations = sum(1 for w, s in zip(word, slice) if w != s)
        min_deviations = min(min_deviations, deviations)
    
    return min_deviations

def similarity(query: str, file: str) -> float:
    '''
    Finds similarity between query and file name
    returns float from 0 to 1
    '''

    words = query.split()

    similarity = 0
    for word in words:
        similarity += 1 - count_deviations(word, file) / len(word)
        
    return similarity / len(words)
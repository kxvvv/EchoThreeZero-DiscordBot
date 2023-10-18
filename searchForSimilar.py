
def levenshtein_distance(word1, word2):
    if len(word1) < len(word2):
        return levenshtein_distance(word2, word1)

    if len(word2) == 0:
        return len(word1)

    previous_row = range(len(word2) + 1)
    for i, c1 in enumerate(word1):
        current_row = [i + 1]
        for j, c2 in enumerate(word2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def find_similar_words(input_word, word_list, max_distance):
    similar_words = []
    for word in word_list:
        distance = levenshtein_distance(input_word, word)
        if distance <= max_distance:
            similar_words.append((word, distance))
    return similar_words



def TrySearchForSimilar(players, input, max_distance = 2):

    similar_words = find_similar_words(input, players, max_distance)
    return similar_words

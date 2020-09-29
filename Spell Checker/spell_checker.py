# Created by Vaishali Jain and Vinayak Gupta

from collections import Counter


def custom_tokeniser(text):
    """
        Takes text string as input and returns tokenised text as a list.
    """
    result = [text]
    for punc in ['.', ',', '\n', ' ', '\t', '[', ']', '(', ')', '{', '}', ';', "'", '"', '-']:
        new_result = []
        for sentence in result:
            token_list = sentence.split(punc)
            first = True
            for token in token_list:
                if not first:
                    new_result.append(punc)
                else:
                    first = False
                new_result.append(token)
        result = new_result
    return result


def tokenized_data_counter(tokenized_data):
    """
        Takes tokenised text list as input and return a dict that provides frequency of each token.
    """
    counter = Counter(map(str.lower, tokenized_data))
    return dict(counter)


def get_vocab_set():
    """
        Gets the vocabulary set from the file.
    """
    vocab_set = set()
    with open('words_alpha.txt', 'r') as f:
        for line in f:
            vocab_set.add(line.strip())
    return vocab_set


def min_distance(word1, word2):
    """
        Calculates and returns the Levenshtein distance between 2 words
    """
    matrix = [[max(0, abs(j - i)) if (i == 0 or j == 0) else 0 for j in range(1 + len(word2))] for i in
              range(1 + len(word1))]
    for i in range(1, len(word1) + 1):
        for j in range(1, len(word2) + 1):
            sub_incr = 0 if word1[i - 1] == word2[j - 1] else 1
            matrix[i][j] = min(sub_incr + matrix[i - 1][j - 1], 1 + min(matrix[i - 1][j], matrix[i][j - 1]))
    return matrix[len(word1)][len(word2)]


def find_among_best_words(best_words, tokenized_data_dict):
    """
        Finds the most commonly occuring word among the list of words with minimum Levensthein distance
    """
    best_word = best_words[0]
    freq = 0
    for word in best_words:
        if (word in tokenized_data_dict) and (tokenized_data_dict[word] > freq):
            freq = tokenized_data_dict[word]
            best_word = word
    return best_word


def find_min_distance_word(token, vocab_set, tokenized_input_counter):
    """
        Iterates through the dictionary to find the best word to replace the spelling mistake
    """
    min_dist = len(token)
    best_words = []
    for vocab_word in vocab_set:
        if abs(len(token) - len(vocab_word)) <= min_dist:
            curr_dist = min_distance(token.lower(), vocab_word.lower())
            if curr_dist < min_dist:
                min_dist = curr_dist
                best_words = [vocab_word]
            elif curr_dist == min_dist:
                best_words.append(vocab_word)
    return find_among_best_words(best_words, tokenized_input_counter)


def custom_detokeniser(token_list):
    """
        Performs detokenization by joining all the tokens
    """
    return "".join(token_list)


def spell_checker(input_data):
    """
        Performs tokenization, spell checking and detokenization by calling the appropriate functions
    """
    tokenized_input = custom_tokeniser(input_data)
    tokenized_input_counter = tokenized_data_counter(tokenized_input)
    tokenized_input = tokenized_input
    vocab_set = get_vocab_set()
    dictionary = {}
    tokenized_output = []
    for token in tokenized_input:
        if (not token.isalpha()) or (token.lower() in vocab_set):
            tokenized_output.append(token)
        else:
            if token in dictionary:
                tokenized_output.append(dictionary[token])
            else:
                if len(token) > 0 and (ord(token[0]) >= 97 and ord(token[0]) <= 122) or (
                        ord(token[len(token) - 1]) <= 90 and ord(
                    token[len(token) - 1]) >= 65):  # starting with small letter or containing all capital letter
                    best_word = find_min_distance_word(token, vocab_set, tokenized_input_counter)
                    if ord(token[len(token) - 1]) <= 90:
                        best_word = best_word.upper()
                    dictionary[token] = best_word
                    print(token, best_word)
                    tokenized_output.append(best_word)
                else:
                    tokenized_output.append(token)
    output_data = custom_detokeniser(tokenized_output)
    return output_data


def get_input_text(filename):
    """
        Reads the input file from the filename specified
    """
    with open(filename, 'r') as file:
        data = file.read()
    return data


def write_output_text_to_file(output_text):
    """
        Writes string to an output file
    """
    text_file = open("austen-sense-corrected.txt", "wt")
    text_file.write(output_text)
    text_file.close()


if __name__ == "__main__":
    input_file = 'austen-sense-corrupted.txt'
    input_data = get_input_text(input_file)
    output_data = spell_checker(input_data)
    write_output_text_to_file(output_data)

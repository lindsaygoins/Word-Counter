# Author: Lindsay Goins
# Description: Implements a word counter that counts the number of words in a file. It returns a list of tuples
# showing the top X words from the specified file.

import re
from hash_map import HashMap

rgx = re.compile("(\w[\w']*\w|\w)")


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


def top_words(source, number):
    """
    Summary: Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top "number" of words in a list of tuples of the form (word, count).
    Parameters: Source (file name containing the text) and Number (the desired amount of words to return)
    Returns: A list of tuples of the form (word, count), sorted by most common word.
    """
    ht = HashMap(2500, hash_function_2)

    # This block of code will read a file one word as a time and put the word in "w"
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                w = w.lower()
                count = 1

                # put the keys and values into the hash map, updating the value every time there is another occurrence
                # of the word, word is the "key" and number of occurrences is the "value"
                if ht.contains_key(w):
                    count = ht.get(w)
                    count += 1
                    ht.put(w, count)
                else:
                    ht.put(w, count)

    count_bucket = 0
    word_sort = []

    # search through the buckets and append each key-value pair as a tuple to the list to be sorted
    for bucket in ht._buckets:
        count_bucket += 1
        cur_node = ht._buckets[count_bucket - 1].head

        while cur_node is not None:
            word_sort.append((cur_node.key, cur_node.value))
            cur_node = cur_node.next

    sort_list = sorted(word_sort, key=lambda count: count[1], reverse=True)
    return sort_list[:number]

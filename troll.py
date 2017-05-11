"""Troll.py."""
import nltk as n
import random


def troll(string):
    """Do the troll."""
    sentence_struct = []
    words = []
    punctuation = []
    try:
        # Get list of tuples (word, part of speech)
        tags = n.pos_tag(n.word_tokenize(string))
        for i, (word, tag) in enumerate(tags):
            # Skip None values that are created by contractions
            if word is None:
                continue
            # Casing will be handled later
            word = word.lower()
            # Handle casing for 'I'
            if word == 'i':
                word = word.upper()
            # Translate tag to a simpler format
            simple_tag = n.tag.mapping.map_tag('en-ptb', 'universal', tag)
            # Handle contractions so that it remains a single word
            if i + 1 < len(tags):
                next_word, next_tag = tags[i + 1]
                if '\'' in next_word:
                    # Fuse the contraction back together
                    word += next_word
                    # This is a noun-based contraction (I've)
                    if simple_tag == 'NOUN' or simple_tag == 'PRON':
                        simple_tag = 'NCONT'
                    # This is a verb-based contraction (Could've)
                    elif simple_tag == 'VERB':
                        simple_tag = 'VCONT'
                    # Now that the contraction is one word, create a blank
                    tags[i + 1] = (None, None)
            # Build the sentence structure that will be substituted into
            sentence_struct.append(simple_tag)
            # Build collection of words and punctuation for substituting
            if simple_tag == '.':
                punctuation.append(word)
            else:
                words.append((word, simple_tag))
    except Exception as e:
        print(str(e))
    # print(str(sentence_struct) + '\n' + str(punctuation) + '\n' + str(words))

    # Shuffle the order of the words but NOT the punctuation
    random.shuffle(words)
    # Fill in the sentence structure in-place
    for i in range(len(sentence_struct)):
        # Replace punctuation type spot with same punctuation as original
        if sentence_struct[i] == '.':
            # Add a space conditionally depending on punctuation
            sentence_struct[i] = punctuation.pop(0)
            if not any(punc in sentence_struct[i] for punc in ["``"]):
                sentence_struct[i] += ' '
        else:
            # Find a word with a matching part of speech
            for word, part_of_speech in words:
                if sentence_struct[i] == part_of_speech:
                    # Replace the spot with the word
                    sentence_struct[i] = word
                    # Make sure not to reuse words
                    words.remove((word, part_of_speech))
                    # Capitalize the word if it is the beginning of a sentence
                    if i == 0 or any(punc in sentence_struct[i - 1]
                                     for punc in ['.', '!', '?']):
                        sentence_struct[i] = sentence_struct[i].capitalize()
                    # Add a space after the word if next spot isn't punctuation
                    if (i + 1 < len(sentence_struct) and
                       sentence_struct[i + 1] != '.'):
                        sentence_struct[i] += ' '
                    # Done, break the word search loop
                    break
    print('\n' + ''.join(sentence_struct))
    # print(str(words) + '\n' + str(punctuation))

troll(raw_input("Enter sentence to troll: "))

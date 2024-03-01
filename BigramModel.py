import os
import nltk
import math
from nltk.tokenize import word_tokenize
nltk.download('punkt')


# might be useful?
from collections import Counter


def read_files_in_directory(directory_path):
    # Define filler words
    filler_words = ['a', 'an', 'and', 'are', 'as', 'at', 'but', 
        'for', 'if', 'in', 'is', 'it', 'no', 'not', 'of', 
         'or', 'that', 'the', 'their', 'then', 'there', 'these', 
        'they', 'this', 'to', 'was', 'will', 'with']
    
    # Dictionary to store word frequencies for each genre
    genre_word_frequency = {}
    
    # Dictionary to store word pair frequencies for each genre
    genre_word_pair_frequency = {}
    
    # Iterate over genres
    for genre in os.listdir(directory_path):
        genre_folder = os.path.join(directory_path, genre)  # Full path to genre folder
        
        # Dictionary to store word frequencies for files in this genre
        word_frequency = {}
        
        # Dictionary to store word pair frequencies for files in this genre
        word_pair_frequency = {}
        
        # Iterate over files in the genre folder
        for file_name in os.listdir(genre_folder):
            file_path = os.path.join(genre_folder, file_name)  # Full path to the file
            with open(file_path, 'r') as rfile:
                for line in rfile:
                    current_line = line.strip()
                    tokens = current_line.split()  # Split line into words

                    # Update word frequency dictionary
                    for word in tokens:
                        if word in word_frequency:
                            word_frequency[word] += 1
                        else:
                            word_frequency[word] = 1

                    # Generate pairs of adjacent words
                    word_pairs = [(tokens[i], tokens[i+1]) for i in range(len(tokens) - 1)]

                    # Update word pair frequency dictionary
                    for pair in word_pairs:
                        if pair in word_pair_frequency:
                            word_pair_frequency[pair] += 1
                        else:
                            word_pair_frequency[pair] = 1
        
        # Store word frequencies for this genre
        genre_word_frequency[genre] = word_frequency
        
        # Store word pair frequencies for this genre
        genre_word_pair_frequency[genre] = word_pair_frequency
    
    return genre_word_frequency, genre_word_pair_frequency


def freq_to_prob(dic_word_freq, dic_pair_freq):
    pair_probabilities = {}
    vocabulary_size = len(dic_word_freq)
    
    for pair, freq in dic_pair_freq.items():
        word_1 = pair[0]
        word_1_freq = dic_word_freq.get(word_1, 0)  # Frequency of word_1, default to 0 if not found
        probability = (freq + 1) / (word_1_freq + vocabulary_size)
        pair_probabilities[pair] = probability
    
    return pair_probabilities


# def calculate_probability(dic_term_prob, input_text):
#     prob = 0.0

#     # Split the input text into pairs of adjacent words
#     word_pairs = [(input_text[i], input_text[i+1]) for i in range(len(input_text) - 1)]

#     # Iterate over pairs of words in the input text
#     for word_pair in word_pairs:
#         if word_pair in dic_term_prob:
#             pair_probability = dic_term_prob[word_pair]  # Retrieve probability of the word pair
#             prob += math.log10(pair_probability)  # Add logarithm of the probability

#     return prob

def calculate_probability(dic_term_prob, input_text):
    prob = 0.0

    # Split the input text into pairs of adjacent words
    word_pairs = [(input_text[i], input_text[i+1]) for i in range(len(input_text) - 1)]

    # Iterate over pairs of words in the input text
    for word_pair in word_pairs:
        if word_pair in dic_term_prob:
            pair_probability = dic_term_prob[word_pair]  # Retrieve probability of the word pair
            #print(f"Pair: {word_pair}, Probability: {pair_probability}")
            prob += math.log10(pair_probability)  # Add logarithm of the probability
        #else:
            #print(f"Pair not found: {word_pair}")

    return prob


def main():
    directory_path = 'assignment2folder/TM_CA1_Lyrics'

    # Step 1: Read files in the directory and calculate term frequencies for each genre
    genre_word_freq, genre_word_pair_freq = read_files_in_directory(directory_path)
    print("Word Frequency:")
    print(genre_word_freq)
    print("\nWord Pair Frequency:")
    print(genre_word_pair_freq)
    
    # Step 2: Calculate probabilities for word pairs
    genre_word_pair_probabilities = {}
    for genre, word_pair_freq in genre_word_pair_freq.items():
        genre_word_pair_probabilities[genre] = freq_to_prob(genre_word_freq[genre], word_pair_freq)
    print("\nWord Pair Probabilities:")
    print(genre_word_pair_probabilities)

    # Step 3: Provide some sample input text
    input_text = '''We're talkin' away I don't know what I'm to say I'll say it anyway Today's another day to find you
    Shying away I'll be comin' for your love, okay'''

    print("\nInput Text:")
    print(input_text)

    # Step 4: Calculate probabilities of the input text belonging to each genre
    probabilities_per_genre = {}
    for genre, word_pair_prob in genre_word_pair_probabilities.items():
        print(f"\nGenre: {genre}")
        probabilities_per_genre[genre] = calculate_probability(word_pair_prob, input_text.split())
        print(f"Probability: {probabilities_per_genre[genre]}")

    # Step 5: Print the probabilities for each genre
    print("\nProbabilities of the input text belonging to each genre:")
    for genre, prob in probabilities_per_genre.items():
        print(f"{genre}: {prob}")

if __name__ == '__main__':
    main()


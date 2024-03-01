import os
import math
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')


# might be useful?
from collections import Counter


import os

def read_files_in_directory(directory_path):
    # Define filler words
    filler_words = ['a', 'an', 'and', 'are', 'as', 'at', 'but', 
        'for', 'if', 'in', 'is', 'it', 'no', 'not', 'of', 
         'or', 'that', 'the', 'their', 'then', 'there', 'these', 
        'they', 'this', 'to', 'was', 'will', 'with']
    
    # Dictionary to store term frequencies for each genre
    genre_dic = {}
    
    # Iterate over genres
    for genre in os.listdir(directory_path):
        genre_folder = os.path.join(directory_path, genre)  # Full path to genre folder
        genre_term_frequency = {}  # Dictionary to store term frequencies for files in this genre
        
        # Iterate over files in the genre folder
        for file_name in os.listdir(genre_folder):
            file_path = os.path.join(genre_folder, file_name)  # Full path to the file
            with open(file_path, 'r') as rfile:
                for line in rfile:
                    current_line = line.strip()
                    # pre-process each line if you want to and save the results in current_line
                    tokens = nltk.word_tokenize(current_line.lower())
                    tokens = [word for word in tokens if word.isalpha()]
                    filtered_tokens = [word for word in tokens if word not in filler_words]
                    current_line = ' '.join(filtered_tokens)
                    tokens = word_tokenize(current_line)

                    # process the tokens and update your dictionary
                    for word in tokens:
                        if word in genre_term_frequency:
                            genre_term_frequency[word] += 1
                        else:
                            genre_term_frequency[word] = 1
        
        # Store the term frequencies for this genre
        genre_dic[genre] = genre_term_frequency

    return genre_dic



def freq_to_prob(dic_term_frequency):
    dic_term_prob = {}
    sum = 0

    dic_term_prob .update(dic_term_frequency)
    # YOUR CODE
    for word in dic_term_frequency:

        sum += dic_term_frequency[word]

    for word in dic_term_frequency:

        dic_term_prob[word] = dic_term_frequency[word]/sum 

    return dic_term_prob


def calculate_probability(dic_term_prob, input_text):
    prob = 0.0

    for word in input_text:
        if word in dic_term_prob:
            prob += math.log10(dic_term_prob[word])

    return prob


def main():
    # Specify the directory path where your genre folders and files are located
    directory_path = 'assignment2folder/TM_CA1_Lyrics'  # Update this path with the actual directory path

    # Step 1: Read files in the directory and calculate term frequencies for each genre
    genre_term_frequencies = read_files_in_directory(directory_path)
    print("Term frequencies for each genre:")
    print(genre_term_frequencies)
    
    # Step 2: Convert term frequencies to probabilities for each genre
    genre_probabilities = {}
    for genre, term_frequency in genre_term_frequencies.items():
        genre_probabilities[genre] = freq_to_prob(term_frequency)
    print("\nProbabilities for each genre:")
    print(genre_probabilities)

    # Step 3: Provide some sample input text
    input_text = '''We're talkin' away I don't know what I'm to say I'll say it anyway Today's another day to find you
    Shying away I'll be comin' for your love, okay'''.split()

    # Step 4: Calculate probabilities of the input text belonging to each genre
    probabilities_per_genre = {}
    for genre, term_prob in genre_probabilities.items():
        probabilities_per_genre[genre] = calculate_probability(term_prob, input_text)

    # Step 5: Print the probabilities for each genre
    print("\nProbabilities of the input text belonging to each genre:")
    for genre, prob in probabilities_per_genre.items():
        print(f"{genre}: {prob}")

    return


if __name__ == '__main__':
    main()
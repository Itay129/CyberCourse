import sys


def word_freq_counter(words_file, top_words_amount):
    try:   
        with open(words_file, 'r') as file:
            content = file.read()
        print ("File was read successfuly")

    except FileNotFoundError:
        print (f"File {file} not found.")
        sys.exit(1)

    words = content.split()

    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1


    sorted_words_list = (sorted(word_freq.items(), key = lambda item: item[1], reverse = True))
    sorted_words_list = sorted_words_list[:top_words_amount]


word_freq_counter(r"D:\itay\אקדמיית המתכנתים\CyberCourse\most_frquent_words_in_file.txt", int(sys.argv[1]))    
import sys

def read_file(words_file):
    try:   
        with open(words_file, 'r') as file:
            content = file.read()
        print ("File was read successfuly")

    except FileNotFoundError:
        print (f" File: {words_file} was not found.")
        sys.exit(1)
        
    return content


def count_words (content):
    words = content.lower().split()

    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    return word_freq

def sort_words(word_freq, top_words_amount):
    sorted_words_list = (sorted(word_freq.items(), key = lambda item: item[1], reverse = True))
    sorted_words_list = sorted_words_list[:top_words_amount]
    return sorted_words_list


def print_results(sorted_words_list):
    for word, count in sorted_words_list:
        print (f"{word}  was found {count}  times in the file") 


def main():
    top_words_amount = int(sys.argv[1])
    content = read_file(r"D:\itay\אקדמיית המתכנתים\CyberCourse\most_frquent_words_in_file.txt")
    word_freq = count_words(content)
    sorted_words_list = sort_words(word_freq , top_words_amount)
    print_results(sorted_words_list)
    


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("No input found with sys.argv")
        sys.exit(1)

    main()

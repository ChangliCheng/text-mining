from mediawiki import MediaWiki
import random
import string
import sys
from unicodedata import category
# This block of code get ideas from analyze_book.py we did in the class

wikipedia = MediaWiki()
# Following are different properties in this library

# wikipedia.random(pages=3)
# wikipedia.search('Babson', results=3)
# wikipedia.allpages('Babson', results=10)
# wikipedia.geosearch(latitude=42.361145, longitude=-71.057083)
# wikipedia.opensearch('new york', results=2)
# wikipedia.prefixsearch('ba', results=5)
# babson = wikipedia.page("Babson College")
# babson.title
# babson.content
# babson.pageid
# babson._revision_id
# babson._parent_id
# babson.links
# babson.summarize(chars=200)
# babson.categories
# babson.summary
# babson.backlinks
# babson.coordinates
# babson.links
# babson.logos
# babson.sections
# babson.table_of_contents
# babson.wikitext


def content():
    """return the required content from wikipedia"""
    keyword = input("What do you want to search?>>>")
    desired_page = wikipedia.page(keyword)
    desired_content = desired_page.content
    return desired_content


def frequency():
    """returns: map from each word to the number of times it appears."""
    d = {}
    use_content = content()
    for word in use_content.split():
        word = word.strip()
        word = word.lower()
        d[word] = d.get(word, 0) + 1

    return d


def get_summary_and_categories():
    """return the summary of the search item"""
    word = input("What search item summary you want to get?>>>")
    required_page = wikipedia.page(word)
    print(required_page.summarize(sentences=5))
    return required_page.categories


def total_words(d):
    """Returns the total of the frequencies in a histogram."""
    return sum(d.values())


def different_words(d):
    """Returns the number of different words in a histogram."""
    return len(d)


def process_file(filename):
    """Makes a histogram that contains the words from a file.

    filename: string

    returns: map from each word to the number of times it appears.
    """
    hist = {}
    fp = open(filename, encoding='utf8')

    strippables = ''.join(
        [chr(i) for i in range(sys.maxunicode)
         if category(chr(i)).startswith("P")]
    )

    for line in fp:
        if line.startswith('*** END OF THIS PROJECT'):
            break

        line = line.replace('-', ' ')
        line = line.replace(
            chr(8212), ' '
        )

        for word in line.split():
            word = word.strip(strippables)
            word = word.lower()
            hist[word] = hist.get(word, 0) + 1

    return hist


def most_common(d, excluding_stopwords=True):
    """Makes a list of word-freq pairs(tuples) in descending order of frequency.

    d: map from word to frequency
    excluding_stopwords: a boolean value. If it is True, do not include any stopwords in the list.

    returns: list of (frequency, word) pairs
    """
    t = []

    stopwords = process_file('data/stopwords.txt')

    stopwords = list(stopwords.keys())

    for word, freq in d.items():
        if excluding_stopwords:
            if word in stopwords:
                continue

        t.append((freq, word))

    t.sort(reverse=True)
    return t


def print_most_common(d, num=10):
    """Prints the most commons words in a histgram and their frequencies.
    d: histogram (map from word to frequency)
    num: number of words to print
    """
    t = most_common(d)
    print('The most common words are:')
    for freq, word in t[:num]:
        print(word, '\t', freq)


def subtract(d, d1):
    """Returns a dictionary with all keys that appear in d but not d1.
    d, d1: dictionaries of searched items
    """
    dif = {}
    count = 0
    for key in d:
        if key not in d1 and count < 10:
            dif[key] = None
            count += 1
    return dif


def random_word(d):
    """Chooses a random word from a histogram.

    The probability of each word is proportional to its frequency.
    """
    t = []

    for word, freq in d.items():
        t.extend([word] * freq)

    return random.choice(t)


def get_coordinates():
    """return the coordinates of the input"""
    place = input("Which place's coordinate do you want to get?<<<")
    want_page = wikipedia.page(place)
    return want_page.coordinates


def get_logos():
    """return urls of the logos of the input word"""
    word = input(
        "What search item's logos or signature pictures do you want to get?<<<")
    page = wikipedia.page(word)
    return page.logos


if __name__ == '__main__':
    d = frequency()
    d1 = frequency()
    frequency()
    get_summary_and_categories()
    total_words(d)
    different_words(d)
    most_common(d, excluding_stopwords=True)
    print_most_common(d, num=10)
    subtract(d, d1)
    random_word(d)
    get_coordinates()
    get_logos()

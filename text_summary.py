import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import spacy.displacy as displacy
from string import punctuation
from heapq import nlargest

text = """
Paul William Walker IV[3] (September 12, 1973[4] – November 30, 2013) was an American actor. He is best known for his role as Brian O'Conner in the Fast & Furious franchise.

Walker began his career as a child actor in the 1980s, gaining recognition in the 1990s after appearing in the television soap opera The Young and the Restless; he received praise for his performances in the teen comedy She's All That and the comedy-drama Varsity Blues (both 1999), and saw international fame by starring in The Fast and the Furious (2001).

Walker also starred in the commercially successful road thriller Joy Ride (2001), becoming an action star. He followed this with the box-office disappointments Into the Blue (2005) and Running Scared (2006), although he earned praise for his performance in the survival drama Eight Below, and for his portrayal of Hank Hansen in Flags of Our Fathers (both 2006). Outside of these, Walker largely appeared in low budget action films, but starred in the commercially successful heist film Takers (2010).

Walker died of injuries sustained from a single-vehicle collision on November 30, 2013. His father and daughter filed separate wrongful death lawsuits against Porsche, which resulted in settlements. At the time of his death, Walker had not completed filming Furious 7 (2015); it was released after rewrites and stand-ins, including his brothers Cody and Caleb, filled in for Walker, while the song "See You Again" by Wiz Khalifa and Charlie Puth was commissioned as a tribute.
"""
def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    # print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    document = nlp(rawdocs)
    # print(document)
    tokens = [token.text for token in document]
    # print(tokens)
    word_frequency = {}
    for word in document:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_frequency.keys():
                word_frequency[word.text] = 1
            else:
                word_frequency[word.text] += 1

    # print(word_frequency)

    max_frequency = max(word_frequency.values())
    # print(max_frequency)

    for word in word_frequency.keys():
        word_frequency[word] = word_frequency[word]/max_frequency

    # print(word_frequency)


    sent_tokens = [sent for sent in document.sents]
    # print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_frequency.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_frequency[word.text]
                else:
                    sent_scores[sent] += word_frequency[word.text]
    # print(sent_scores)
    select_len = int(len(sent_tokens) * 0.2)
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(summary)
    # print('Length of original text: ', len(text.split(' ')))
    # print('Length of summarized text: ', len(summary.split(' ')))
    return summary, document, len(rawdocs.split(' ')), len(summary.split(' '))
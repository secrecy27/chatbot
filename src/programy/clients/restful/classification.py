import nltk
# nltk.download("punkt")
from nltk.stem.lancaster import LancasterStemmer
import os


class Naive_bayes():

    def __init__(self):
        self.stemmer = LancasterStemmer()
        self.training_data = []
        self.base_path = "../../../conversation/"

        # 파일 읽어들임
        for filename in os.listdir(self.base_path):
            self.read_data(filename)

        self.corpus_words = {}
        self.class_words = {}
        self.classes = list(set([a['class'] for a in self.training_data]))
        for c in self.classes:
            self.class_words[c] = []
        self.extract_data()

    def read_data(self, filename):
        with open(self.base_path + filename, encoding="utf-8") as f:
            while True:
                line = f.readline().strip()
                if not line: break
                self.training_data.append({"class": filename, "sentence": line})

    def extract_data(self):
        for data in self.training_data:
            # 각 문장을 단어를 토큰화
            for word in nltk.word_tokenize(data['sentence']):
                if word not in ["?", "'s"]:
                    # stem and lowercase each word
                    stemmed_word = self.stemmer.stem(word.lower())

                    # 이미 나온 문자인지 확인
                    if stemmed_word not in self.corpus_words:
                        self.corpus_words[stemmed_word] = 1
                    else:
                        self.corpus_words[stemmed_word] += 1

                    # class list에 단어 추가
                    self.class_words[data['class']].extend([stemmed_word])

    def calculate_class_score_commonality(self, sentence, class_name, show_details=True):
        score = 0
        # 새로운 문장에서 단어를 각각 토큰화
        for word in nltk.word_tokenize(sentence):
            # 단어의 stem이 클래스 중에 속하는 지 여부
            if self.stemmer.stem(word.lower()) in self.class_words[class_name]:
                # 상대적인 가중치를 더함
                score += (1 / self.corpus_words[self.stemmer.stem(word.lower())])

                if show_details:
                    print("   match: %s (%s)" % (
                        self.stemmer.stem(word.lower()), 1 / self.corpus_words[self.stemmer.stem(word.lower())]))
        return score

    def classify(self, sentence):
        high_class = None
        high_score = 0

        for c in self.class_words.keys():
            score = self.calculate_class_score_commonality(sentence, c, show_details=False)

            if score > high_score:
                high_class = c
                high_score = score
        return high_class, high_score

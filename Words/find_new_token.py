from collections import defaultdict, Counter
import numpy as np
import re
from tqdm import tqdm

class FindNewToken:
    def __init__(self, input_path, output_path, min_count=25, token_length=4, min_proba={2:150, 3:450, 4:2100}):
        self.input_path = input_path
        self.output_path = output_path
        self.min_count = min_count
        self.token_length = token_length
        self.min_proba = min_proba

    def read_text(self):
        print("reading text!")
        texts = []
        with open(self.input_path, encoding='utf-8') as f:
            texts = [line for line in f if line not in ['\n']]
        texts = [y for x in texts for y in x]
        self.texts = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）0-9a-zA-Z]+', "", "".join(texts))
        print(self.texts[:200])

    def statistic_ngrams(self):
        print('Starting statistic ngrams!')
        ngrams = defaultdict(int)
        for char_id in range(len(self.texts)):
            for step in range(1, self.token_length+1):
                if char_id+step <= len(self.texts):
                    ngrams[self.texts[char_id:char_id+step]] += 1
        self.ngrams = {k: v for k, v in ngrams.items() if v >= self.min_count}
        self.total = sum([v for k, v in self.ngrams.items() if len(k) == 1])
        print("ngrams:", self.ngrams)
        print("total:", self.total)
        return self.ngrams

    def calculate_prob(self, token):
        """
        计算凝固度
        :param token: word
        :return:
        """
        if len(token) >= 2:
            score = min([self.total*self.ngrams[token]/(self.ngrams[token[:i+1]]*self.ngrams[token[i+1:]]) for i in range(len(token)-1)])
            if score > self.min_proba[len(token)]:
               return True
        else:
            return False

    def filter_ngrams(self):
        """
        储存凝固度合格的词语
        :return:
        """
        self.ngrams = set(token for token in self.ngrams if self.calculate_prob(token))

    def write(self, final_words):
        with open(output_path, 'w', encoding='utf-8') as f:
            [f.write(token + '\n') for token in final_words]

    def calculate_entropy(self, char_list):
        """
        计算左右熵
        :param char_list:
        :return:
        """
        char_freq_dic = dict(Counter(char_list))
        entropy = (-1)*sum([char_freq_dic.get(i)/len(char_list)*np.log2(char_freq_dic.get(i)/len(char_list))for i in char_freq_dic])
        return entropy

    def Entropy_left_right_filter(self, min_entropy):
        """
        根据左右熵筛选新词
        :param min_entropy:
        """
        print("Starting entropy filter!")
        final_words = []
        pbar = tqdm(total=len(self.ngrams))
        for word in self.ngrams:
            try:
                left_right_char = re.findall('(.)%s(.)'%word, self.texts)
                left_char = [i[0] for i in left_right_char]
                left_entropy = self.calculate_entropy(left_char)
                right_char = [i[1] for i in left_right_char]
                right_entropy = self.calculate_entropy(right_char)
                if min(right_entropy, left_entropy) > min_entropy:
                    final_words.append(word)
                pbar.update(1)
            except:
                pass
        return final_words


if __name__ == '__main__':
    input_path = 'Data/n_wzdmd_crawl.txt'
    output_path = 'Data/user_dict.txt'
    findtoken = FindNewToken(input_path, output_path)
    findtoken.read_text()
    ngrams = findtoken.statistic_ngrams()
    findtoken.filter_ngrams()
    final_words = findtoken.Entropy_left_right_filter(1)
    findtoken.write(final_words)
    # two_grams = ['撕逼', '开开', '大王', '小王', '千千', '纸鸟', '水产', '可爱', '王源']
    # two_proba = sum([findtoken.calculate_prob(w, ngrams) for w in two_grams]) / len(two_grams)
    # three_grams = ['文明旅', '恩负义', '业院校']
    # three_proba = sum([findtoken.calculate_prob(w, ngrams) for w in three_grams]) / len(three_grams)
    # four_grams = ['真情实感', '鹬蚌相争', '渔翁得利', '易烊千玺']
    # four_proba = sum([findtoken.calculate_prob(w, ngrams) for w in four_grams]) / len(four_grams)
    # print("two_proba", two_proba)
    # print("three_proba", three_proba)
    # print("four_proba", four_proba)



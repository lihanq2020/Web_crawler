import jieba
import codecs
jieba.load_userdict('data/user_dict.txt')
with open('data/test.txt', 'r') as f:
    for line in f:
        seg = jieba.cut(line.strip(), cut_all=False)
        s = '/'.join(seg)
        m = list(s)
        with open('data/output.txt', 'a+') as f:
            for word in m:
                f.write(word)

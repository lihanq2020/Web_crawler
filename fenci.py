import jieba
import codecs
jieba.load_userdict('Data/user_dict.txt')
with open('Data/wangzhademadai.txt', 'r') as f:
    for line in f:
        seg = jieba.cut(line.strip(), cut_all=False)
        s = ' '.join(seg)
        m = list(s)
        with open('Data/output.txt', 'a+') as o:
            for word in m:
                if word in ['\n', '。', '!', '?', '~', '～', '！', '？']:
                    o.write('\n')
                else:
                    o.write(word)
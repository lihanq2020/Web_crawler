import jieba
import codecs
jieba.load_userdict('Data/user_dict.txt')
with open('Data/n_wzdmd_crawl.txt', 'r') as f:
    for line in f:
        seg = jieba.cut(line.strip(), cut_all=False)
        s = ' '.join(seg)
        m = list(s)
        if len(m) > 1:
            with open('Data/n_output.txt', 'a+') as o:
                for word in m:
                    o.write(word)
                o.write('\n')
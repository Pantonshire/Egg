import csv


vowels = 'a e i o u'.split()



def load_names(from_file):
    with open(from_file, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        names = [ row[1].replace('"', '') for row in reader ]
    return names


def search(names, needles):
    counter = 0
    no_names = len(names)
    results = []
    for name in names:
        for needle in needles:
            match = best_match(name.lower(), needle)
            new_name = match[0]
            score = match[1]
            if new_name is not None and score > 0 and score < 1:
                results.append((name, new_name, score))
        counter += 1
        if counter % 10000 == 0:
            print(str(counter) + '/' + str(no_names))
    return sorted(results, key=lambda x: x[2], reverse=True)


def best_match(haystack, needle):
    h_len = len(haystack)
    n_len = len(needle)
    if n_len > h_len:
        return None, 0
    best_index = -1
    best_score = 0
    best_match = None
    for i in range(h_len - n_len + 1):
        slice = haystack[i:i+n_len]
        this_score = score(slice, needle)
        if this_score > best_score:
            best_score = this_score
            best_index = i
            best_match = slice
    if best_index == -1:
        return None, 0
    sub = needle
    best_match_end = best_match[-1:]
    if vowel(best_match_end) and not vowel(sub[-1:]):
        sub += best_match_end
    return capitalise(haystack[0:best_index] + sub + haystack[best_index+n_len:h_len]), (best_score / n_len)


def score(a, b):
    score = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            score += 1
    return score


def vowel(x):
    return x in vowels


def capitalise(s):
    return s[0].upper() + s[1:]

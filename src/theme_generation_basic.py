import re
from collections import Counter
from preprocessing import load_json

'''Since it is impossible automatically generate themes using Regular Expressions(RE), keywords will be manually selected'''

themes = {'finance':  re.compile(r"\b(rent|loan|debt|money|bills?|salary|wages?|paycheck|finance|expensive|cheap|broke|sales?|discount)\b", re.IGNORECASE),
          'relationships': re.compile(r"\b(girlfriend|boyfriend|husband|wife|partner|spouse|fiance|relationship|dating|ex|cheat(ed)?|valentine)\b", re.IGNORECASE),
          'family': re.compile(r"\b(mother|father|mom|dad|parents?|sister|brother|siblings?|child|son|daughter|in[- ]?laws?|grandparents?)\b", re.IGNORECASE),
          'friendship': re.compile(r"\b(friend|bestie|bff|buddy|pal|roommate|flatmate|neighbor)\b", re.IGNORECASE),
          'work': re.compile(r"\b(boss|coworker|colleague|manager|office|job|promotion|workplace|company|employment|employee|employer)\b", re.IGNORECASE),
          'societal norms': re.compile(r"\b(right|wrong|selfish|respect|rude|entitled|ethical|manners|justice|unfair|fair)\b", re.IGNORECASE),
          'education': re.compile(r"\b(school|college|university|classmate|professor|teacher|exam|homework|study|student)\b", re.IGNORECASE),
          #'emotions': re.compile(r"\b(angry|furious|mad|rage|yell(ed)?|scream(ed)?|argument|fight|rude|disrespect(ed)?)\b", re.IGNORECASE),
          }

corpus = "./data/output.json"

def generate_themes(regex_themes, chunk_size=1000):
    data = load_json(corpus)
    theme_counts = Counter()
    batch_counter = Counter()

    for i, line in enumerate(data, 1):
        for theme, pattern in regex_themes.items():
            if pattern.search(line):
                theme_counts[theme] += 1

        if i % chunk_size == 0:
            theme_counts.update(batch_counter)
            batch_counter.clear() # This line resets the counter so that it can process the next 1000 lines

    if batch_counter: # Remaining lines
        theme_counts.update(batch_counter)

    return theme_counts

if __name__ == "__main__":
    print(generate_themes(themes))

''' This is the result:
Counter({'societal norms': 61539, 'family': 52716, 'emotions': 47869, 'relationships': 47192, 'finance': 37687, 'friendship': 37528, 'work': 34511, 'education': 31495})
'''
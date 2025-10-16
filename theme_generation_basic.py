import re
from collections import Counter

'''Since it is impossible automatically generate themes using Regular Expressions(RE), keywords will be manually selected'''

themes = {'finance':  re.compile(r"\b(rent|loan|debt|money|bills?|salary|wages?|paycheck|finance|expensive|cheap|broke|sales?|discount)\b", re.IGNORECASE),
          'relationships': re.compile(r"\b(girlfriend|boyfriend|husband|wife|partner|spouse|fiance|relationship|dating|ex|cheat(ed)?|valentine)\b", re.IGNORECASE),
          'family': re.compile(r"\b(mother|father|mom|dad|parents?|sister|brother|siblings?|child|son|daughter|in[- ]?laws?|grandparents?)\b", re.IGNORECASE),
          'friendship': re.compile(r"\b(friend|bestie|bff|buddy|pal|roommate|flatmate|neighbor)\b", re.IGNORECASE),
          'work': re.compile(r"\b(boss|coworker|colleague|manager|office|job|promotion|workplace|company|employment|employee|employer)\b", re.IGNORECASE),
          'societal norms': re.compile(r"\b(right|wrong|selfish|respect|rude|entitled|ethical|manners|justice|unfair|fair)\b", re.IGNORECASE),
          'education': re.compile(r"\b(school|college|university|classmate|professor|teacher|exam|homework|study|student)\b", re.IGNORECASE),
          'emotions': re.compile(r"\b(angry|furious|mad|rage|yelled?|screamed?|argument|fight|rude|disrespect)\b", re.IGNORECASE),
          }

def generate_themes(file_path, regex_themes):

    theme_counts = Counter()

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            for theme, pattern in regex_themes.items():
                if pattern.search(line):
                    theme_counts[theme] += 1

    return theme_counts

# print(generate_themes('./data/amitheasshole_comments_preprocessed.txt', themes))

comments =  "My girlfriend said I was rude for not paying rent. GIRLFRIEND My boss yelled at me at work today. My parents think I should apologize. My coworker didn’t invite me to lunch."


print(generate_themes(comments, themes))
''' Counter({'family': 511163, 'relationships': 306116, 'societal norms': 226386, 'friendship': 120553, 'finance': 118324, 'emotions': 70621, 'work': 70560, 'education': 59018}) '''
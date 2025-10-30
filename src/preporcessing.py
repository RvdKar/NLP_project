import json
from collections import defaultdict

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data


def load_reddit_data(comments_directory, submissions_directory):
    with open(comments_directory, 'r', encoding='utf-8') as file:
        comment_id_pairs = []
        for i, line in enumerate(file, 1):
            try:
                # if i >= 500000:
                #     break
                data = json.loads(line)
                body = data.get('body', '').strip() # Comment text
                link_id = data.get('link_id', '').strip() # Link id
                id = data.get('name', '').strip() # Specific id
                comment_id_pairs.append((body, link_id))
            except json.JSONDecodeError:
                continue  # This is done to avoid missing comments or bad lines
        comment_id_pairs = tuple(comment_id_pairs)
        comments_dict = {id_: text for text, id_ in comment_id_pairs}
        comments_dict = {id_: text for id_, text in comments_dict.items() if text not in ("[deleted]", "[removed]")} # To remove deleted or removed comments
        #print(comments_dict)

    with open(submissions_directory, 'r', encoding='utf-8') as file:
        text_id_pairs = []
        for i, line in enumerate(file, 1):
            try:
                # if i >= 500000:
                #     break
                data = json.loads(line)
                title = data.get('title', '').strip() # Submission title
                body = data.get('selftext', '').strip() # Submission text
                id = data.get('name', '').strip() # Specific id
                text_id_pairs.append((title, body, id))
            except json.JSONDecodeError:
                continue # This is done to avoid missing comments or bad lines
        submissions_dict = {id_: (title + " " + body).strip() for title, body, id_ in text_id_pairs}
        submissions_dict = {id_: text for id_, text in submissions_dict.items() if text not in ("[deleted]", "[removed]")}
        #print(submissions_dict)

    grouped = defaultdict(list)
    res = []
    for comment, id_ in comment_id_pairs:
        if id_ in submissions_dict:
            grouped[id_].append(comment)

    banned_phrases = [
        "^^^^automod",
        "welcome to /r/amitheasshole.",
        "your post has been removed",
        "#read this carefully",
        "[removed]",
        "[deleted]"
        ]

    for id_, comments in grouped.items():
        # This removes the copy of each submission because, each submission has an automated comment that starts with the string that is present in the code.
        clean_comments = [c for c in comments  if len(c.strip()) > 0 and not any(phrase in c.lower() for phrase in banned_phrases)] 
        # The following statement is to avoid appending the list with submissions that have no comments at all
        if not clean_comments:
            continue
        combined = submissions_dict[id_] + ' [======>] ' + " ".join(clean_comments)
        res.append(combined)

    res = [post for post in res if not any(p in post.lower() for p in banned_phrases)] # Copy of line clean_comments to ensure the data is filtered completely
    #print(res[4])

    with open("./data/output.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    comments_dir = './data/amitheasshole_comments.ndjson'
    submissions_dir = './data/amitheasshole_submissions.ndjson'
    reddit_data = load_reddit_data(comments_dir, submissions_dir)
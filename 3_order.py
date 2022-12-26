with open('ratings.csv', 'r') as f:
    ratings = f.readlines()


def rating_key(rating_str):
    elements = rating_str.rsplit(',')
    return elements[-2]


sorted_ratings = sorted(ratings, key=rating_key, reverse=True)

with open('sorted_ratings.csv', 'w') as f:
    f.writelines(sorted_ratings)

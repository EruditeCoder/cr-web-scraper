# Open the ratings.csv file and read its contents into a list of strings
with open('ratings.csv', 'r') as f:
    ratings = f.readlines()


# Sort the list of strings by the second element (the rating) using the sorted() function
# and a custom key function
def rating_key(rating_str):
    # Split the string on the comma to get a list of elements
    elements = rating_str.rsplit(',')
    # Return the second element (the rating) as the key
    return elements[-2]


sorted_ratings = sorted(ratings, key=rating_key, reverse=True)

# Open a new file called sorted_ratings.csv and write the sorted list of strings to this file
with open('sorted_ratings.csv', 'w') as f:
    f.writelines(sorted_ratings)

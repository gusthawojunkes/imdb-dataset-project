import csv
import os

ratings_tsv = open("ratings.tsv","r",encoding='utf-8')
titles_tsv = open("titles.tsv","r",encoding='utf-8')
ratings = csv.reader(ratings_tsv, delimiter="\t")
titles = csv.reader(titles_tsv, delimiter="\t")

IMDB_DATA = dict()
not_found = []

print("Loading IMDB data...")
for title in titles:
    if title and len(title) > 0:
        dictionary = {}
        dictionary['id'] = title[0]
        if len(title) > 1:
            dictionary['titleType'] = title[1]
        if len(title) > 2:
            dictionary['primaryTitle'] = title[2]
        if len(title) > 3:
            dictionary['originalTitle'] = title[3]
        if len(title) > 4:
            dictionary['isAdult'] = title[4]
        if len(title) > 5:
            dictionary['startYear'] = title[5]
        if len(title) > 6:
            dictionary['endYear'] = title[6]
        if len(title) > 7:
            dictionary['runtimeMinutes'] = title[7]
        if len(title) > 8:
            dictionary['genres'] = title[8]

        IMDB_DATA[title[0]] = dictionary


for rating in ratings:
    if rating and len(rating) > 0:
        id = rating[0]
        try:
            if len(rating) > 1:
                ratingValue = rating[1]
                IMDB_DATA[id]['ratingValue'] = ratingValue
            if len(rating) > 2:
                numVotes = rating[2]
                IMDB_DATA[id]['numVotes'] = numVotes
        except KeyError:
            not_found.append(id)

total = len(IMDB_DATA)
print("Total of movies loaded: " + str(total))

with_errors = len(not_found)
percentage_with_errors = (with_errors / total) * 100
print("Total of movies not found: " + str(with_errors) + " (" + str(percentage_with_errors) + " of total)")

try: os.remove("data.csv")
except: pass
    
csvTitles = open('data.csv','w',newline='',encoding='utf-8')
writeFile = csv.writer(csvTitles,delimiter=';')

values = IMDB_DATA.values()

count = 0

for dictionary in values:
    row = []
    try:
        type = dictionary['titleType']
        if type == 'movie':
            if count > 0 and dictionary['startYear'] != '\\N':
                year = int(dictionary['startYear'])
                if year >= 2000 and year <= 2020:
                    for property in dictionary:
                        data = dictionary[property]
                        if data and data != []:
                            row.append(data)
            else:
                for property in dictionary:
                    data = dictionary[property]
                    if data:
                        row.append(data)
    except:
        pass

    if len(row) > 0:
        writeFile.writerow(row)
        count += 1

print("Total of movies written: " + str(count) + "\n")
    
csvTitles.close()
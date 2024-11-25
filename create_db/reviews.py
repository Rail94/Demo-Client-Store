import json
with open('reviews.json', 'r') as f:
	reviews = json.load(f)

	for row in reviews:
		if row['star_rating'] > 3:
			#print(row)
			print(row['reviewer'], row['date_reviewed'], row['star_rating'],row['message'])
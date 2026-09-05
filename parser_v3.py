import requests
import time
import json
import os
url_twogis = "https://public-api.reviews.2gis.com/3.0/branches/70000001056730848/reviews?limit=50&offset=0&is_advertiser=false&fields=meta.providers,meta.branch_rating,meta.branch_reviews_count,meta.total_count,reviews.hiding_reason,reviews.emojis,reviews.trust_factors&rated=true&sort_by=trust&key=6e7e1929-4ea9-4a5d-8c05-d601860389bd&locale=ru_RU"

url_yandex = "https://yandex.ru/maps/api/business/fetchReviews?ajax=1&businessId=41867541882&csrfToken=efdc30abb7ad58759de6962e19d5f84321a5b86d%3A1788594635&locale=ru_RU&page=1&pageSize=50&ranking=by_relevance_org&reqId=1788594635192059-1231116757-addrs-upper-yp-22&s=759499643&sessionId=1788594635146516-7338186996850161903-balancer-l7leveler-kubr-yp-vla-88-BAL"

old_data = requests.get(url_twogis).json()
old_count = len(old_data["reviews"])
review = old_data["reviews"]
old_dict = {}
for i in review:
    old_dict[i["id"]] = {
        "name": i["user"]["name"],
        "text": i["text"],
        "rating": i["rating"]
    }

while True:
    new_data = requests.get(url_twogis).json()
    if len(new_data["reviews"]) == old_count:
        print("Data not upload")
        time.sleep(100)
    else:
        print("Data upload")
        new_dict = {}
        for i in new_data["reviews"]:
            new_dict[i["id"]] = {
                "name": i["user"]["name"],
                "text": i["text"],
                "rating": i["rating"]
            }
        detect_id = new_dict.keys() - old_dict.keys()
        reviews_for_post = []
        for i in detect_id:
            reviews_for_post.append(new_dict[i])
        with open('data_temp.json', 'w', encoding='utf-8') as f:
            json.dump(reviews_for_post , f, ensure_ascii=False, indent=4)
        f.close()
        os.replace("data_temp.json", "data.json")
        old_count = new_data["meta"]["branch_reviews_count"]
        old_data = new_data
        old_dict = new_dict
        time.sleep(100)
        
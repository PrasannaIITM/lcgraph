from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import Form
import json
import requests

def new(request):
    form = Form(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        query = {"operationName":"getContestRankingData","variables":{"username":username},"query":"query getContestRankingData($username: String!) {\n  userContestRanking(username: $username) {\n    attendedContestsCount\n    rating\n    globalRanking\n    __typename\n  }\n  userContestRankingHistory(username: $username) {\n    contest {\n      title\n      startTime\n      __typename\n    }\n    rating\n    ranking\n    __typename\n  }\n}\n"}
        headers = {
            'authority': 'leetcode.com',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'accept': '*/*',
            'x-newrelic-id': 'UAQDVFVRGwEAXVlbBAg=',
            'x-csrftoken': 'BvBM29lAlYBCZwOLiwLZrpWIcmfNnefxoNvGwL2NvASAyrJUlEBehFON8EueWqkC',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'content-type': 'application/json',
            'origin': 'https://leetcode.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://leetcode.com/'+username+'/',
            'accept-language': 'en-GB,en;q=0.9',
            'cookie': '__cfduid=d52b66c03d3581445d2dbd00222b7b9371620126831; csrftoken=BvBM29lAlYBCZwOLiwLZrpWIcmfNnefxoNvGwL2NvASAyrJUlEBehFON8EueWqkC; __cf_bm=56e236acabfadf57a81f0d1ac0d559abee230797-1620126831-1800-ASXX3TrJn7iUZoZ1aQGGaxX24MoCCAH16a94qxUmk7cm09kYU85eSwB2Ih97o5Kv1yxCm3eXV3w4SxBMU7t0dZM=; _ga=GA1.2.215630670.1620126833; _gid=GA1.2.1094012222.1620126833; _gat=1',
        }

        url = 'https://leetcode.com/graphql'
        
        response = requests.post(url, json=query, headers=headers)
        if response.text != """{"errors":[{"message":"User matching query does not exist.","locations":[{"line":2,"column":3}],"path":["userContestRanking"]},{"message":"User matching query does not exist.","locations":[{"line":8,"column":3}],"path":["userContestRankingHistory"]}],"data":{"userContestRanking":null,"userContestRankingHistory":null}}""":
            labels = []
            data = []
            ranking = []
            links = []
            response = response.json()
            for item in response["data"]["userContestRankingHistory"]:
                labels.append(item["contest"]["title"])
                data.append(int(item["rating"]))
                ranking.append(int(item["ranking"]))
                currlink = "https://leetcode.com/contest/"+"-".join(item["contest"]["title"].split()).lower()+"/ranking"
                links.append(currlink)
            print(data, labels,links)
            return render(request, "chart.html", {"response":response, "data":json.dumps(data), "labels":json.dumps(labels), "username":username, "ranking":ranking, "links":json.dumps(links)})
        else:
            return HttpResponse('<h1>Username incorrect</h1>')

    return render(request, "forms.html", {"form":form})

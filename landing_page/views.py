from newsapi import NewsApiClient
import datetime
from django.shortcuts import render
def landing_index(request):
    API_KEY = "e10089beab6045d8aa9c685a108ee279"   # 🔑 replace with your valid key

    newsapi = NewsApiClient(api_key=API_KEY)

    today = datetime.date.today()
    one_week_ago = today - datetime.timedelta(days=7)

    all_articles = newsapi.get_everything(
        q="stocks",
        from_param=one_week_ago.strftime("%Y-%m-%d"),
        to=today.strftime("%Y-%m-%d"),
        language="en",
        sort_by="relevancy",
        page=1
    )

    articles = all_articles.get("articles", [])[:10]
    
    return render(request, "landing_page/landing_page_1.html", {"articles": articles})

def about(request):
    return render(request,"landing_page/about.html")

def login(request):
    return render(request,"landing_page/login.html")

def sign_in(request):
    return render(request,"landing_page/sign_in.html")
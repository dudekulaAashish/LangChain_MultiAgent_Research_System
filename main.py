from src.tools.tools import web_search,scrape_url

results = scrape_url.invoke({"url": "https://www.reddit.com/r/artificial/"})

print(results)

# r = web_search.invoke("what is the latest research on using AI for climate change mitigation?")

# print(r)

import requests
import random
import sys

visited = []
def wikilinks(term, depth, lastpages):
    results = []
    apilink = f'https://he.wikipedia.org/w/api.php?action=query&format=json&titles={term}&prop=links&pllimit=max'
    res = requests.get(apilink).json()
    pageid, pagedata = list(res["query"]["pages"].items())[0]
    pagetitle = pagedata["title"]
    print(pageid + " - " + pagetitle)
    # Check if link is missing page or model page
    if pageid == "-1" or pagetitle[0:6] == "תבנית:": 
        return "Same"
    # Check if link was already visited and add to visited list
    if pageid in lastpages:
        visited.append(1)
        return "Same"
    lastpages.append(pageid)
    links = pagedata["links"]
    for i in links:
        results.append(i["title"])
    if depth > 0:
        if len(results) > 0:
            newterm = results[random.randrange(0,len(results))]
            nextpage = wikilinks(newterm,depth-1,lastpages)
            if not isinstance(nextpage,list):
                print("Some error - skipping")
            # If some got some error (missing page or whatever) try again until no error
            while nextpage == "Same":
                nextpage = wikilinks(results[random.randrange(0,len(results))],depth-1,lastpages)
            results.extend(nextpage)
    return results
        

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Enter term:")
        term = input()
    else:
        term = " ".join(sys.argv[1:])
    link_list = wikilinks(term,3,[])
    print(f'Got {len(link_list)} total links')
    print (f'Got {len(set(link_list))} unique links')
    print(f'Tried to revisit a link {len(visited)} times')
import requests
import random
import sys

test = []
def wikilinks(term, depth, lastpages):
    results = []
    apilink = f'https://he.wikipedia.org/w/api.php?action=query&format=json&titles={term}&prop=links&pllimit=max'
    res = requests.get(apilink).json()
    pageid = list(res["query"]["pages"].keys())[0]
    pagetitle = res["query"]["pages"][pageid]["title"]
    print(pageid + " - " + pagetitle)
    if pageid in lastpages or pagetitle[0:6] == "תבנית:":
        return "Same"
    if pageid == "-1":
        test.append(1)
        return "Same"
    lastpages.append(pageid)
    links = res["query"]["pages"][pageid]["links"]
    for i in links:
        results.append(i["title"])
    if depth > 0:
        if len(results) > 0:
            newterm = results[random.randrange(0,len(results))]
            print(f'New term: {newterm}') 
            nextpage = wikilinks(newterm,depth-1,lastpages)
            if not isinstance(nextpage,list):
                print(nextpage)
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
    print(f"Tried to revisit a link {len(test)} times")
import json
import sys

import requests

QueryURL = "https://demo.kvasira.com/api/library/"
LibraryURL = "https://demo.kvasira.com/api/libraries"
#headers = {'content-type': 'application/json'}
LibraryList = {}
SearchResult = {}


def main(argv):
    # welcome message.

    print("Welcome to Kvasir Example API CLI Tool.\n \
    This Tool allows you to search Kvasir using a script.\n")
    menu()


def menu():

    while(True):
        myInput = input(
            "\n---MENU--- Press: \n1. To list Search Libraries.\n2. To Search a Library\n3. To Show Previous Results\n0. To Exit.\n\nMy Selection: ")

        if (myInput == "1"):
            print("You pressed One!\nListing Libraries....")
            ListLibraries()
            pass
        elif (myInput == "2"):
            print("You Pressed Two!\nStarting Text Search....")
            # ListLibraries() -- consiidering if I should list on search.
            # added a Zero Option to re-list libraries.
            searchLibraries()
        elif (myInput == "3"):
            print("You pressed Three! --- Reprinting Previous Results\n")
            if SearchResult:
                counter = 1
                for n in SearchResult:
                    i = SearchResult[int(counter)]
                    print(str(counter)+". Title: " +
                          i['title']+"\nSummary: "+i['summary']+"\nURI: "+i['uri']+"\n")
                    counter += 1
            else:
                print("\n------ ERROR No Available Results ------\n")
            pass

        elif (myInput == "0"):
            print("You pressed Zero! closing app\n\n      GoodBye! :)\n")
            break
        else:
            print("You Pressed A Wrong button!!\nPlease Try Again.")
            pass


def searchFunction(searchString, libraryDict, numOfResults, textOrUrl,):

    print("Search function......\n")

    # https://demo.kvasira.com/api/library/LIBRARY_ID/query?query_type=[url|text]&k=N,
    SearchQueryURL = QueryURL + \
        libraryDict['id']+"/query?query_type=" + \
        str(textOrUrl)+"&k="+str(numOfResults)
    # print(SearchQueryURL)
    # print(searchString)
    myPayload = {'doc': searchString}
    # print(myPayload)
    KvasirQuery = requests.post(
        SearchQueryURL, data=myPayload)  # headers=headers,
    # print(KvasirQuery)
    if KvasirQuery.status_code == 200:
        # result = json.loads(KvasirQuery.content.decode('utf-8'))
        result = json.loads(KvasirQuery.text)
     #  print(result)
     #  print(result.keys())
        counter = 0
        for i in result['response']['results']:
            # Storing output to dict.
            counter += 1
            print(str(counter)+". Title: " +
                  i['title']+"\nSummary: "+i['summary']+"\nURI: "+i['uri']+"\n")
            SearchResult[counter] = i

    else:
        print("Error of some kind")

    pass


def ListLibraries():
    print("\n\n ----- LIBRARY LIST -----\n\n")
    # requests.Response()

    searchRequest = requests.get(LibraryURL)

    if searchRequest.status_code == 200:
        # result = json.loads(searchRequest.content.decode('utf-8'))
        result = json.loads(searchRequest.text)
        number = 0
        for i in result['data']:
            # Storing output to dict.
            number += 1
            LibraryList[number] = i
            print(str(number)+". Title: " +
                  i['title']+"\nDescription: "+i['description'])

    # for i in result:
    #     print(i, result[i])
    pass


def searchLibraries():
    LibrarySelection = input(
        "Which Library Would you like to search? (0. To list libraries.) ")
    # if int in Library List
    if(int(LibrarySelection) in LibraryList):
        while True:
            textOrUrl = input(
                "Would you like to search for text, file or URL? ")
            if(textOrUrl.lower() == "text" or textOrUrl.lower() == "url" or textOrUrl.lower() == "file"):
                break

            else:
                print("invalid option, please try again.")
        if(textOrUrl.lower() == "text"):
            searchString = input("What would you like to search for? ")
        elif(textOrUrl.lower() == "file"):
            filename = input("What is the location of the file? ")
            f = open(filename, "r")
            if f.mode == 'r':
                searchString = f.read()
                textOrUrl = "text"
                f.close()
        else:
            searchString = input("Please enter a search URL: ")
        while True:
            try:
                numResults = int(
                    input('How Many Results would you like? '))
                break
            except:
                print("That's not a valid number!")
        searchFunction(
            searchString, LibraryList[int(LibrarySelection)], numResults, textOrUrl)
    elif(LibrarySelection == "0"):
        ListLibraries()
        pass
    else:
        print(
            "Sorry, Library Not Found, Please try again\n**HINT: YOU MUST list libraries first to populate the list**")
        pass


if __name__ == "__main__":
    main(sys.argv)

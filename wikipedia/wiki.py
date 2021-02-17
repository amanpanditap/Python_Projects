#Installation : pip install wikipedia
#Read the docs here : https://wikipedia.readthedocs.io/en/latest/code.html#api
#Note: Do not save this file as 'wikipedia.py'
import wikipedia

# Do a Wikipedia search for query.
# results - the maxmimum number of results returned
# suggestion - if True, return results and suggestion (if any) in a tuple
print('\nSearch : ',wikipedia.search("Coronavirus"))
print('\nCustomized Search : ',wikipedia.search("Coronavirus", results = 5, suggestion = True))

#Get a Wikipedia search suggestion for query. Returns a string or None if no suggestion was found.
print('\nSuggested Search : ',wikipedia.suggest('Coronavir'))

#Plain text summary of the page.
print('\nSummary : ',wikipedia.summary("Coronavirus"))                   #wikipedia.summary(query, sentences=0, chars=0, auto_suggest=True, redirect=True)
# sentences - if set, return the first sentences sentences (can be no greater than 10).
# chars - if set, return only the first chars characters (actual text returned may be slightly longer).
# auto_suggest - let Wikipedia find a valid page title for the query
# redirect - allow redirection without raising RedirectError
# Note: But watch out - wikipedia.summary will raise a DisambiguationError if the page is a disambiguation page, or a PageError if the page doesn’t exist (although by default, it tries to find the page you meant with suggest and search.):
#For example, the word “bass” can represent a fish or beats or many more. At that time the summary method throws an error as shown below.

wikipedia.set_lang("en")
#Change the language of the API being requested. Set prefix to one of the two letter prefixes found on the list of all Wikipedias.
#Note: Make sure you search for page titles in the language that you have set.

print('\nLanguages Supported : \n',wikipedia.languages())
#List all the currently supported language prefixes (usually ISO language code).
#Returns: dict of <prefix>: <local_lang_name> pairs. To get just a list of prefixes, use wikipedia.languages().keys().

#Get a WikipediaPage object for the page with title title or the pageid pageid (mutually exclusive).
covid = wikipedia.page("Coronavirus")              #wikipedia.page(title=None, pageid=None, auto_suggest=True, redirect=True, preload=False)
# title - the title of the page to load
# pageid - the numeric pageid of the page to load
# auto_suggest - let Wikipedia find a valid page title for the query
# redirect - allow redirection without raising RedirectError
# preload - load content, summary, images, references, and links during initialization

section_title = ''              #enter your section title for page here.

print('\nTitle : ',covid.title)
print('\nURL : ',covid.url)
print('\nList of categories of page : ',covid.categories)
print('\nSections : ',covid.sections)           #List of section titles from the table of contents on the page.
print('\nSection : ',covid.section(section_title))       #Get the plain text content of a section from self.sections. Returns None if section_title isn’t found, otherwise returns a whitespace stripped string.
#Warning!!! Calling section on a section that has subheadings will NOT return the full text of all of the subsections. It only gets the text between section_title and the next subheading, which is often empty.

print('Get Full HTML Page : ',covid.html)      #Warning!!! This can get pretty slow on long pages.
print('\nContent : \n',covid.content)
print('\nImages : \n',covid.images)           #List of URLs of images on the page.
print('\nLinks : \n',covid.links)             #List of titles of Wikipedia page links on a page.
print('\nReferences : \n',covid.references)
print('\nRevision_Id : ',covid.revision_id)        #The revision ID is a number that uniquely identifies the current version of the page.
print('\nParent_Id : ',covid.parent_id)         #Revision ID of the parent version of the current revision of this page

print('\nRandom Article : ',wikipedia.random(pages=1))     #Get a list of random Wikipedia article titles.
#pages - the number of random pages returned (max of 10)
#Note : Random only gets articles from namespace 0, meaning no Category, User talk, or other meta-Wikipedia pages.

wikipedia.donate()       #Open up the Wikimedia donate page in your favorite browser.

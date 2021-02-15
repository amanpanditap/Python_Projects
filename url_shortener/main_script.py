import url_shortener

#Testing the program for the first URL
url1 = "https://www.moneycontrol.com/news/india/coronavirus-india-news-today-live-updates-covid-19-cases-india-today-maharashtra-mumbai-gujarat-tamilnadu-nirmala-sitharaman-press-conference-5269421.html"
url_short = url_shortener.make_shorten(url1)
print('Test1 : ',url_short)

#Testing the program for the second URL
url2 = "https://analyticsindiamag.com/10-leading-courses-training-programmes-for-cloud-computing-in-india-2019/"
url_short2 = url_shortener.make_shorten(url2)
print('Test2 : ',url_short2)

#Opening the file that contains URLs
file = open('url_file.txt', 'r')

#Reading all the URLs line-by-line
lines = file.readlines()

#Opening the file in which we will write the shortened URLS
file2 = open(r"url_file_shortened.txt","w+")

#Shortening each URL, printing n console and writing them in a text file
print('\nShortened URL for links from file:\n')
for url in lines:
    url_short = url_shortener.make_shorten(url.strip('\n'))
    print(url_short)
    file2.write(url_short)
    file2.write("\n")

#Closing bothe the files
file.close()
file2.close()

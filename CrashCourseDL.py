import requests
import bs4
import urllib.request
import os
#Change site for which set to DL
home_res = requests.get('https://thecrashcourse.tumblr.com/downloads')
home_soup = bs4.BeautifulSoup(home_res.text,"lxml") #convert to soup
all_courses = home_soup.select('.article-content p a')

link_start = 'http://thecrashcourse.tumblr.com/downloads/'
root_dl_loc = 'C://Users//rsgn6//Downloads//Crash Course//'
#courses I want via link endings as dictionary keys for a title
to_get = {'biology':'Crash Course - Biology', \
          'chemistry':'Crash Course - Chemistry', \
          'economics':'Crash Course - Economics',\
          'engineering': 'Crash Course - Engineering',\
          'busent': 'Crash Course - Entrepreneurship',\
          'euro': 'Crash Course - European History',\
          'ochem': 'Crash Course - Organic Chemistry',\
          'compsci': 'Crash Course - Computer Science',\
          'physics': 'Crash Course - Physics',\
          'psychology' : 'Crash Course - Psychology',\
          'stats' : 'Crash Course - Statistics',\
          'worldhistory' : 'Crash Course - World History',\
          'worldhistory2' : 'Crash Course - World History 2'}
for course in all_courses:
    course_link_name = course['href'].split(link_start)[-1] #split returns an array; -1 means last to get link ending
    if course_link_name in to_get.keys():
        folder_to_save_in = root_dl_loc + to_get[course_link_name]
        os.mkdir(folder_to_save_in) #make folder for course
        print(f'Created: {folder_to_save_in}')
        res = requests.get(link_start + course_link_name)
        soup = bs4.BeautifulSoup(res.text,"lxml")
        link_to_dl = soup.select('div ol li a') #list of <a href>
        episode_count = 1
        for links in link_to_dl:
            url_link = links['href'][17:] #17 and on is because of a pre-link to video structure
            #remove characters not allowed in filenames and add an Episode Number
            filename = 'Ep' + str(episode_count) + ' - ' + links.text.replace(':',' -').replace('?','').replace('/','-') + '.mp4'
            urllib.request.urlretrieve(url_link, f'{folder_to_save_in}//{filename}') #downoad the video and save the name as the text in the <a href>
            print(f'Downloaded: {filename}')
            episode_count += 1

print('Finshed.')
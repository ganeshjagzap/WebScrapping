# importing all the required libraries
import requests as r
import bs4 as b
import re
import os

category_url = input("Enter the URL of the category: ")

num_of_pages = input("How many pages do you want to download?")

# Iterate through the specified number of pages
for index in range(1, int(num_of_pages) + 1):

    # Create the URL for the current page
    sampleurl = f"{category_url}/page/{index}"

    url = r.get(sampleurl)
    htmlcontent = url.text

    soup = b.BeautifulSoup(htmlcontent, 'html.parser')
    # allimgtags is list which contain all img tag with its attributes
    allimgtags = soup.find_all('img')

    # creating list for storing all links
    newsrclist = []
    # creating list for storing all names of images
    newnamelist = []
    count = 0
    # this loop for fetching the image links form the list allimgtags
    for i in allimgtags:
        mysrc = i['src']
        # mysrc contain 20 images links but we do not want first and last image that's why i applied folloing conditions
        if (count == 0):
            count += 1
            pass
        else:
            count += 1
            if (count == 20):

                pass
            else:
                newsrclist.append(mysrc)

    # This for loop fetch the all names of images form the links, newsrclist contains the links
    for name in newsrclist:
        '''
        image links look like
            'https://images.hdqwalls.com/wallpapers/thumb/elk-sunrise-4b.jpg'

        In this link , the image name is 
             elk-sunrise-4b.jpg
        '''

        ''' 
        So for extracting name from link , first i have to know the starting position of the name so i can 
        use slicing there to extract name , for that i use re module 
        '''
        pos = re.finditer('/', name)
        # This list contain the starting position of all the imges name
        poslist = []
        for i in pos:
            poslist.append(i.start())

        # here i append all the images name in newnamelist
        newnamelist.append(name[poslist[-1] + 1:])

    ''''
    newsrclist contain the images link which is look like
        'https://images.hdqwalls.com/wallpapers/thumb/elk-sunrise-4b.jpg'

    In above link there is one problem , this link contain */thumb* i.e. this link is for thumbnails
    so i have to remove that /thumb 

    after removing that /thumb i can able to download original image with high resolution
    '''
    # this list is for storing the links which do not contain /thumb
    finalimglist = []
    for i in newsrclist:

        ''''
        for removing the /thumb first i have to know the starting index of /thumb 
        '''
        # this list stores the starting position of /thumb
        thumbposlist = []
        thumpos = re.finditer('/thumb', i)
        for j in thumpos:
            thumbposlist.append(j.start())

        '''
        this variable contain the image link before /thumb
        i.e.  https://images.hdqwalls.com/wallpapers
        '''
        newsrc = i[0:thumbposlist[0]]
        '''
        this variable contain the image link after /thumb
        i.e.  /elk-sunrise-4b.jpg
        '''
        newsrc1 = i[thumbposlist[0] + 6:]
        finalimglist.append(newsrc + newsrc1)

    # print(finalimglist)
    print('***************************************************************')

    # now i make directry in the parent directry 'D:\os module' with prefix '/category page(pagenumber)'

    foldernameposstart = re.finditer('category/', sampleurl)
    foldernameposend = re.finditer('/page', sampleurl)
    foldernameindex = []
    for i in foldernameposstart:
        foldernameindex.append(i.end())
    for i in foldernameposend:
        foldernameindex.append(i.start())
    foldername = sampleurl[foldernameindex[0]:foldernameindex[1]]
    mydir = f'{foldername} page {index}'
    parentdir = 'D:\os module'

    # newdir variable join parentdir with mydir using os module
    newdir = os.path.join(parentdir, mydir)
    # this is for checking whether directry already available or not
    ifdirexist = os.path.exists(newdir)
    if (ifdirexist != True):
        print(newdir)
        # here i have create new directry to store images
        os.mkdir(newdir)

        count = 0
        # this loop is for fetching the all images from the page
    for i in finalimglist:
        # image vaiable load the image by using the request module
        image = r.get(i)
        print(image)

        # by using file handling concept i store the images into directy
        # image variable contain binary data that is why i have to open file in append binary format
        with open(newdir + f'/{newnamelist[count]}', 'ab') as f:
            f.write(image.content)
        count += 1

    print(newsrclist)





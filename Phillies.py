#import library
import requests #for accessing/scaping webpage
import lxml.html as lh
import pandas as pd #for data analysis
import locale #for currency formatting

#import the website (each reload should update GUI/change average)
url='https://questionnaire-148920.appspot.com/swe/data.html'

#cite for website scraping from: https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059

#create page
page = requests.get(url)

#store website contents under doc
doc = lh.fromstring(page.content)

#parse data between <tr>..</tr> where the table is located in the html 
tr_elements = doc.xpath('//tr')

#check len of the first 20 rows (should be the same aka 4)
print([len(T) for T in tr_elements[:20]])

#create empty list
col=[]
i=0
#since the method used in the reference wasn't working as anticipated, I decided to 
#hardcode the headers since it was stated the format of the table wouldn't change
#if the format had the potential to be dynamic, however, this would have to be fixed
headers = ["Players", "Salary", "Years", "Level"]

#for each row, store header and empty list
for t in tr_elements[0]:
    name = headers[0+i]
    i += 1 #increment to next col
    print('%d:"%s"'%(i , name)) #check that headers are implemented correctly 
    col.append((name , []))
    
#get data for each row 
for j in range(0,len(tr_elements)):
    #T is the j'th row
    T = tr_elements[j]
    
    #check if //tr len is 4
    if len(T)!= 4:
        break
    
    #col index from 0-3
    i=0
    #iterate thru each element of the row
    for t in T.iterchildren():
        data = t.text_content() #get data from html
        #Check if row is empty
        if i > 0:
        #convert any numerical value to integers (should only be year)
            try:
                data=int(data)
            except:
                pass
        #append the data to the empty list of i'th column
        #REVISE THIS- want to skip any row missing salary 
        if data == 'no salary data' or data == None or data == '':
                data = -1
        col[i][1].append(data)
        #move on to next col
        i+=1
        
#length of each col (should be the same)
print([len(C) for (title,C) in col])

Table = {title:column for (title,column) in col}
df=pd.DataFrame(Table)

#display beginning of table (prior to cleaning up fields)
df.head()

#clean up salary field
df['Salary'] = df['Salary'].str.replace(',', '')
df['Salary'] = df['Salary'].str.replace('$', '')

#convert to float
df['Salary'].astype('float')

#sort by salary descending order 
df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce') #despite dtype: float64, this is what seemed to actually convert to float
#cite: https://stackoverflow.com/questions/47914274/pandas-sort-values-does-not-sort-numbers-correctly
df = df.sort_values(by=['Salary'], ascending = False) #largest salaries are now at the top

#narrow list down to top 125
df = df.head(125)

#get the average salary
average = df['Salary'].mean()
locale.setlocale(locale.LC_ALL, '') #for formatting to currency 
average = locale.currency(average, grouping=True)
print(average) #will not be consistent as data is dynamic


import tkinter as tk #gui
import requests
import tkinter.font as tkFont #custom fonts

#canvas dimensions
HEIGHT = 600
WIDTH = 900

#root (welcome page)
root = tk.Tk()
root.minsize(WIDTH,HEIGHT)

#for displaying the calculated average 
#cite: https://stackoverflow.com/questions/2603169/update-tkinter-label-from-variable
var = tk.StringVar()
var.set(average)

#custom fonts
font1 = tkFont.Font(family="Segoe UI Light",size=16) #bold and large
root.font=font1
font2 = tkFont.Font(family="Segoe UI Light",size=24)
root.font2 = font2

#create canvas
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#title and icon 
root.title("Phillies Qualifying Offer: One Year Contract")
root.iconbitmap("philliesicon.ico")

#background image
bg_image = tk.PhotoImage(file='transparent_bg5.gif')
root.bg_image = bg_image
background_label = tk.Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)

#frame that holds the labels and buttons 
frame1 = tk.Frame(root, bg = "white",  borderwidth=2, relief="groove")
frame1.place(relx=0.2, rely=0.3, relwidth=0.6, relheight=0.4)

#labels
label = tk.Label(frame1, text="2016 qualifying offer", bg="white",font="font2")
label.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.25)


'''welcome page: BEGIN button event'''

#begin button event (go to main page)
def beginClick():

    
    #new page
    #cite- https://www.youtube.com/watch?v=qC3FYdpJI5Y&list=PLCC34OHNcOtoC6GglhF3ncJ5rLwQrLGnV&index=14&ab_channel=Codemy.com
    #canvas dimensions
    HEIGHT = 600
    WIDTH = 900

    average = '$16,000,000'

    #main
    main = tk.Toplevel()
    main.minsize(WIDTH,HEIGHT)
    
    #custom font
    font1 = tkFont.Font(family="Segoe UI Light",size=16)
    main.font = font1

    #create canvas
    canvas = tk.Canvas(main, height=HEIGHT, width=WIDTH)
    canvas.pack()

    #title and icon 
    main.title("Phillies Qualifying Offer: One Year Contract")
    main.iconbitmap("philliesicon.ico")

    #cite- image not getting garbage collected anymore
    #https://stackoverflow.com/questions/26479728/tkinter-canvas-image-not-displaying
    #background image
    background_image = tk.PhotoImage(file='transparent_bg5.gif')
    main.image = background_image
    background_label = tk.Label(main, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    #button events (change to redirecting to different page (phase 2))
    #accept button event 
    def acceptClick():
        
        #new page
        accept_win = tk.Toplevel()
        accept_win.minsize(WIDTH,HEIGHT)
        accept_win.title("Acceptance Page")
        accept_win.iconbitmap("philliesicon.ico")
        img = tk.PhotoImage(file='transparent_bg5.gif') #not showing up for some reason
        accept_win.img = img
        background_label = tk.Label(accept_win, image=img)
        background_label.place(relwidth=1, relheight=1)
        

        #frame that holds the labels and buttons 
        f = tk.Frame(accept_win, bg = "black",  borderwidth=2, relief="groove")
        f.place(relx=0.15, rely=0.1, relwidth=0.7, relheight=0.8)
        
        background_label = tk.Label(f, bg="white")
        background_label.place(relwidth=1, relheight=1)
        
        background_label = tk.Label(f, bg="white", text="Congratulations!\nYou have accepted the qualifying offer.\nThe Philadelphia Phillies look forward to\nhaving you again next year!", pady=10, padx=10, font="font1")
        background_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)


        #exit both windows
        #cite: https://stackoverflow.com/questions/55560127/how-to-close-more-than-one-window-with-a-single-click
        def qExit():
            accept_win.destroy()
            main.destroy()
            root.destroy()

        btn = tk.Button(f, text="exit", bg="#f4fdf4", activebackground="#b1d3b1", activeforeground="black",cursor="hand2", pady=10, padx=10, font="font1", command=qExit).place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1) 


    #decline button event 
    def declineClick():
        
        #new page (go to decline page)
        decline_win = tk.Toplevel()
        decline_win.minsize(WIDTH,HEIGHT)
        decline_win.title("Decline Page")
        decline_win.iconbitmap("philliesicon.ico")
        img = tk.PhotoImage(file='transparent_bg5.gif')
        decline_win.img = img
        background_label = tk.Label(decline_win, image=img)
        background_label.place(relwidth=1, relheight=1)
        
        
        #custom font
        font1 = tkFont.Font(family="Segoe UI Light",size=16)
        decline_win.font = font1
        
        #frame that holds the labels and buttons 
        f = tk.Frame(decline_win, bg = "black",  borderwidth=2, relief="groove")
        f.place(relx=0.15, rely=0.1, relwidth=0.7, relheight=0.8)
        
        background_label = tk.Label(f, bg="white")
        background_label.place(relwidth=1, relheight=1)
        
        background_label = tk.Label(f, bg="white", text="You have declined the qualifying offer.\nWe wish you the best of luck!\n-The Philadelphia Phillies", pady=10, padx=10, cursor="hand2", font="font1")
        background_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        
        #exit both windows
        #cite: https://stackoverflow.com/questions/55560127/how-to-close-more-than-one-window-with-a-single-click
        def qExit():
            decline_win.destroy()
            main.destroy()
            root.destroy()

        btn = tk.Button(f, text="exit",  bg="#f4fdf4", activebackground="#b1d3b1", activeforeground="black",cursor="hand2", pady=10, padx=10, font="font1", command=qExit).place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1) 

        
    #run average 
    def runClick():

        #show average
        average_label = tk.Label(frame1, textvariable=var, bg="white", font="font1")
        average_label.place(relx=0.45, rely=0.5, relwidth=0.3, relheight=0.3)
        
        #enable accept and decline button
        #cite: https://stackoverflow.com/questions/53580507/disable-enable-button-in-tkinter
        accept_btn["state"]=tk.NORMAL
        accept_btn["cursor"]= "hand2"
        decline_btn["state"]=tk.NORMAL
        decline_btn["cursor"]= "hand2"
        run_btn["state"]=tk.DISABLED
        run_btn["cursor"]= "arrow"
        

    #frame that holds the labels and buttons 
    frame1 = tk.Frame(main, bg = "white",  borderwidth=2, relief="groove")
    frame1.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.3)

    #frame that holds the labels and buttons 
    frame2 = tk.Frame(main, bg = "white",  borderwidth=2, relief="groove")
    frame2.place(relx=0.15, rely=0.5, relwidth=0.7, relheight=0.3)

    #labels
    label = tk.Label(frame1, text="Click RUN to generate the 2016 qualifying offer", bg="white",font="font1")
    label.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.25)

    label = tk.Label(frame2, text="Would you like to accept the qualifying offer?", bg="white",font="font1")
    label.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.25)

    #MAIN PAGE accept button
    accept_btn = tk.Button(frame2, text="accept", pady=10, padx=10, command=acceptClick, fg="black", bg="#f4fdf4",
                          activebackground="#b1d3b1", activeforeground="black",cursor="X_cursor", font="font1", borderwidth=2,
                          state=tk.DISABLED)
    accept_btn.place(relx=0.15, rely=0.5, relwidth=0.3, relheight=0.3)
    
    #MAIN PAGE decline button
    decline_btn = tk.Button(frame2, text="decline", pady=10, padx=10, command=declineClick, fg="black", bg="#f6ced2",
                           activebackground="#d3808a", activeforeground="black", cursor="X_cursor",font="font1", borderwidth=2,
                           state=tk.DISABLED)
    decline_btn.place(relx=0.55, rely=0.5, relwidth=0.3, relheight=0.3)
    
    #MAIN PAGE run button
    run_btn = tk.Button(frame1, text="run", pady=10, padx=10, command=runClick, fg="black", bg="white", activebackground="grey",
                       activeforeground="black",cursor="hand2", font="font1", borderwidth=2)
    run_btn.place(relx=0.15, rely=0.5, relwidth=0.2, relheight=0.3)
    
    #MAIN PAGE exit button
    btn = tk.Button(main, text="exit", bg="white", activebackground="grey", activeforeground="black",cursor="hand2", pady=10, padx=10, font="font1", command=root.destroy).place(relx=0.3, rely=0.85, relwidth=0.4, relheight=0.1) 



'''welcome page: HELP btn event '''
    
def helpClick():
    
    #new page (go to decline page)
    help_win = tk.Toplevel()
    help_win.minsize(WIDTH,HEIGHT)
    help_win.title("Help Page")
    help_win.iconbitmap("philliesicon.ico")
    img = tk.PhotoImage(file='transparent_bg5.gif')
    help_win.img = img
    background_label = tk.Label(help_win, image=img)
    background_label.place(relwidth=1, relheight=1)
    
    #custom font
    font1 = tkFont.Font(family="Segoe UI Light",size=16)
    help_win.font = font1
    
    #frame that holds the labels and buttons 
    f = tk.Frame(help_win, bg = "black",  borderwidth=2, relief="groove")
    f.place(relx=0.075, rely=0.1, relwidth=0.85, relheight=0.8)
    
    background_label = tk.Label(f, bg="white")
    background_label.place(relwidth=1, relheight=1)
    
    background_label = tk.Label(f, bg="white", text="A departing free agent player may be provided a qualifying offer.\n"
                                "A qualifying offer is a one year contract whose monetary value is\n"
                                "the average of the top 125 highest paid players.  Players have the\n"
                                "option to accept or reject the qualifying offer. Teams that extend\n"
                                "a qualifying offer risk forfeiting a draft pick if the player rejects the\noffer.", pady=10, padx=10, font="font1",justify="left")
    background_label.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
    
    #back
    btn = tk.Button(f, text="back", bg="#f4fdf4", activebackground="#b1d3b1", activeforeground="black",cursor="hand2", pady=10, padx=10, font="font1", command=help_win.destroy).place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.1) 
    
'''welcome page: buttons'''

#buttons
#begin button (go to main page)
begin_btn = tk.Button(frame1, text="begin", pady=10, padx=10, command=beginClick, fg="black", bg="#f4fdf4",
                      activebackground="#b1d3b1", activeforeground="black",cursor="hand2", font="font1", borderwidth=2)
begin_btn.place(relx=0.15, rely=0.5, relwidth=0.3, relheight=0.3)

#help button
help_btn = tk.Button(frame1, text="help", pady=10, padx=10, command=helpClick, fg="black", bg="#f4fdf4",
                      activebackground="#b1d3b1", activeforeground="black",cursor="hand2", font="font1", borderwidth=2)
help_btn.place(relx=0.55, rely=0.5, relwidth=0.3, relheight=0.3)
    
root.mainloop()
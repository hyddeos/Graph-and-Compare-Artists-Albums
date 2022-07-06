# Compare your favorite artist albums
## Description: Compare how any artist album compare to one and another. You can compare them in five different ways.

###This is my final project for the Harvard CS50x course
####Read more about the official site [cs50.harvard.edy/x/2022](https://cs50.harvard.edu/x/2022/)

**Files(3)**

Main.py - The only code file.
music.db - The database file where the artists, albums and songs will be stored.
READ ME.mb - Information about the code and the project.

**Goal and propose**

My goal with this program from the start was just to be able to graph one particular band with only one variable(tempo).
I wanted the graph to actually be meaningful and be clear enough to easily see how the albums compare to each other.
However, I later decided to make it much more versatile by making it possible to search for any other artist and to choose one of five different variables to plot.

If I had to remake this program I would for sure have made some different choices, one of them being to more clearly plan out exactly what the program would do.


**How it works**

First it checks the Spotify token to see if it authorizes the credentials.
Second step is the choose_artist() function. Here you will be asked to input the Spotify ID of the artist that you would like to check up(you will have to get it manually from a Spotify url).
Then get_albums() check if the artist already is in the database or else the albums and songs get added. 
I have set a limit of 20 albums since more albums than that just gets completely unreadable.

I know that it would probably been easier to skip the whole database part and just use the data from Spotify directly. But since databases was a big part out the course I wanted to try it out further and get more experience working with them.

The plot_datahandle() function then prepares the data for the plotting function later on. Getting the data from the own database this time and not from the Spotify API.

Last but not least was the plotting and graphing part. This was my first time using Matplotlib and any graph-tool what-so-ever and this proved to be the hardest part by far.
From the start I wanted to make all songs on an album to be marked at the right time on the timeline(x-axis). So for example, if the fifth song started 35 minutes into the album I wanted it to get placed at the 35-minute mark.
I was never able to full solve this but since I feel like my main goal(comparing albums clearly against each other) still was attained I did not fix it. This is why there still are parts of the code that refers to this function.
Except for this part, I spent most time making the colors of the lines match the colors of the albums in the Legend. I do not really think my solution is the optimal one, but it works.

After that you will choose what you want to plot of: Danceability, Energy, Intrumentalness, Tempo or Valence.

The id_filter() function makes it possible to filter out some albums that you might not want to compare. You have to do this manually. In my case I want to filter out live and remastered albums to get cleaner results.


**Improvements and known problems**

I want to keep developing this. Not just fix the problems but also take it further.
First of, I should make the choose_artist() function save from bad input or if Spotify simply doesn't find the artist. But the best thing would be a real search function to skip the hassle with artist id.
I would like to add a better function to choose what albums to exclude. Lastly I would like to be able to fix the part where you can see in what minute on the graph the songs end(i.e make the x axis display the albums more in real time how they develop over the album.)


**Sources**

To get the Spotify API working i got a lot of help from the [Ashley Gingeleski guide](https://ashleygingeleski.com/2019/11/11/spotify-web-api-how-to-pull-and-clean-top-song-data-using-python/)





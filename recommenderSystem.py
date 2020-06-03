#!/usr/bin/python3

from math import sqrt
import re
import sys
"""
Function to read files (movie-names.txt, movie-matrix.txt, input.txt) and store them in list
"""
def readFile():
    movieNameList=[]
    movieReviewList=[]
    inputMovieList=[]
    with open('/home/turing/t90rkf1/d656/dhw/hw3-recom/movie-names.txt','r',encoding='latin-1') as f:
        # read a movie-names file and split them based on '|' and append them to movieNameList
        for line in f:
            movieNameList.append([line.split("|")[0].rstrip(),line.split("|")[1].rstrip()])
    with open('/home/turing/t90rkf1/d656/dhw/hw3-recom/movie-matrix.txt', 'r') as f:
        #read a movie-matrix file and split them based on ';' and append them to movieReviewList
        for line in f:
            movieReviewList.append(line.rstrip().split(';'))
    print("\n")
    print("*** No. of rows (movies) in matrix =  ",len(movieNameList)) #print the total rows in movie names file
    print("*** No. of columns (reviewers) = "+str(len(movieReviewList[1]))) #print the total columns in movie matrix file
    regex = '[0-9]+$'
    # read a input file and check the given number is present in range of movie-names(1 to 1682)
    for line in sys.stdin:
        line = line.rstrip()
        # regular expression to check given input is numeric or not
        if (re.search(regex, line)):
            if int(line) > 0 and int(line) < 1683:
                index = int(line) - 1
                # if number is in range of 1 to 1682 then call smiliar movies function to calculate similar rated movies
                similarMovies(movieNameList, movieReviewList, [line, index])
            else:
                print("\nMovie:   " + str(line) + "  Movie number must be between 1 and 1682")
        else:
            print("\nMovie:  " + line + "  Movie number must be numeric")
    return movieNameList, movieReviewList, inputMovieList

"""
function to calculate mean of given movie ratings
Formula: (total sum/total count)
"""
def meanMovie(movie):
    sum=0
    for i in movie:
        sum+=int(i)
    return (sum/len(movie))
"""
function to calculate standard deviation of rating using mean calculated previously
Formula: squareroot((sum(movie-mean)power 2) / total count)
"""
def stdMovie(movie,mean):
    sum = 0
    for i in range(len(movie)):
        sum = sum + (int(movie[i]) - mean) **2
    return sqrt(sum / (len(movie) - 1))
"""
function to calculate pearson value for usergiven movie and remaining movies using mean and standard deviation calculated previously
Formula: (total sum((other movie - mean1)* (usergiven movie - mean2)/(std1*std2))/(total count - 1)
"""
def pearsonCompute(movieTarget,movieCompare):
    if len(movieTarget) != len(movieCompare):
        raise ValueError("The rating list lengths are different")
    movie1 = meanMovie(movieTarget)
    movie2 = meanMovie(movieCompare)
    stdmovie1 = stdMovie(movieTarget, movie1)
    stdmovie2 = stdMovie(movieCompare, movie2)
    comparison_sum = 0
    for i in range(len(movieTarget) and len(movieCompare)):
        comparison_sum += ((int(movieTarget[i]) - movie1) * (int(movieCompare[i]) - movie2) / (stdmovie1 * stdmovie2))
    return (comparison_sum / (len(movieTarget) - 1))
"""
calculate similar movies and print them, target movies must have atleat 10 reviewers.
"""
def similarMovies(movieName,movieReview, inputMovieList):
    print("\nMovie:    "+inputMovieList[0]+"  "+movieName[inputMovieList[1]][1])
    print("  #       R       No.     Reviews        Name")

    UserSelectedMovie = movieReview[inputMovieList[1]]
    similarMoviesList = []
    for i in range(len(movieName)):
        movieTarget, movieCompare = [], []
        reviewCount=0
        targetMovie = movieReview[i]
        for j in zip(UserSelectedMovie,targetMovie):
            if ((j[0] != '') & (j[1] != '')):
                reviewCount += 1
                movieTarget.append(j[0])
                movieCompare.append(j[1])
        if reviewCount >=10:
            similarMoviesList.append([i,pearsonCompute(movieTarget,movieCompare),reviewCount])
    if (len(similarMoviesList) < 20):
        print("  Insufficient comparison movies\n")
    else:
        similarMoviesList = sorted(similarMoviesList, key=lambda similarMoviesList: similarMoviesList[-2], reverse=True)[:20]
        for i in range(len(similarMoviesList)):
            print(" %2d.   %6f  %4d ( %3d reviews)  %s"%(i+1,similarMoviesList[i][1],similarMoviesList[i][0]+1,similarMoviesList[i][2],movieName[similarMoviesList[i][0]][1]))

if __name__ == "__main__":
    readFile()


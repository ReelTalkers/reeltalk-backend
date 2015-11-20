from django.core.management.base import BaseCommand, CommandError
from reeltalk.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        userlist = UserProfile.objects.all() # list

        def findSimilarUsers( currentUser, userList):
            similarityList = []
            currentUserReviews = Review.objects.filter(user = currentUser)
            for u in userList:
                if u.id != currentUser.id:
                    matches = 0
                    totalDifference = 0
                    reviews = Review.objects.filter(user=u)
                    for r in reviews:
                        if currentUserReviews.filter(show__id=r.show.id).exists():
                            totalDifference += abs(currentUserReviews.get(show__id = r.show.id).score - r.score)
                            matches+=1
                    if matches>0:
                        similarityList.append((u.id, 2 - totalDifference / matches))
            similarityList = [user for user in similarityList if user[1] > 0]
            return similarityList

        def findMovieRecommendations( currentUser, userList):
            similarUsers = findSimilarUsers( currentUser, userList)
            currentUserReviews = Review.objects.filter(user = currentUser)
            possibleMovieDict = {}
            for u in similarUsers:
                reviewedMovies = Review.objects.filter(user__id = u[0])
                for r in reviewedMovies:
                    if not currentUserReviews.filter(show__id=r.show.id).exists():
                        weightedScore = (r.score - 3)*u[1]
                        if possibleMovieDict.get(r.show.id, False):
                            totalWeightedScore = possibleMovieDict[r.show.id] + weightedScore
                            possibleMovieDict[r.show.id] = totalWeightedScore
                        else:
                            possibleMovieDict[r.show.id] = weightedScore
            return possibleMovieDict

        def findGroupMovieRecommendations( group, userList ):
            possibleMovieDict = {}
            for u in group:
                recommendedMovies = findMovieRecommendations( u, userList )
                # filters movies so nobody has seen any of the movies
                recommendedMovies = { key:recommendedMovies[key] for key in recommendedMovies.keys() if hasNotSeen(group, key)}
                for m in recommendedMovies.keys():
                    score = recommendedMovies[m]
                    if possibleMovieDict.get(m, False):
                        totalScore = possibleMovieDict[m] + score
                        possibleMovieDict[m] = totalScore
                    else:
                        possibleMovieDict[m] = score
            return possibleMovieDict

        def hasNotSeen(group, showId):
            for u in group:
                reviewedMovies = Review.objects.filter(user__id = u.id)
                for r in reviewedMovies:
                    if r.show.id == showId:
                        return False
            return True


        group = [userlist.first()]
        group.append(userlist.get(id = 2))
        print(findGroupMovieRecommendations(group, userlist))

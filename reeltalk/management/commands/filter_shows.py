from django.core.management.base import BaseCommand, CommandError
from reeltalk.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        userlist = UserProfile.objects.all() # list

        def findSimilarUsers( currentUser, userList):
            similarityList = []
            currentUserReviews = Review.objects.filter(user = currentUser)
            for u in userList:
                if(u.id != currentUser.id):
                    matches = 0
                    totalDifference = 0
                    reviews = Review.objects.filter(user=u)
                    for r in reviews:
                        if currentUserReviews.filter(show__id=r.show.id).exists():
                            totalDifference += abs(currentUserReviews.get(show__id = r.show.id).score - r.score)
                            matches+=1
                    if(matches>0):
                        similarityList.append((u.id, 2 - totalDifference / matches))
            similarityList = [user for user in similarityList if user[1] > 0]
            return similarityList

        def findMovieRecommendations( currentUser, similarUsers):
            currentUserReviews = Review.objects.filter(user = currentUser)
            possibleMovieDict = {}
            for u in similarUsers:
                reviewedMovies = Review.objects.filter(user__id = u[0])
                for r in reviewedMovies:
                    if(!currentUserReviews.filter(show__id=r.show.id).exists()):
                        weightedScore = (r.score - 3)*u[1]
                    if(possibleMovieMap.has_key(r.show.id)):
                        totalWeightedScore = possibleMovieMap[r.show.id] + weightedScore
                        possibleMovieMap[r.show.id] = totalWeightedScore
                    else:
                        possibleMovieMap[r.show.id] = weightedScore
            return possibleMovieMap

        similarUsers = findSimilarUsers(userlist.first(), userlist)
        print(findMovieRecommendations(userlist.first(), similarUsers))

        # print(findSimilarUsers(userlist.first(), userlist))

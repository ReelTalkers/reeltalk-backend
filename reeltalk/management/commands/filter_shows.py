from django.core.management.base import BaseCommand, CommandError
from reeltalk.models import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        userlist = UserProfile.objects.all() # list
        currentUser = userlist.first()

        def findSimilarUsers( currentUser, userList):
            similarityDict = {}
            currentUserReviews = Review.objects.filter(user = currentUser)
            for u in userList:
                matches = 0
                totalDifference = 0
                reviews = Review.objects.filter(user=u)
                for r in reviews:
                    if currentUserReviews.filter(show__id=r.show.id).exists:
                        totalDifference += abs(currentUserReviews.get(show__id = r.show.id).score - r.score)
                        matches+=1
                        if(matches>0):
                            similarityDict[u.id] = 2 - totalDifference / matches

        print(findSimilarUsers(userlist.first(), userlist))

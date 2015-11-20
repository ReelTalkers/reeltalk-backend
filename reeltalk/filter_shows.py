from .models import *

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

def find_group_movie_recommendations( group, userList ):
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
    recommendedMovies = { key:recommendedMovies[key] for key in recommendedMovies.keys() if recommendedMovies[key]>0}
    return possibleMovieDict

def get_show_recommendations_via_group(group, users):
    scores = find_group_movie_recommendations(group, users)
    sorted_show_ids = sorted(scores, key=scores.get, reverse=True)
    return [Show.objects.get(id=show_id) for show_id in sorted_show_ids]


def hasNotSeen(group, showId):
    for u in group:
        reviewedMovies = Review.objects.filter(user__id = u.id)
        for r in reviewedMovies:
            if r.show.id == showId:
                return False
    return True

from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=150)
    genre = models.ForeignKey(Genre, related_name='movies', on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)
    description = models.TextField()
    release_date = models.DateField()
    cover_img = models.ImageField(upload_to='images/')

    def __str__(self) -> str:
        return self.title

class UserRating(models.Model):
    user_id = models.IntegerField()
    movie = models.ForeignKey(Movie, related_name='user_rating', on_delete=models.CASCADE)
    rating = models.FloatField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.update_movie_rating()

    def update_movie_rating(self):
        all_ratings = UserRating.objects.filter(movie=self.movie)
        new_rating = sum(r.rating for r in all_ratings) / len(all_ratings)
        self.movie.rating = new_rating
        self.movie.save()
    
    def __str__(self):
        return f'{self.user_id}|{self.movie}|{self.rating}'

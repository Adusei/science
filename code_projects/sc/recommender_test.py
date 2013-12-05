# from crab import datasets
import crab as datasets


movies = datasets.load_sample_movies()
songs = datasets.load_sample_songs()

print movies.data
import csv
import os
import sys
from data_analyse.analysis import (
    spotify_popularity_by_artist,
    avg_itunes_price_genre
)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = current_dir
sys.path.append(project_dir)

def write_results_to_csv():
    with open("spotify_popularity.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Artist", "Average Popularity"])

        for name, popularity in spotify_popularity_by_artist():
            writer.writerow([name, popularity])

    with open("itunes_genre_prices.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Genre", "Average Track Price"])

        for genre, price in avg_itunes_price_genre():
            writer.writerow([genre, price])

if __name__ == "__main__":
    write_results_to_csv()
# Introduction

Inspired by Kaggle user [Yonatan Rabinovich](kaggle.com/yonatanrabinovich)'s work, we present an anime recommendation engine that takes an anime title as input, and outputs a list of recommendations, sorted in descending order, based on their similarities to the input. Specifically, we computed the pairwise cosine similarities between the mean-normalized feature vectors for 11,161 animes available on [myanimelist.net](https://myanimelist.net/)'s catalog, as of 2021. The full analysis is detailed in `analysis.ipynb`, and the recommendation pipeline is defined as a Python function in `src/utils.py`. 

# Installation

To play around with the recommendation engine yourself, simply `git clone` the repository onto your local machine.
```
git clone https://github.com/zachtheyek/Anime-Rec-Bot.git
```
Then, either run `analysis.ipynb` once through, or download [`similarities.csv`](https://drive.google.com/drive/folders/1yOZsmFC75oBtUvpDXPoj7U887m1LvwZT?usp=sharing) directly through Google Drive, and place it in the `src/` directory. This additional step is required due to the file's size exceeding GitHub's 2 GB limit.

# Documentation

```
get_recommendations(anime, num_recs=5, threshold=0.2, type=True, df_list=[])
```
* `anime`: The anime title you want to get recommendations for.
* `num_recs`: The number of recommendations you want to get (default=5).
* `threshold`: The threshold for the cosine similarity value (default=0.2).
* `type`: If True, you'll only get recommendations of a similar type, e.g. TV, Movie, OVA, Special, etc. (default=True).
* `df_list`: The dataframes you want to use for the recommendations.

# Examples

A comprehensive guide to using and troubleshooting `get_recommendations`, with examples and detailed explanations, is given in `inference.ipynb`. Here, we'll list a couple examples to get you started:

The most straightforward way of calling the `get_recommendations` function is to simply pass in an anime title of your choice.
```
>>> Input: get_recommendations('Naruto')
>>> Output:
Calibrating, please wait...
Fetching recommendations...
Since you watched Naruto, we recommend:

	 #1 - Sword Art Online (29.19% match)
	 #2 - Bleach (28.06% match)
	 #3 - Elfen Lied (27.78% match)
	 #4 - Ao no Exorcist (26.80% match)
	 #5 - Shaman King (22.70% match)
```

One can also pass in additional arguments.
```
>>> Input: get_recommendations('Dragon Ball Z', num_recs=10, threshold=0.4)
>>> Output:
Calibrating, please wait...
Fetching recommendations...
Since you watched Dragon Ball Z, we recommend:

	 #1 - Dragon Ball (75.66% match)
	 #2 - Fullmetal Alchemist (41.05% match)
	 #3 - Death Note (40.74% match)

No more recommendations found.
```
```
>>> Input: get_recommendations('Dragon Ball Z', num_recs=20, threshold=0.25, type=False)
>>> Output:
Calibrating, please wait...
Fetching recommendations...
Since you watched Dragon Ball Z, we recommend:

	 #1 - Dragon Ball (75.66% match)
	 #2 - Fullmetal Alchemist (41.05% match)
	 #3 - Death Note (40.74% match)
	 #4 - Dragon Ball Z Special 2: Zetsubou e no Hankou!! Nokosareta Chousenshi - Gohan to Trunks (35.85% match)
	 #5 - Code Geass: Hangyaku no Lelouch (35.49% match)
	 #6 - Yuu☆Yuu☆Hakusho (35.46% match)
	 #7 - Neon Genesis Evangelion (35.22% match)
	 #8 - Digimon Adventure (34.57% match)
	 #9 - Rurouni Kenshin: Meiji Kenkaku Romantan (33.88% match)
	 #10 - Dragon Ball Kai (33.80% match)
	 #11 - Code Geass: Hangyaku no Lelouch R2 (33.58% match)
	 #12 - Trigun (32.88% match)
	 #13 - Cowboy Bebop (32.87% match)
	 #14 - Tengen Toppa Gurren Lagann (32.78% match)
	 #15 - Fullmetal Alchemist: Brotherhood (32.42% match)
	 #16 - Samurai Champloo (32.09% match)
	 #17 - Dragon Ball Z Special 1: Tatta Hitori no Saishuu Kessen (32.08% match)
	 #18 - Soul Eater (31.73% match)
	 #19 - Shingeki no Kyojin (30.88% match)
	 #20 - Clannad (30.78% match)
```

Be careful of typos or "mistranslations".
```
>>> Input: get_recommendations('Maruto')
>>> Output:
Calibrating, please wait...
Anime title not found. Please check for typos, or perhaps try using the anime's original (phonetic Japanese) name.
```
```
>>> Input: get_recommendations('naruto')
>>> Output:
Calibrating, please wait...
Anime title not found. Please check for typos, or perhaps try using the anime's original (phonetic Japanese) name.
```
```
>>> Input: get_recommendations('Attack on Titan')
>>> Output:
Calibrating, please wait...
Anime title not found. Please check for typos, or perhaps try using the anime's original (phonetic Japanese) name.
```
```
>>> Input: get_recommendations('Shingeki no Kyojin')
>>> Output:
Calibrating, please wait...
Fetching recommendations...
Since you watched Shingeki no Kyojin, we recommend:

	 #1 - No Game No Life (55.45% match)
	 #2 - Death Note (49.32% match)
	 #3 - Angel Beats! (48.91% match)
	 #4 - Noragami (48.71% match)
	 #5 - One Punch Man (48.08% match)
```

# Faster Runtimes

Each function call takes ~1.5 mins on a typical machine. To reduce this to only a few seconds, read in the relevant data into memory beforehand, and pass it in via the `df_list` parameter. Note that the order of elements does not matter, nor do you need to have both files loaded into memory to invoke the argument.
```
# low_memory must be disabled to avoid DType error
similarities = pd.read_csv('src/similarities.csv', low_memory=False)
features = pd.read_csv('src/features.csv', low_memory=False)
```
```
>>> Input: get_recommendations('Dragon Ball Z', num_recs=20, threshold=0.3, type=False, df_list=[similarities, features])
>>> Output: 
Calibrating, please wait...
Fetching recommendations...
Since you watched Dragon Ball Z, we recommend:

	 #1 - Dragon Ball (75.66% match)
	 #2 - Fullmetal Alchemist (41.05% match)
	 #3 - Death Note (40.74% match)
	 #4 - Dragon Ball Z Special 2: Zetsubou e no Hankou!! Nokosareta Chousenshi - Gohan to Trunks (35.85% match)
	 #5 - Code Geass: Hangyaku no Lelouch (35.49% match)
	 #6 - Yuu☆Yuu☆Hakusho (35.46% match)
	 #7 - Neon Genesis Evangelion (35.22% match)
	 #8 - Digimon Adventure (34.57% match)
	 #9 - Rurouni Kenshin: Meiji Kenkaku Romantan (33.88% match)
	 #10 - Dragon Ball Kai (33.80% match)
	 #11 - Code Geass: Hangyaku no Lelouch R2 (33.58% match)
	 #12 - Trigun (32.88% match)
	 #13 - Cowboy Bebop (32.87% match)
	 #14 - Tengen Toppa Gurren Lagann (32.78% match)
	 #15 - Fullmetal Alchemist: Brotherhood (32.42% match)
	 #16 - Samurai Champloo (32.09% match)
	 #17 - Dragon Ball Z Special 1: Tatta Hitori no Saishuu Kessen (32.08% match)
	 #18 - Soul Eater (31.73% match)
	 #19 - Shingeki no Kyojin (30.88% match)
	 #20 - Clannad (30.78% match)
```
This utility is especially useful, since the time saved compounds as the number of consecutive function calls increases.

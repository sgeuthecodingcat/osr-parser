# OSR-PARSER
Simple program written in Python for osu! replays

# What it can do

> [!IMPORTANT]
> While osu!lazer replays are supported with this tool, since they are similar to osu!classic replays, for some odd reason, mods in osu!lazer replays refuse to parse properly 

Extract the following data:
* Player Username
* Beatmap (hash)
* Accuracy (percent)
* UR (locally calculated using replay data)
* Game Mode
* Mods (osu!classic replays only)
* Score
* Combo (in number)
* 300s/100s/50s/Mises
* Geki & Katus
* Replay Length

# How to use it
Type into terminal (OS X & Linux):
``python3 osr-parser.py -osr /path/to/file.osr -osu /path/to/extracted/beatmap.osu``
OR
``python3 osr-parser.py --osr-path /path/to/file.osr --osu-path /path/to/extracted/beatmap.osu``

Type into CMD (Windows):
``py osr-parser.py -osr C:/path/to/file.osr -osu /path/to/extracted/beatmap.osu``
OR
``py osr-parser.py --osr-path C:/path/to/file.osr --osu-path /path/to/extracted/beatmap.osu``

# Mopidy-Playlist-Generator
## Python script to generate random playlists for Mopidy/Pi MusicBox

This python script will create a random playlist of a given length (or default 50, max 1000) of all tracks in the SQLite database.
Also preferred genres can be defined.

Playlists are placed in the __playlists_dir__ directory defined in your settings.ini file.
## Usage

```
usage: mopidy-playlist-db.py [-h] [-l PLAYLISTLENGTH] [-g GENRE] [-t TITLE]

optional arguments:
  -h, --help            show this help message and exit
  -l PLAYLISTLENGTH, --playlistLength PLAYLISTLENGTH
                        Supply the length of the playlist.
  -g GENRE, --genre GENRE
                        Supply the genre(s) of the tracks to pick. This should
                        be a comma seperated list like 'Pop, Rock'
  -t TITLE, --title TITLE
                        Supply the tile of the playlist
```
### Examples
To generate a playlist of 50 random tracks from all genres with the (default) title *Random playlist* use:

```python mopidy-playlist-db.py```

To generate a playlist of 100 random tracks from the genres *Alternative* and *Indie* with the title *Alternative random playlist* use:


```python mopidy-playlist-db.py -l 100 -t 'Alternative random playlist' -g 'Alternative, Indie'```

I call the script (from another python script) everytime before power-down, to generate a couple of fresh playlists, like this:
```python
call(['python', '/home/mopidy/mopidy-playlist/mopidy-playlist-db.py', '-l', '50', '-t', 'Alternative', '-g' 'Alternative, Indie'], shell=False)
```

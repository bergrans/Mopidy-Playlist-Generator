import sqlite3
import argparse
import ConfigParser

# script settings
mopidy_setting_file = '/boot/config/settings.ini'
default_list_length = 50
max_list_length = 1000

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-l", "--playlistLength", help="Supply the length of the playlist.", type=int, default=default_list_length)
    parser.add_argument("-g", "--genre", help="Supply the genre(s) of the tracks to pick. This should be a comma seperated list like 'Pop, Rock'", type=str, default='all')
    parser.add_argument("-t", "--title", help="Supply the tile of the playlist", type=str, default='Random playlist')

    # Parse arguments
    args = parser.parse_args()
    return args

# Get the script arguments
args = parseArguments()

# read settings from mopidy ini file
config = ConfigParser.RawConfigParser()
config.read(mopidy_setting_file)
# get output path
playlists_dir = config.get('local','playlists_dir')
# get sqlite db path
data_dir = config.get('local','data_dir')
db_library = config.get('local','library')

# Connect to sqlite database
db_file = data_dir + '/' + db_library + '/library.db'
conn = sqlite3.connect(db_file)
cur_track = conn.cursor()
cur_art = conn.cursor()

# set list length
list_length = int(args.playlistLength)
if list_length <= 0 or list_length > max_list_length:
    list_length = default_list_length

# open playlist file
playlist_file = open(playlists_dir + '/' + args.title + '.m3u', 'w')
playlist_file.write('#EXTM3U\n')

# build db query
query = 'SELECT  artists, uri, name, length FROM track '
if args.genre != 'all':
    genres = args.genre.split(",")
    for i, val in enumerate(genres):
        genres[i] = '"' + val.strip() + '"'
    gen = ",".join(genres)
    query += 'WHERE genre IN (' + gen + ') '
query += 'ORDER BY RANDOM() LIMIT ' + str(list_length)

track_count = 0;

# get n random tracks from the database
for track_data in cur_track.execute(query):
    artist_data = ['Unkown']
    if track_data[0] is not None:
        # get the artist data from database
        artist_uri = (track_data[0],)
        cur_art.execute('SELECT name FROM artist WHERE uri = ?', artist_uri)
        artist_data = cur_art.fetchone()

    # alter track uri to the absolute file path
    uri = track_data[1].replace('local:track:', config.get('local','media_dir') + '/')
    track_count += 1;

    # display results
    print str(track_count) + ': ' + artist_data[0].encode('UTF-8') + ' - ' + track_data[2].encode('UTF-8')

    # print to file
    playlist_file.write('#EXTINF:' + str(track_data[3]/1000) + ', ' + artist_data[0].encode('ascii', 'xmlcharrefreplace') + ' - ' + track_data[2].encode('ascii', 'xmlcharrefreplace') + '\n')
    playlist_file.write('file://' + uri + '\n')

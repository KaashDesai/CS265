import os, sys

def read_db(filepath):
	"Reads the cd database file, then returns a dictionary holding all of its data"
	lines = iter(open(filepath, 'r'))

	artists = {} # structure to hold all of the data from file
	artist = ""
	albumName = ""
	songs = []
	for line in lines:
		if artist == "":
			artist = line.rstrip('\n')
		elif albumName == "":
			albumName = line.rstrip('\n')
		elif line in ['\n', '\r\n']:
			artist = ""
			albumName = ""
			songs = []
		else:	
			song = line[1:].rstrip('\n')
			songs.append(song)
			if artist in artists:
				innerDict = artists[artist]
				innerDict[albumName] = songs
			else:
				artists[artist] = {albumName:songs}
	return artists

def write_db(filepath,artists):
	"Commits changes to the cd database (add or delete) and overwrites specified path"
	tmpfilepath = filepath + '.tmp'
	f = open(tmpfilepath, 'w')

	l = sorted(artists)
	for artist in l:
		albums = sorted(artists[artist])
		for album in albums:
			f.write(artist + '\n')
			f.write(album + '\n')
			for song in artists[artist][album]:
				f.write('-' + song + '\n')
			f.write('\n')
	f.close()

	os.rename(tmpfilepath,filepath) # replace existing db file with new one

def list_album(artists):
	"Displays a menu for navigating thru the cd database, represented as a dict"
	state = 0 # to keep track of where we are in the menu
	curArtist = ''
	curAlbum = ''

	while True:
		if state == 0:
			print 'Enter a # to view artist, or q to exit.'
			l = sorted(artists)
			for i, artist in enumerate(l):
				print str(i) + '. ' + artist
			n = raw_input()
			if n == 'q':
				break
			elif n.isdigit() and int(n) < len(l):
				curArtist = l[int(n)]
				state = 1
			else:
				print '\nInvalid input, try again\n'
		elif state == 1:
			print '\nEnter a # to view album, or a to go back:'
			l = sorted(artists[curArtist])
			for i, album in enumerate(l):
				print str(i) + '. ' + album
			n = raw_input()
			if n == 'a':
				state = 0
			elif n.isdigit() and int(n) < len(l):
				curAlbum = l[int(n)]
				state = 2
			else:
				print '\nInvalid input, try again\n'
		elif state == 2:
			print '\nShowing album songs:'
			for song in artists[curArtist][curAlbum]:
				print song
			print '\nEnter a to go back to artist menu:'
			n = raw_input()
			if n == 'a':
				state = 0

def delete_album(artists):
	"Deletes a user-specified album from the specified cd database"
	state = 0 # to keep track of where we are in the menu
	curArtist = ''
	curAlbum = ''

	while True:
		if state == 0:
			print 'Enter a # to view artist, or q to exit.'
			l = sorted(artists)
			for i, artist in enumerate(l):
				print str(i) + '. ' + artist
			n = raw_input()
			if n == 'q':
				break
			elif n.isdigit() and int(n) < len(l):
				curArtist = l[int(n)]
				state = 1
			else:
				print '\nInvalid input, try again\n'
		elif state == 1:
			print '\nEnter a # to delete respective album, or a to go back:'
			l = sorted(artists[curArtist])
			for i, album in enumerate(l):
				print str(i) + '. ' + album
			n = raw_input()
			if n == 'a':
				state = 0
			elif n.isdigit() and int(n) < len(l):
				curAlbum = l[int(n)]
				del artists[curArtist][curAlbum]
				if not artists[curArtist]: # if no albums left
					del artists[curArtist] # remove artist
				state = 0
			else:
				print '\nInvalid input, try again\n'

def add_album(artists):
	"Add a user-specified album to the specified cd database"
	artist = ""
	album = ""
	date = ""
	song = "temp" # placeholder
	songs = []

	# get all music info from user
	print 'Specify artist:'
	while not artist:
		artist = raw_input()
	print 'Specify album:'
	while not album:
		album = raw_input()
	print 'Specify release date:'
	while not date:
		date = raw_input()
		if artists.has_key(artist) and artists[artist].has_key(date + ' ' + album):
			print 'Album already exists, exiting...'
			sys.exit(2)
	print 'Specify track list (press enter twice to exit):'
	while song or not songs: # prompt until user has entered at least one track
		song = raw_input()
		if song:
			songs.append(song)

	# now add all info to master dictionary of artists
	album = date + ' ' + album
	if artist in artists:
		innerDict = artists[artist]
		innerDict[album] = songs
	else:
		artists[artist] = {album:songs}

def show_help():
	"Prints out program usage information"
	print 'Only specify exactly one of the following options:'
	print '-l --display menu to see artists, albums, and songs'
	print '-d --delete an album(s) from the database'
	print '-a --add an album to the database'
	print '-h --display this usage information'

def main(argv):
	filepath = os.environ['CDDB']

	if len(argv) != 1:
		show_help()
	elif argv[0] == '-l':
		artists = read_db(filepath)
		list_album(artists)
	elif argv[0] == '-d':
		artists = read_db(filepath)
		delete_album(artists)
		write_db(filepath,artists)
	elif argv[0] == '-a':
		artists = read_db(filepath)
		add_album(artists)
		write_db(filepath,artists)
	elif argv[0] == '-h':
		show_help()
	else:
		show_help()

if __name__ == "__main__":
	main(sys.argv[1:])

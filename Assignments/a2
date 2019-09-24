data = file('./sample.in', 'r')
teams = {} # structure to hold all of the data from file
for line in data:
	line = line.rstrip('\n').split(',')
	team = line[2]
	playerName = line[0] + ', ' + line[1]
	stats = line[3:]
	
	if team in teams:
		innerDict = teams[team]
		innerDict[playerName] = stats
	else:
		teams[team] = {playerName:stats}

# to keep track of where we are in the menu
state = 0
curTeam = ''
curPlayer = ''

statNames = ['Position:', 'At bats:', 'Base hits:', 'Doubles:', 'Triples:', 'Home runs:', 'RBI:', 'Batting avg:']

while True:
	if state == 0:
		print 'Please choose a team by #. Any non-integer will exit.'
		tl = sorted(teams)
		for i, t in enumerate(tl):
			print str(i) + '. ' + t
		n = raw_input()
		if not n.isdigit():
			break
		elif int(n) < 0 or int(n) >= len(tl):
			print 'Invalid team number, try again'
		else:
			curTeam = tl[int(n)]
			state = 1
	elif state == 1:
		print '\nPlease choose a player by #, b to go back:'
		pl = sorted(teams[curTeam])
		for i, p in enumerate(pl):
			print str(i) + '. ' + p
		n = raw_input()
		if n == 'b':
			state = 0
		elif not n.isdigit() or int(n) >= len(pl):
			print 'Invalid input, try again'
		else:
			curPlayer = pl[int(n)]
			state = 2
	elif state == 2:
		print '\nShowing player stats:'
		for s, n in zip(teams[curTeam][curPlayer], statNames):
			print n, s
		print '\nPress b to go back to team menu:'
		n = raw_input()
		if n == 'b':
			state = 0

import socket , datetime, time , sqlite3

nick = "MGreet"
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect(("irc.freenode.net",6667))
irc.send("NICK "+nick+"\r\n")
irc.send("USER "+nick+" MGreet MGreet :MGreet\r\n")
irc.send("JOIN #mgreet\r\n")

con = sqlite3.connect('mgbot.sql')
con.text_factory = str
cur = con.cursor()

while True:
	data = irc.recv(4096)
	print data
	for line in data.split('\n'):
		word = line.split(' ')
		if len(word) == 3:
			if word[1] == "JOIN":
				player = word[0].split('!')[0][1:]
				clean_player = player.split('_')
				if len(clean_player) == 3:
					clean_player = clean_player[1]
					if player[:3] == "MG_" and player[3:9] == "newbie":
						irc.send("PRIVMSG #megaglest-lobby :Hi "+player+" , Welcome to Megaglest .Plesae consider changing your nick at Menu > Options ,also try playing tutorials and some scenarios first if you didn't already. If you did , please wait for someone to join.\r\n")
					elif player[:3] == "MG_" and player[3:9] != "newbie":
						date = datetime.datetime.now().strftime("%H:%M:%S")
						cur.execute("SELECT * FROM players WHERE nick=?",[clean_player])
						row = cur.fetchone()
						if row:
							joins = row[1]+1
							con.execute("UPDATE players SET joins=? , last_join=? WHERE nick=? ",[joins,clean_player,date])

						else:
							cur.execute("SELECT last_join FROM players ORDER BY last_join DESC LIMIT 1")
							last_join = cur.fetchone()
							irc.send("PRIVMSG #megaglest-lobby :Hi "+player+" , The last player online was seen at "+last_join[0]+" .\r\n")
							con.execute("INSERT INTO players VALUES(?,?,?)",[date,clean_player,1])
						
						con.commit()
		elif len(word) == 2:
			if word[0] == "PING":
				irc.send("PONG "+word[1][1:])
	time.sleep(1)
import discord
import random as r
import time as t
import sqlite3

message_crime = ["You robbed the Society of Schmoogaloo and ended up in a lake,but still managed to steal ",
"tu as volé une pomme qui vaut ", "tu as gangé le loto ! prends tes ", "j'ai plus d'idée prends ça "]
# 4 phrases
message_gamble = ["tu as remporté le pari ! tu obtiens ","Une grande victoire pour toi ! tu gagnes ",
"bravo prends ", "heu.... "]
# 4 phrases
# se sont les phrases prononcé par le bot pour plus de diversité
# il n'y en a pas bcp donc je les laisse directement dans le code
anti_spam = 6
anti_spam2 = 3
# nb de sec nécessaire entre 2 commandes

TOKEN = "********************************"
# ***********************************Bastion's Gems
# ***********************************Bot_RPG
#le token permet de reconnaitre mon bot

client = discord.Client()
@client.event
async def on_message(message):
	message.content = message.content.lower()
# on ne prend que la version miniscule du message
# pour l'instant chaque commande que le bot detecte commence par if message.con...

	data = sqlite3.connect('players.db')
	c = data.cursor()
	# on ouvre la base de donnée une fois au lancement du Bot
	if message.content.startswith('ba.begin'):
	#cette fonction initialise les données dans la bdd
		ID = message.author.id
		c.execute("""SELECT ID FROM donnees WHERE ID=?""", (ID,))
		rep = c.fetchone()
		print (rep)
		if rep != None :
			msg = "personnage déjà créé !"
		else :
			gem = 10
			time = t.time()-anti_spam
			c.execute("""INSERT INTO donnees VALUES(?,?,?)""",(ID,gem,time))
			# on injecte 3 données l'ID discord, le nombre de gems,et la date de
			# la dernière commande, qui permet de vérifier de faire mon anti spam
			c.execute("""INSERT INTO inventaire VALUES(?,?,?,?,?,?,?,?,?,?,?)""",(ID,0,0,0,0,0,0,0,0,0,0))
			data.commit()
			msg = "fiche personnage créé !"
		await client.send_message(message.channel, msg)

	if message.content.startswith('ba.crime'):
		ID = message.author.id
		c.execute("""SELECT time FROM donnees WHERE ID=?""", (ID,))
		time = c.fetchone()
		# on récupère le la date de la dernière commande
		if time[0] < t.time()-anti_spam:
		# si 10 sec c'est écoulé depuis alors on peut en  faire une nouvelle
			gain = r.randint(5,10)
			msg = message_crime[r.randint(0,3)]+str(gain)+":gem:"
			c.execute("""UPDATE donnees SET gem = gem + ? WHERE ID = ?""",(gain,ID))
			c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
		else:
			msg = "il faut attendre "+str(anti_spam)+" secondes entre chaque commande !"
		await client.send_message(message.channel, msg)
		data.commit()

	if message.content.startswith('ba.bal'):
		ID = message.author.id
		c.execute("""SELECT time FROM donnees WHERE ID=?""", (ID,))
		time = c.fetchone()
		if time[0] < t.time()-anti_spam2:
			c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
			c.execute("""SELECT gem FROM donnees WHERE ID=?""", (ID,))
			gem = c.fetchone()
			msg = "tu as actuellement : "+str(gem[0])+" :gem: !"
		else:
			msg = "il faut attendre "+str(anti_spam2)+" secondes entre chaque commande !"
		await client.send_message(message.channel, msg)
		data.commit()


	if message.content.startswith('ba.gamble'):
		valeur = int(message.content[10:])
		ID = message.author.id
		c.execute("""SELECT time FROM donnees WHERE ID=?""", (ID,))
		time = c.fetchone()
		if time[0] < t.time()-anti_spam:
			if r.randint(0,3) == 0:
				gain = valeur*3
				# l'espérence est de 0 sur la gamble
				msg = message_gamble[r.randint(0,3)]+str(gain)+":gem:"
				c.execute("""UPDATE donnees SET gem = gem + ? WHERE ID = ?""",(gain,ID))
			else:
				c.execute("""UPDATE donnees SET gem = gem - ? WHERE ID = ?""",(valeur,ID))
				msg = "dommage tu as perdu "+str(valeur)+":gem:"
			c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
		else:
			msg = "il faut attendre "+str(anti_spam)+" secondes entre chaque commande !"
		await client.send_message(message.channel, msg)
		data.commit()


	if message.content.startswith('ba.buy pickaxe'):
		ID = message.author.id
		c.execute("""UPDATE donnees SET gem = gem - ? WHERE ID = ?""",(20,ID))
		c.execute("""UPDATE inventaire SET pickaxe = pickaxe + ? WHERE ID = ?""",(1,ID))
		data.commit()
		await client.send_message(message.channel, "tu as désormais une pioche en plus !")

	if message.content.startswith('ba.mine'):
		ID = message.author.id
		c.execute("""SELECT time FROM donnees WHERE ID=?""", (ID,))
		time = c.fetchone()
		if time[0] < t.time()-anti_spam:
			c.execute("""SELECT pickaxe FROM inventaire WHERE ID=?""", (ID,))
			if c.fetchone()[0] >= 1:
				if r.randint(0,20)==0:
					c.execute("""UPDATE inventaire set pickaxe = pickaxe - ? WHERE ID=?""", (1,ID))
					msg = "pas de chance tu as cassé ta pioche !"
				else :
					if r.randint(0,8)==0:
						c.execute("""UPDATE inventaire set iron = iron + ? WHERE ID=?""", (1,ID))
						msg = "tu as obtenue un bloc de iron !"
					else:
						c.execute("""UPDATE inventaire set cobblestone = cobblestone + ? WHERE ID=?""", (r.randint(1,2),ID))
						msg = "tu as obtenue un bloc.s de cobblestone.s !"
			else:
				msg = "il faut acheter une pioche !"
			c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
		else:
			msg = "il faut attendre "+str(anti_spam)+" secondes entre chaque commande !"
		await client.send_message(message.channel, msg)
		data.commit()


	if message.content.startswith('ba.help'):
		msg = "**Bienvenue dans l'aide de Bastion's gems !** \n Il y a actuellement 6 commandes :\n\
		*-ba.begin* : permet de d'initialiser la base de donnée\n\
		*-ba.crime* : permet de récolter entre 5 et 10 :gem:\n\
		*-ba.bal* : permet de savoir combien on a dans son compte en banque !\n\
		*-ba.buy pickaxe* : j'ai vraiment besoin d'expliquer celle là ?\n\
		*-ba.mine* : en minant on récolte de la coble ou des minerais de iron (nécessite une pioche qui peut se briser)\n\
		*-ba.gamble* : on mise, on perd.. on peut aussi triplé sa mise !(pas encore de plafond )\nBientot de nouvelles fonctionnalités ! "
		await client.send_message(message.channel, msg)

	if message.content.startswith('ba.inv'):
		ID = message.author.id
		c.execute("""SELECT time FROM donnees WHERE ID=?""", (ID,))
		time = c.fetchone()
		if time[0] < t.time()-anti_spam2:
			c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
			c.execute("""SELECT pickaxe,cobblestone,iron,gold,diamond FROM inventaire WHERE ID=?""", (ID,))
			inv = c.fetchone()
			print (inv)
			msg = "**ton inventaire**\n```-pickaxe.s : "+str(inv[0])+"\n-cobblestone.s : "+str(inv[1])+"\n-iron.s : "+str(inv[2])+"\n-gold: "+str(inv[3])+"\n-diamond : "+str(inv[4])+"```"
		else:
			msg = "il faut attendre "+str(anti_spam2)+" secondes entre chaque commande !"
		await client.send_message(message.channel, msg)
		data.commit()


	if message.content.startswith('ba.sell'):
		i = 0
		content = message.content[8:]
		while content[i] != " ":
			i += 1
		item = content[:i]
		nb = content[i+1:]
		mult = 0
		print(item,nb)
		if item == "cobblestone":
			mult = 1
		elif item =="iron":
			mult = 10
		elif item =="gold":
			mult = 25
		elif item =="diamond":
			mult = 50
		else:
			mult = 0
		gain = int(nb)*mult
		msg = "tu veux vendre "+nb+" "+item+" pour "+str(gain)+":gem:"
		await client.send_message(message.channel, msg)

	if message.content.startswith('ba.rebdd') and message.author.id == 141883318915301376 :
		data.commit()
		data.close()
		data = sqlite3.connect('players.db')
		c = data.cursor()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user)
	print(client.user.id)
	print('------')

client.run(TOKEN)

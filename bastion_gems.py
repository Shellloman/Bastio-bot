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
anti_spam = 10
# nb de sec nécessaire entre 2 commandes

TOKEN = "NjAzMjA4ODQxNDEyNDc2OTI5.XTcE5A.LhrQtshs6LFGKGB1dlGhGKpp_HY"
#le token permet de reconnaitre mon bot

client = discord.Client()
@client.event
async def on_message(message):

# pour l'instant chaque commande que le bot detecte commence par if message.con...

	if message.content.startswith('ba.begin') or message.content.startswith('Ba.begin'):
	#cette fonction initialise les données dans la bdd
		ID = message.author.id
		data = sqlite3.connect('spameurs.db')
		c = data.cursor()
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
			data.close()
			msg = "fiche personnage créé !"
		await client.send_message(message.channel, msg)

	if message.content.startswith('ba.crime') or message.content.startswith('Ba.crime'):
		ID = message.author.id
		data = sqlite3.connect('spameurs.db')
		c = data.cursor()
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
			msg = "il faut attendre 10 secondes entre chaque commande !"
		await client.send_message(message.channel, msg)
		data.commit()
		data.close()

	if message.content.startswith('ba.bal') or message.content.startswith('Ba.bal'):
		ID = message.author.id
		data = sqlite3.connect('spameurs.db')
		c = data.cursor()
		c.execute("""SELECT time FROM donnees WHERE ID=?""", (ID,))
		time = c.fetchone()
		if time[0] < t.time()-5:
			c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
			c.execute("""SELECT gem FROM donnees WHERE ID=?""", (ID,))
			gem = c.fetchone()
			msg = "tu as actuellement : "+str(gem[0])+" :gem: !"
		else:
			msg = "il faut attendre 5 secondes entre chaque commande !"
		await client.send_message(message.channel, msg)
		data.commit()
		data.close()

	if message.content.startswith('ba.gamble') or message.content.startswith('Ba.gamble'):
		valeur = int(message.content[10:])
		ID = message.author.id
		data = sqlite3.connect('spameurs.db')
		c = data.cursor()
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
			msg = "il faut attendre 10 secondes entre chaque commande !"
		await client.send_message(message.channel, msg)
		data.commit()
		data.close()

	if message.content.startswith('ba.buy pickaxe') or message.content.startswith('Ba.buy pickaxe'):
		ID = message.author.id
		data = sqlite3.connect('spameurs.db')
		c = data.cursor()
		c.execute("""UPDATE donnees SET gem = gem - ? WHERE ID = ?""",(20,ID))
		c.execute("""UPDATE inventaire SET pickaxe = pickaxe + ? WHERE ID = ?""",(1,ID))
		data.commit()
		data.close()
		await client.send_message(message.channel, "tu as désormais une pioche en plus !")

	if message.content.startswith('ba.mine') or message.content.startswith('Ba.mine'):
		ID = message.author.id
		data = sqlite3.connect('spameurs.db')
		c = data.cursor()
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
						c.execute("""UPDATE inventaire set fer = fer + ? WHERE ID=?""", (1,ID))
						msg = "tu as obtenue un bloc de fer !"
					else:
						c.execute("""UPDATE inventaire set cobblestone = cobblestone + ? WHERE ID=?""", (r.randint(1,2),ID))
						msg = "tu as obtenue un bloc.s de cobblestone.s !"
			else:
				msg = "il faut acheter une pioche !"
			c.execute("""UPDATE donnees SET time = ? WHERE ID = ?""",(t.time(),ID))
		else:
			msg = "il faut attendre 10 secondes entre chaque commande !"
		await client.send_message(message.channel, msg)
		data.commit()
		data.close()

	if message.content.startswith('ba.help') or message.content.startswith('Ba.help'):
		msg = "**Bienvenue dans l'aide de Bastion's gems !** \n Il y a actuellement 6 commandes :\n\
		*-ba.begin* : permet de d'initialiser la base de donnée\n\
		*-ba.crime* : permet de récolter entre 5 et 10 :gem:\n\
		*-ba.bal* : permet de savoir combien on a dans son compte en banque !\n\
		*-ba.buy pickaxe* : j'ai vraiment besoin d'expliquer celle là ?\n\
		*-ba.mine* : en minant on récolte de la coble ou des minerais de fer (nécessite une pioche qui peut se briser)\n\
		*-ba.gamble* : on mise, on perd.. on peut aussi triplé sa mise !(pas encore de plafond )\nBientot de nouvelles fonctionnalités ! "
		await client.send_message(message.channel, msg)

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user)
	print(client.user.id)
	print('------')

client.run(TOKEN)

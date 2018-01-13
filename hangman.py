'''
	File name: 		hangman.py
	Author:			Michal Filipowicz
	Nr indeksu:		226393
	Date created:	13-01-2018
	PLEASE CHECK README.md
'''
import argparse
import random
import sys
import os

#CLEAR SCREEN
os.system('cls' if os.name=='nt' else 'clear')

#GLOBAL VARS
difficulty_level = 0	# sets difficulty level: 1 - easy | 2 - medium | 3 - insane | -1 - own file
game_state = 0			# checks game state: 0 - game in progress | 1 - win | -1 - loose
mistakes = 0			# how many mistakes user did
correct = 0				# how many correct answers
user_inputs = []		# as its called..

#OPEN FILE AND SAVE WORDS FUNCTION
def readWords(diff, filename="words.txt"):
	if os.path.isfile(filename):
		with open(filename, 'r') as file:
			data = file.read().splitlines()		# it's not readlines() because we don't want \n symbol at the end
		wordslist = []							# list of saved words
		for line in data:
			if not len(line)<1:					# minimal length of word is 1
				if diff == -1:					# all words from user's file
					wordslist.append(line.lower())
				elif len(line.split()) == diff:	# wordslist depends on difficulty level
					wordslist.append(line.lower())
		return wordslist
	else:
		os.system('cls' if os.name=='nt' else 'clear')
		print("PROBLEM WITH READING FILE.")
		exit()

#PRINT UNDERSCORES
def printWord(word, inputs):
	for v in range(len(word)):
		typed = False
		for i in range(len(inputs)):
			if ord(word[v]) == ord(inputs[i].lower()):
				sys.stdout.write(inputs[i]+' ')
				typed = True
				continue
		if typed:
			continue
		if 97 <= ord(word[v]) <= 122:
			sys.stdout.write('_ ')
		elif word[v] == " ":
			sys.stdout.write('	')
		else:
			os.system('cls' if os.name=='nt' else 'clear')
			print("ERROR IN WORDS LIST FILE. ONLY ALPHABETICAL CHARS AND SPACES ARE ALLOWED!")
			exit()

#PRINT HANGMAN (KINDA BRUTE FORCE.. BUT IT WORKS)
#MAX MISTAKES = 6
def printHangman(progress):
	if progress == 0:
		print("""
    ---------
    |       |
    |
    |
    |
    |
    |
____|____
|       |""")
	if progress == 1:
		print("""
    ---------
    |       |
    |       O
    |
    |
    |
    |
____|____
|       |""")
	if progress == 2:
		print("""
    ---------
    |       |
    |       O
    |       |
    |       |
    |
    |
____|____
|       |""")
	if progress == 3:
		print("""
    ---------
    |       |
    |       O
    |       |
    |       |
    |      /
    |
____|____
|       |""")
	if progress == 4:
		print("""
    ---------
    |       |
    |       O
    |       |
    |       |
    |      / \\
    |
____|____
|       |""")
	if progress == 5:
		print("""
    ---------
    |       |
    |       O
    |      \|
    |       |
    |      / \\
    |
____|____
|       |""")
	if progress == 6:
		print("""
    ---------
    |       |
    |       O
    |      \|/
    |       |
    |      / \\
    |
____|____
|       |""")


#HANDLING ARGUMENTS
parser = argparse.ArgumentParser(description='Hangman game in PYTHON. Choose difficulty level.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-e', '--easy', help='Select easy mode', action='store_true')
group.add_argument('-m', '--medium', help='Select medium mode', action='store_true')
group.add_argument('-i', '--insane', help='Select insane mode', action='store_true')
group.add_argument('-o', '--open', help='Choose your own words file', action='store', dest='file')
parser.add_argument('-c', '--cheat', help='CHEAT MODE', action='store_true')
args = parser.parse_args()

if len(sys.argv) == 1:
	parser.print_help()
	exit()
if args.easy:
	difficulty_level = 1
	words = readWords(difficulty_level)
elif args.medium:
	difficulty_level = 2
	words = readWords(difficulty_level)
elif args.insane:
	difficulty_level = 3
	words = readWords(difficulty_level)
else:
	difficulty_level = -1
	words = readWords(difficulty_level, args.file)


game_word = random.choice(words)
while game_state == 0:
	print("HANGMAN BY MICHAL FILIPOWICZ")
	print("DIFFICULTY: %s" % (difficulty_level))
	print("1 - EASY | 2 - MEDIUM | 3 - INSANE | -1 - OWN FILE")
	printHangman(mistakes)
	print("\nWORD TO GUESS:")
	if args.cheat:
		print("Word you looking for: %s" % (game_word))
		print("Characters to guess: %s" % (len(game_word)-game_word.count(' ')))
		print("Correct characters: %s" % (correct))
	printWord(game_word, user_inputs)

	user_input = raw_input("\nEnter character and press ENTER: ")
	if user_input and user_input not in user_inputs:
		if len(user_input) == 1:
			user_inputs.append(user_input)
			if user_input not in game_word:
				mistakes+=1
			if game_word.count(user_input) >= 0:
				correct+=game_word.count(user_input)	
		
	printHangman(mistakes)
	if mistakes >= 6:
		game_state = -1
	if correct >= len(game_word)-game_word.count(' '):
		game_state = 1
	os.system('cls' if os.name=='nt' else 'clear')

if game_state == -1 and args.cheat:
	print("""
  ____    _____      _      _       _      __   __  ___ 
 |  _ \  | ____|    / \    | |     | |     \ \ / / |__ \\
 | |_) | |  _|     / _ \   | |     | |      \ V /    / /
 |  _ <  | |___   / ___ \  | |___  | |___    | |    |_| 
 |_| \_\ |_____| /_/   \_\ |_____| |_____|   |_|    (_) 
                                                        """)
	print("Correct answer...: %s" % (game_word))
	exit()

if game_state == -1:
	print("""
  _____   ____   __   __    _   _   _____  __  __  _____     _____   ___   __  __   _____ 
 |_   _| |  _ \  \ \ / /   | \ | | | ____| \ \/ / |_   _|   |_   _| |_ _| |  \/  | | ____|
   | |   | |_) |  \ V /    |  \| | |  _|    \  /    | |       | |    | |  | |\/| | |  _|  
   | |   |  _ <    | |     | |\  | | |___   /  \    | |       | |    | |  | |  | | | |___ 
   |_|   |_| \_\   |_|     |_| \_| |_____| /_/\_\   |_|       |_|   |___| |_|  |_| |_____|
                                                                                          """)
	print("Correct answer: %s" % (game_word))
	exit()

if game_state == 1 and args.cheat:
	print("""
  _   _     ____     __        __  _____      _      _  __    
 | | | |   |  _ \    \ \      / / | ____|    / \    | |/ /    
 | | | |   | |_) |    \ \ /\ / /  |  _|     / _ \   | ' /     
 | |_| |   |  _ <      \ V  V /   | |___   / ___ \  | . \   _ 
  \___/    |_| \_\      \_/\_/    |_____| /_/   \_\ |_|\_\ ( )
                                                           |/ 
   ____   _   _   _____      _      _____   _____   ____  
  / ___| | | | | | ____|    / \    |_   _| | ____| |  _ \ 
 | |     | |_| | |  _|     / _ \     | |   |  _|   | |_) |
 | |___  |  _  | | |___   / ___ \    | |   | |___  |  _ < 
  \____| |_| |_| |_____| /_/   \_\   |_|   |_____| |_| \_\\
                                                          """)
	exit()

if game_state == 1:
	print("""
 __        __  ___   _   _   _   _   _____   ____  
 \ \      / / |_ _| | \ | | | \ | | | ____| |  _ \ 
  \ \ /\ / /   | |  |  \| | |  \| | |  _|   | |_) |
   \ V  V /    | |  | |\  | | |\  | | |___  |  _ < 
    \_/\_/    |___| |_| \_| |_| \_| |_____| |_| \_\                                                   
 __        __  ___   _   _   _   _   _____   ____  
 \ \      / / |_ _| | \ | | | \ | | | ____| |  _ \ 
  \ \ /\ / /   | |  |  \| | |  \| | |  _|   | |_) |
   \ V  V /    | |  | |\  | | |\  | | |___  |  _ < 
    \_/\_/    |___| |_| \_| |_| \_| |_____| |_| \_\                                                   
   ____   _   _   ___    ____   _  __  _____   _   _ 
  / ___| | | | | |_ _|  / ___| | |/ / | ____| | \ | |
 | |     | |_| |  | |  | |     | ' /  |  _|   |  \| |
 | |___  |  _  |  | |  | |___  | . \  | |___  | |\  |
  \____| |_| |_| |___|  \____| |_|\_\ |_____| |_| \_|
  ____    ___   _   _   _   _   _____   ____  
 |  _ \  |_ _| | \ | | | \ | | | ____| |  _ \ 
 | | | |  | |  |  \| | |  \| | |  _|   | |_) |
 | |_| |  | |  | |\  | | |\  | | |___  |  _ < 
 |____/  |___| |_| \_| |_| \_| |_____| |_| \_\\
                                              """)
	exit()
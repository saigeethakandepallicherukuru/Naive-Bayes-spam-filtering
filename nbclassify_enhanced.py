#Classifies a file to either spam or ham by reading parameters from nbmodel.txt

import sys
import os
import json
from decimal import Decimal, getcontext
import ast
def main():
	STOPWORDS = ['a','able','about','across','after','all','almost','also','am','among',
   				'an','and','any','are','as','at','be','because','been','but','by','can',
             	'cannot','could','dear','did','do','does','either','else','ever','every',
             	'for','from','get','got','had','has','have','he','her','hers','him','his',
             	'how','however','i','if','in','into','is','it','its','just','least','let',
             	'like','likely','may','me','might','most','must','my','neither','no','nor',
           		'not','of','off','often','on','only','or','other','our','own','rather','said',
             	'say','says','she','should','since','so','some','than','that','the','their',
             	'them','then','there','these','they','this','tis','to','too','twas','us',
             	'wants','was','we','were','what','when','where','which','while','who',
             	'whom','why','will','with','would','yet','you','your']

	getcontext().prec = 4
	input_dir_path=sys.argv[1]
	ham_dict, spam_dict, prob_class, vocab = {}, {}, {}, {}
	prob_ham_class, prob_spam_class = 1, 1
	num_spam_classified, num_ham_classified = 0, 0
	num_spam_correct, num_ham_correct = 0, 0
	total_spam_files, total_ham_files = 0, 0
	output_file="nboutput.txt"
	fp_w=open(output_file,'w')
	with open("nbmodel.txt","r", encoding="latin1") as fp:
		contents=fp.read()
		ham_dict, spam_dict, prob_class, vocab = contents.split("; ")
		ham_dict, spam_dict, prob_class, vocab = ast.literal_eval(ham_dict), ast.literal_eval(spam_dict), ast.literal_eval(prob_class), ast.literal_eval(vocab)
	
	for root, subdirs, files in os.walk(input_dir_path):
		#print('--root'+root)
		#print('--subdir'+str(subdirs))
		#print('--files'+str(files))
		for file in files:
			if(not file.startswith('.')):
				# count total number of ham and spam files
				if('spam' in file):
					total_spam_files += 1
				if('ham' in file):
					total_ham_files += 1

				fp=open(root+str('/'+file), "r", encoding="latin1")
				prob_ham_class, prob_spam_class = 1, 1
				for line in fp.readlines():
					words=line.split(" ")
					for word in words:
						word = word.rstrip()
						if(len(word) != 0 and word not in STOPWORDS):
							#Add-k smoothing and eliminating stop words
							vocabulary = Decimal(1/vocab.get("vocab"))
							prob_ham_class = Decimal(prob_ham_class) * Decimal((((ham_dict.get(word) if(ham_dict.get(word)) else 0)+(5*vocabulary))) / Decimal((vocab.get("ham_token_count")+5)))
							prob_spam_class = Decimal(prob_spam_class) * Decimal((((spam_dict.get(word) if(spam_dict.get(word)) else 0)+(5*vocabulary))) / Decimal((vocab.get("spam_token_count")+5)))
				prob_ham_class = Decimal(prob_ham_class) * Decimal(prob_class.get("P(ham)"))
				prob_spam_class = Decimal(prob_spam_class) * Decimal(prob_class.get("P(spam)"))
				#print(prob_ham_class)
				#print(prob_spam_class)
				if(prob_ham_class > prob_spam_class):
					fp_w.write("ham "+root+str('/'+file))
					fp_w.write("\n")
					num_ham_classified += 1
					if('ham' in file):
						num_ham_correct += 1
				else:
					fp_w.write("spam "+root+str('/'+file))
					fp_w.write("\n")
					num_spam_classified += 1
					if('spam' in file):
						num_spam_correct += 1
'''	if(num_spam_classified != 0 and total_spam_files != 0):
		spam_precision = (num_spam_correct) / (num_spam_classified)
		spam_recall = (num_spam_correct) / (total_spam_files)
		spam_f1_score = (2*spam_precision*spam_recall) / (spam_precision+spam_recall)
		print("spam precision: {0:.2f}".format(spam_precision))
		print("spam recall: {0:.2f}".format(spam_recall))
		print("spam f1 score: {0:.2f}".format(spam_f1_score))
	if(num_ham_classified != 0 and total_ham_files != 0):	
		ham_precision = (num_ham_correct) / num_ham_classified
		ham_recall = (num_ham_correct) / (total_ham_files)
		ham_f1_score = (2*ham_precision*ham_recall) / (ham_precision+ham_recall)
		print("ham precision: {0:.2f}".format(ham_precision))
		print("ham recall: {0:.2f}".format(ham_recall))
		print("ham f1 score: {0:.2f}".format(ham_f1_score)) '''
main()
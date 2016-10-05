#To learn a naive Bayes model from training data and write the model parameters to nbmodel.txt

import sys
import os
import json

def main():
	input_dir_path=sys.argv[1]
	output_file="nbmodel.txt"
	fp_w=open(output_file,'w')
	num_ham_files, num_spam_files = 0, 0
	ham_dict, spam_dict = {}, {}
	ham_token_count, spam_token_count = 0, 0
	vocab = []
	for root, subdirs, files in os.walk(input_dir_path):
		#print('--root'+root)
		#print('--subdir'+str(subdirs))
		#print('--files'+str(files))
		if('/ham' in root):
			for file in files:
				if(not file.startswith('.')):
					num_ham_files += 1
					fp=open(root+str('/'+file), "r", encoding="latin1")
					for line in fp.readlines():
						words=line.split()
						vocab += words
						for word in words:
							if(word in ham_dict):
								ham_dict[word] += 1
							else:
								ham_dict[word] = 1
							ham_token_count += 1
					fp.close()
		if('/spam' in root):
			for file in files:
				if(not file.startswith('.')):
					num_spam_files += 1
					fp=open(root+str('/'+file), "r", encoding="latin1")
					for line in fp.readlines():
						words=line.split()
						vocab += words
						for word in words:
							if(word in spam_dict):
								spam_dict[word] += 1
							else:
								spam_dict[word] = 1
							spam_token_count += 1
					fp.close()
	#print("Total number of ham files: {}".format(num_ham_files))
	#print("Total number of spam files: {}".format(num_spam_files))

	#Writing the model parameters to model file
	prob_class = {"P(ham)": (num_ham_files/(num_ham_files+num_spam_files)), "P(spam)": (num_spam_files/(num_ham_files+num_spam_files))}
	vocab = {"vocab": len(set(vocab)), "ham_token_count": ham_token_count, "spam_token_count": spam_token_count}
	json.dump(ham_dict,fp_w)
	fp_w.write("; ")
	json.dump(spam_dict,fp_w)
	fp_w.write("; ")
	json.dump(prob_class,fp_w)
	fp_w.write("; ")
	json.dump(vocab,fp_w)

	#fp_w.write("probability of ham class P(ham): {}".format(num_ham_files/(num_ham_files+num_spam_files)))
	#fp_w.write("\nprobability of spam class P(spam): {} \n".format(num_spam_files/(num_ham_files+num_spam_files)))
	fp_w.close()

main()
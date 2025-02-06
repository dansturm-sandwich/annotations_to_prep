import os
import argparse
import re
import shutil
import sys


def copyPlates(annoPath, outboxPath):
	# Check if the folder exists
	if os.path.isdir(annoPath):
		# Loop through each file in the folder
		for anno_name in os.listdir(annoPath):
			file_path = os.path.join(annoPath, anno_name)
			# Check if it's a file (not a folder)
			if os.path.isfile(file_path):
				plateName = os.path.basename(file_path[:-20])
				print(f"Processing: {plateName}")
				match = re.match(r"^.+\d{4,}", plateName)
				shotName = match.group(0) if match else plateName
				shotSeries = f'{shotName[:-3]}000'
				shotFolder = f'{file_path.split("online/", 1)[0]}online/{shotSeries}/{shotName}/plates'
				if "log" in plateName:
					platePath = f'{shotFolder}/log/{plateName}.mov'
				elif "cc" in plateName:
					platePath = f'{shotFolder}/cc/{plateName}.mov'
				else:
					print('Error')
				outboxAnno = f'{outboxPath}/annotations'
				outboxPlate = f'{outboxPath}/plates'
				os.makedirs(outboxAnno, exist_ok=True)
				os.makedirs(outboxPlate, exist_ok=True)
				shutil.copy2(file_path, os.path.join(outboxAnno, os.path.basename(file_path)))
				shutil.copy2(platePath, os.path.join(outboxPlate, os.path.basename(platePath)))

	else:
		print("Error. Not a folder.")




def _arg_handler(args):
	print(f'Path to annotations: {args.annopath}')
	print(f'Path to outbox: {args.outboxpath}')

	result = copyPlates(
		annoPath=args.annopath,
		outboxPath=args.outboxpath,
	)

	if result is False:
		print('Error, unable to process args.')
		sys.exit(1)

	print('Done')
	sys.exit(0)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Takes path to footage to create a read node')

	parser.add_argument('-annopath', required=True)
	parser.add_argument('-outboxpath', required=True)
	parser.set_defaults(func=_arg_handler)

	parsed_args = parser.parse_args()
	parsed_args.func(parsed_args)
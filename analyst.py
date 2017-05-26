#!python3
#-*- conding:utf-8 -*-
import pandas as pd
import pymongo
from config import *

client = pymongo.MongoClient(Mongo_URL)
db = client[Mongo_DB]

def create_brief_table():
	items = db[Mongo_TABLE].find()
	df = None
	for item in items:
		if df is None:
			df = pd.DataFrame(item,index=[1])
		else:
			tmp = pd.DataFrame(item,index=[1])
			df = pd.concat([df,tmp],ignore_index=True)
	del df['_id']
	return df.drop_duplicates()

def main():
	df = create_brief_table()
	print(df)

if __name__ == '__main__':
	main()

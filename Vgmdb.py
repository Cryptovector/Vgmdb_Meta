import html
import requests
import shutil
import argparse
import os
import music_tag
from lxml import html

S_path = '/html/body/div[4]/table/tr[1]/td[1]/div/'
S_path_2 = S_path + 'div[2]/div[2]/div/div[1]/table'
S_path_3 = S_path + 'div[3]/div/div/table'
S_path_4 = S_path + 'div[4]/div[2]/div/span[1]/table'

def Show_Album_data(tree):
	print("")
	print("Found Album: ")
	print("")
	print("Album Info")
	for i in range(0, len(tree.xpath(S_path_2+'/tr'))):
		print(tree.xpath(S_path_2+'/tr['+str(i+1)+']/td[2]')[0].text_content().replace('\n','').replace('\r',''))
				
	print("")	
	print("Track Titles")
	for i in range(0, len(tree.xpath(S_path_4))):
		print("CD " + str(i+1) + ":")
		for y in range(0, len(tree.xpath(S_path_4+'['+str(i+1)+']')[0])):
			Title_names = tree.xpath(S_path_4+'['+str(i+1)+']/tr['+str(y+1)+']/td[2]')[0].text_content().replace('\n','').replace('\r','')
			print(Title_names.replace('\n', ''))	

def Meta_rename(tree, Path, CD_Number, Metainfo, Art):
	Files = next(os.walk(Path))[2] 		
	if len(Files) == len(tree.xpath(S_path_4+'['+str(CD_Number)+']')[0]):

		if Art:
			Cover_image = None
			Img_url = tree.xpath(S_path+'div[2]/div[1]/div/table/tr/td/div')[0].get('style')[23:-2]
			response = requests.get(Img_url, stream=True)
			response.raw.decode_content = True
			Cover_image = response.raw.read()
		if Metainfo:
			Metainfo_list = {}
			for i in range(0, len(tree.xpath(S_path_2)[0])):
				Metainfo_list[tree.xpath(S_path_2+'/tr['+str(i+1)+']/td[1]')[0].text_content()] = tree.xpath(S_path_2+'/tr['+str(i+1)+']/td[2]')[0].text_content().replace('\n','').replace('\r','')
	
			for i in range(0, len(tree.xpath(S_path_3+'/tbody/tr'))):
				Metainfo_list[tree.xpath(S_path_3+'/tbody/tr['+str(i+1)+']/td[1]/span/b/span[1]')[0].text_content()] = tree.xpath(S_path_3+'/tbody/tr['+str(i+1)+']/td[2]')[0].text_content()

		for i in range(0, len(Files)):
			Title_name = tree.xpath(S_path_4+'['+str(CD_Number)+']/tr['+str(i+1)+']/td[2]')[0].text_content().replace('\n','').replace('\r','')

			if Art or Metainfo:
				Music_File = music_tag.load_file(Path+'\\'+Files[i])
				if Metainfo:
					Music_File['tracktitle'] = Title_name
					Music_File['tracknumber'] = str(i+1)
					Music_File['totaltracks'] = str(len(Files))
					Music_File['totaldiscs'] = str(len(tree.xpath(S_path_4)))
					Music_File['discnumber'] = str(CD_Number)
					Music_File['album'] = tree.xpath(S_path+'h1/span[1]')[0].text_content()
					try:
						Music_File['genre'] = Metainfo_list['Classification']
					except:
						pass
					try:
						Music_File['year'] = Metainfo_list['Release Date'].split(', ')[1]
					except:
						pass
					try:
						Music_File['composer'] = Metainfo_list['Composer']
					except:
						pass
				if Art:
					Music_File['artwork'] = Cover_image
					Music_File['artwork'].first.thumbnail([64, 64])

				Music_File.save()
			os.rename(Path+'\\'+Files[i], Path+'\\'+Title_name+'.'+Files[i].split('.')[1])
	else:
		raise Exception("The number of tracks and files does not match")			

def Check_Database(ID, Path, CD_Number, Search, Metainfo, Art):
	try:
		response = requests.get('https://vgmdb.net/search?q='+ID, stream=True)
		if response.status_code == 200:
			tree = html.fromstring(response.content)

			if Search:
				Show_Album_data(tree)
			else:	
				CD_Count = len(tree.xpath(S_path_4))
				if CD_Count > 1:
					if CD_Number != None:
						Meta_rename(tree, Path, CD_Number, Metainfo, Art)
					else:
						raise Exception("You have to specify which CD metadata should be used")	
				else:
					if CD_Count:
						Meta_rename(tree, Path, 1, Metainfo, Art)
					else:
						raise Exception("No CD information in Database")								
		else:
			raise Exception("Wrong status_code could not reach site " + str(response.status_code)) 	
	except Exception as e:
		print("Could not Download Data from Database Exception: " + str(e))


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='VGMDB Rename & Update')
	parser.add_argument('-AA','--Album_Art', action='store_true')
	parser.add_argument('-M','--Meta_Info', action='store_true')
	parser.add_argument('-S','--Search', action='store_true')
	parser.add_argument('-ID', '--ID',
	action="store", dest="ID",
	help="Catalog Number or Barcode", default=None)
	parser.add_argument('-D', '--destination',
	action="store", dest="destination",
	help="Path for Tracks", default=None)
	parser.add_argument('-CD','--CD_Number', 
	action="store", dest="CD",
	help="CD Number", default=None)
	args = parser.parse_args()

	if args.ID != None:
		if args.Search:
			Check_Database(args.ID, args.destination, args.CD, args.Search, args.Meta_Info, args.Album_Art)
		else:	
			if args.destination != None:
				Check_Database(args.ID, args.destination, args.CD, args.Search, args.Meta_Info, args.Album_Art)
			else:
				print("You must specify a Filepath with your (Ripped) CD Tracks")
	else:
		print("You must specify a Catalog Number or Barcode")

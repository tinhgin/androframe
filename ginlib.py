import zipfile
import os.path
#import getpass
from subprocess import call
from time import gmtime, strftime
from sdat2img import d2i

def sin(rom):
	print 'Please wait...\nGetting system.sin from ROM...'
	foldersin = 'system.sin' + rom.replace('/','.')
	if os.path.exists(foldersin):
		os.system('rm -rf ' + foldersin)
	with zipfile.ZipFile(rom,"r") as zip_ref:
		zip_ref.extract('system.sin', foldersin)
	print 'GET system.sin SUCCESSFULLY.\nGetting system.ext4 from system.sin...'
	os.system('java -jar sin2ext4.jar ' + foldersin + '/system.sin')

	print 'GET system.ext4 SUCCESSFULLY.'
	print 'Mounting system.ext4...'
	tmp = 'system' + rom.replace('/','.')
	if os.path.exists(tmp):
		os.system('rm -rf ' + tmp)
	os.makedirs(tmp)
	os.system('sudo mount -t ext4 -o loop ' + foldersin + '/system.ext4 ./' + tmp)
	print 'MOUNT system.ext4 SUCCESSFULLY.\nGetting /system/framework...'
	output = 'framework_' + strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	os.makedirs(output)
	tmp1 = 'cp -r ' + tmp + '/framework/* ' + output
	os.system(tmp1)
	print 'GET /system/framework SUCCESSFULLY.'
	call(["sudo", "umount", tmp])
	os.system('rm -rf ' + tmp)
	os.system('rm -rf ' + foldersin)
	return output



def dat(rom):
	print 'Please wait...\nGetting system.transfer.list and system.new.dat from ROM...'
	folderdat = 'system.dat' + rom.replace('/','.')
	if os.path.exists(folderdat):
		os.system('rm -rf ' + folderdat)
	with zipfile.ZipFile(rom,"r") as zip_ref:
		zip_ref.extract('system.new.dat', folderdat)
		zip_ref.extract('system.transfer.list', folderdat)
	print 'GET system.transfer.list AND system.new.dat SUCCESSFULLY.\nGetting system.img...'
	#call(["python", "./sdat2img.py", folderdat + "/system.transfer.list", folderdat + "/system.new.dat", folderdat + "/system.img"])
	d2i(['',folderdat + "/system.transfer.list",folderdat + "/system.new.dat",folderdat + "/system.img"])
	print 'GET system.img SUCCESSFULLY.'
	print 'Mounting system.img...'
	tmp = 'system' + rom.replace('/','.')
	if os.path.exists(tmp):
		os.system('rm -rf ' + tmp)
	os.makedirs(tmp)
	os.system('sudo mount -o loop ' + folderdat + '/system.img ' + tmp)
	print 'MOUNT system.img SUCCESSFULLY.\nGetting /system/framework...'
	output = 'framework_' + strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	os.makedirs(output)
	tmp1 = 'cp -r ' + tmp + '/framework/* ' + output
	os.system(tmp1)
	print 'GET /system/framework SUCCESSFULLY.'
	call(["sudo", "umount", tmp])
	os.system('rm -rf ' + folderdat)
	os.system('rm -rf ' + tmp)
	return output

def raw(rom):
	print 'Please wait...\nExtracting ROM...'
	folderraw = 'system.raw' + rom.replace('/','.')
	if os.path.exists(folderraw):
		os.system('rm -rf ' + folderraw)
	tmp = 'ROM' + rom.replace('/','.')
	with zipfile.ZipFile(rom,"r") as zip_ref:
		zip_ref.extractall("./" + tmp)
	print 'EXTRACT ROM SUCCESSFULLY.\nGetting /system/framework...'
	output = 'framework_' + strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	os.makedirs(output)
	tmp1 = 'cp -r ' + tmp + '/system/framework/* ' + output
	os.system(tmp1)
	print 'GET /system/framework SUCCESSFULLY.'
	os.system('rm -rf ' + tmp)
	return output

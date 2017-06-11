import zipfile
import os.path
import shutil
from subprocess import call
#from time import gmtime, strftime
import sys
sys.path.append("./Tool")
from sdat2img import d2i
import sys

def sinlinux(rom):
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
	#output = 'framework_' + strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	output = 'framework_' + rom
	os.makedirs(output)
	tmp1 = 'cp -r ' + tmp + '/framework/* ' + output
	os.system(tmp1)
	print 'GET /system/framework SUCCESSFULLY.'
	call(["sudo", "umount", tmp])
	os.system('rm -rf ' + tmp)
	os.system('rm -rf ' + foldersin)
	return output

def sinwindows(rom):
	print 'Please wait...\nGetting system.sin from ROM...'
	foldersin = 'system.sin' + rom.replace('/','.')
	with zipfile.ZipFile(rom,"r") as zip_ref:
		zip_ref.extract('system.sin', foldersin)
	print 'GET system.sin SUCCESSFULLY.\nGetting system.ext4 from system.sin...'
	os.system('java -jar "Tool/sin2ext4.jar" ' + foldersin + '/system.sin')
	print 'GET system.ext4 SUCCESSFULLY.'
	print 'Extracting system.ext4...'
	tmp = 'system' + rom.replace('/','.')
	os.makedirs(tmp)
	os.chdir("Tool")
	os.system('ImgExtractor.exe ../' + foldersin + '/system.ext4 ../' + tmp)
	os.chdir("..")
	print 'EXTRACT system.ext4 SUCCESSFULLY.\nGetting /system/framework...'
	#output = 'framework_' + strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	output = 'Result/framework_' + rom
	os.makedirs(output)
	os.system('copy "' + tmp + '/framework" "' + output + '"')
	print 'GET /system/framework SUCCESSFULLY.'
	shutil.rmtree(tmp)
	shutil.rmtree(foldersin)
	return 'framework_' + rom

def sin(rom):
	if sys.platform == "linux" or sys.platform == "linux2":
		return sinlinux(rom)
	elif sys.platform == "win32":
		return sinwindows(rom)


def datlinux(rom):
	print 'Please wait...\nGetting system.transfer.list and system.new.dat from ROM...'
	folderdat = 'system.dat' + rom.replace('/','.')
	if os.path.exists(folderdat):
		os.system('rm -rf ' + folderdat)
	with zipfile.ZipFile(rom,"r") as zip_ref:
		zip_ref.extract('system.new.dat', folderdat)
		zip_ref.extract('system.transfer.list', folderdat)
	print 'GET system.transfer.list AND system.new.dat SUCCESSFULLY.\nGetting system.img...'
	d2i(['',folderdat + "/system.transfer.list",folderdat + "/system.new.dat",folderdat + "/system.img"])
	print 'GET system.img SUCCESSFULLY.'
	print 'Mounting system.img...'
	tmp = 'system' + rom.replace('/','.')
	if os.path.exists(tmp):
		os.system('rm -rf ' + tmp)
	os.makedirs(tmp)
	os.system('sudo mount -o loop ' + folderdat + '/system.img ' + tmp)
	print 'MOUNT system.img SUCCESSFULLY.\nGetting /system/framework...'
	#output = 'framework_' + strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	output = 'framework_' + rom
	os.makedirs(output)
	tmp1 = 'cp -r ' + tmp + '/framework/* ' + output
	os.system(tmp1)
	print 'GET /system/framework SUCCESSFULLY.'
	call(["sudo", "umount", tmp])
	os.system('rm -rf ' + folderdat)
	os.system('rm -rf ' + tmp)
	return output


def datwindows(rom):
	print 'Please wait...\nGetting system.transfer.list and system.new.dat from ROM...'
	folderdat = 'system.dat' + rom.replace('/','.')
	with zipfile.ZipFile(rom,"r") as zip_ref:
		zip_ref.extract('system.new.dat', folderdat)
		zip_ref.extract('system.transfer.list', folderdat)
	print 'GET system.transfer.list AND system.new.dat SUCCESSFULLY.\nGetting system.img...'
	d2i(['',folderdat + "/system.transfer.list",folderdat + "/system.new.dat",folderdat + "/system.img"])
	print 'GET system.img SUCCESSFULLY.'
	print 'Extracting system.img...'
	tmp = 'system' + rom.replace('/','.')
	os.makedirs(tmp)
	os.chdir("Tool")
	os.system('ImgExtractor.exe ../' + folderdat + '/system.img ../' + tmp)
	os.chdir("..")
	print 'EXTRACT system.img SUCCESSFULLY.\nGetting /system/framework...'
	#output = 'framework_' + strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	output = 'Result/framework_' + rom
	os.makedirs(output)
	os.system('copy "' + tmp + '/framework" "' + output + '"')
	print 'GET /system/framework SUCCESSFULLY.'
	shutil.rmtree(folderdat)
	shutil.rmtree(tmp)
	return 'framework_' + rom

def dat(rom):
	if sys.platform == "linux" or sys.platform == "linux2":
		return datlinux(rom)
	elif sys.platform == "win32":
		return datwindows(rom)


def rawlinux(rom):
	print 'Please wait...\nExtracting ROM...'
	folderraw = 'system.raw' + rom.replace('/','.')
	if os.path.exists(folderraw):
		os.system('rm -rf ' + folderraw)
	tmp = 'ROM' + rom.replace('/','.')
	with zipfile.ZipFile(rom,"r") as zip_ref:
		zip_ref.extractall("./" + tmp)
	print 'EXTRACT ROM SUCCESSFULLY.\nGetting /system/framework...'
	#output = 'framework_' + strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	output = 'framework_' + rom
	os.makedirs(output)
	tmp1 = 'cp -r ' + tmp + '/system/framework/* ' + output
	os.system(tmp1)
	print 'GET /system/framework SUCCESSFULLY.'
	os.system('rm -rf ' + tmp)
	return output

def rawwindows(rom):
	print 'Please wait...\nExtracting ROM...'
	folderraw = 'system.raw' + rom.replace('/','.')
	if os.path.exists(folderraw):
		shutil.rmtree(folderraw)
	tmp = 'ROM' + rom.replace('/','.')
	with zipfile.ZipFile(rom,"r") as zip_ref:
		zip_ref.extractall("./" + tmp)
	print 'EXTRACT ROM SUCCESSFULLY.\nGetting /system/framework...'
	#output = 'framework_' + strftime('%Y-%m-%d_%H-%M-%S', gmtime())
	output = 'Result/framework_' + rom
	os.makedirs(output)
	os.system('copy "' + tmp + '/system/framework" "' + output + '"')
	print 'GET /system/framework SUCCESSFULLY.'
	shutil.rmtree(tmp)
	return 'framework_' + rom

def raw(rom):
	if sys.platform == "linux" or sys.platform == "linux2":
		return rawlinux(rom)
	elif sys.platform == "win32":
		return rawwindows(rom)
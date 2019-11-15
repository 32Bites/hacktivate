#
# Checkra1n hacktivation
#
# Proudly written in VSCode
# (c) 2019 Noah Shanaberger
#
#========  Made by  =======
# Noah Shanaberger
#======== Thanks to =======
# argp, axi0mx, danyl931, jaywalker, kirb, littlelailo
# nitoTV, nullpixel, pimskeks, qwertyoruiop, sbingner, siguza
# haifisch, jndok, jonseals, xerub, lilstevie, psychotea, sferrini
# Cellebrite (ih8sn0w, cjori, ronyrus et al.)
#====== Special Note ======
# Praise the free market!
#==========================

from bs4 import BeautifulSoup
import requests
import shutil
import errno
import sys
import pexpect
import paramiko
import scp
import argparse
import time
import colorama

# - Used for adding color to the text.
def format(string, typ):
	if typ == "info":
		return colorama.Fore.GREEN + string + colorama.Fore.RESET
	elif typ == "prompt":
		return colorama.Fore.CYAN + string + colorama.Fore.RESET
	else:
		return colorama.Fore.RED + string + colorama.Fore.RESET
# - Stole this from online. I'm more accustomed to GoLang now.
def copyFolder(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        #else:
            #print('Directory not copied. Error: %s' % e)

# - This is used to find and download a macOS copy of checkra1n, and other tools.
def downloadTools():
	print(format("- [*] Installing checkra1n.", "info"))
	releasePage = requests.get("https://checkra.in/releases/")
	releaseContent = releasePage.content
	soup = BeautifulSoup(releaseContent, "html.parser")
	downloads = soup.find_all("a", {"class":"download-btn"})
	
	for download in downloads:
		if ".dmg" in str(download):
			link = download ["href"]
			checkra1n = requests.get(link).content
			with open("checkra1n.dmg", "wb+") as f:
				f.write(checkra1n)
			break
	hdiutilProc = pexpect.spawn("hdiutil attach checkra1n.dmg")
	hdiutilProc.waitnoecho()
	output = b"".join(hdiutilProc.readlines()).decode("utf-8")
	#output = subprocess.run(["hdiutil", "attach", "checkra1n.dmg"], stdout=subprocess.PIPE)
	path = "/Volumes/" + str(output).split("/Volumes/")[1].replace("\r\n", "") + "/checkra1n.app/"
	copyFolder(path, "/Applications/checkra1n.app/")
	print(format("- [*] checkra1n installed.", "info"))
	homebrew = input(format("- [!] Do you have homebrew installed (Y/n) ", "prompt"))
	if homebrew.lower() == "n":
		pexpect.spawn('/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"').waitnoecho()
		print(format("- [*] Homebrew installed.", "info"))
	print(format("- [*] Installing usbmuxd.", "info"))
	pexpect.spawn("brew install usbmuxd").waitnoecho()
	print(format("- [*] usbmuxd installed.", "info"))


# - This is used to jailbreak the device, and in turn install SSH.
def jailbreakDevice():
	print(format("- [*] We're going to jailbreak your device now.", "info"))
	input(format("- [!] Put your device into DFU mode. Hit enter when you're in DFU mode.", "prompt"))
	checkra1nProc = pexpect.spawn("/Applications/checkra1n.app/Contents/MacOS/checkra1n_gui -V")
	try:
		while True:
			line = checkra1nProc.readline()
			if b"#" not in line:
				sys.stdout.write(format(line.decode("utf-8"), "info"))
			if b"All Done" in line:
				checkra1nProc.terminate(True)
				break
	except pexpect.exceptions.TIMEOUT:
		checkra1nProc.terminate(True)
	except pexpect.exceptions.ExceptionPexpect as err:
		checkra1nProc.terminate(True)
		print("- [@] Error: " + err)
		exit(1)
	input(format("- [!] Hit enter when it is fully booted.", "prompt"))

# - This code connects to the device, and hacktivates it.
def hacktivateDevice(port):
	print(format("- [*] Starting iProxy connection.", "info"))
	iproxyProc = pexpect.spawn(f"iproxy 2222 {str(port)}")
	sshClient = paramiko.SSHClient()
	input(format("- [!] Unplug the device, and plug it back in. Hit enter when done.", "prompt"))
	print(format("- [*] Connecting to device SSH via USB.", "info"))
	sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	sshClient.connect(hostname="localhost", port=2222, username="root", password="alpine")
	print(format("- [*] Running commands.", "info"))
	commands = ["mount -o rw,union,update /", "rm -rf /Applications/Setup.app", "uicache -p /Applications/Setup.app", "rm /var/mobile/Library/Accounts/Accounts3.sqlite", "rm /var/mobile/Library/Accounts/Accounts3.sqlite-shm", "rm /var/mobile/Library/Accounts/Accounts3.sqlite-wal", "killall backboardd"]
	for command in commands:
		stdin, stdout, stderr = sshClient.exec_command(command)
		print(format(f"- [*] Running \"{command}\"", "info"))
		time.sleep(0.5)
	# Write data_ark code.
	sshClient.close()
	iproxyProc.terminate(True)
	print(format("- [*] Done.", "info"))
	print(format("- [*] You can install Cydia within the checkra1n application.", "info"))

if __name__ == "__main__":
	print("""#
# Checkra1n hacktivation
#
# Proudly written in VSCode
# (c) 2019 Noah Shanaberger
#
#========  Made by  =======
# Noah Shanaberger
#======== Thanks to =======
# argp, axi0mx, danyl931, jaywalker, kirb, littlelailo
# nitoTV, nullpixel, pimskeks, qwertyoruiop, sbingner, siguza
# haifisch, jndok, jonseals, xerub, lilstevie, psychotea, sferrini
# Cellebrite (ih8sn0w, cjori, ronyrus et al.)
#====== Special Note ======
# Praise the free market!
#==========================""")
	parser = argparse.ArgumentParser()
	parser.add_argument("--install", help="Installs nessecary dependencies.", action="store_true")
	parser.add_argument("--hacktivate", help="Starts the hacktivation process.", action="store_true")
	parser.add_argument("--alternate", help="Uses port 44 instead of 22.", action="store_true")

	args = parser.parse_args()

	if args.install:
		downloadTools()
	if args.hacktivate:
		jailbreakDevice()
		if args.alternate:
			hacktivateDevice(44)
			exit(0)
		hacktivateDevice(22)

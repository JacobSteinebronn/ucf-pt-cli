#/bin/bash

RED='\033[1;31m'
NC='\033[0m' # No Col

cd
if [ -d "./MultiMC" ]; then
	:
else 
	echo -e "Hey, it's Jacob! ${RED}Please read this!${NC} On the next screen, something like \"MultiMC Quick Setup\", if you're prompted for a java version, ${RED}select \"java\", which should be version 17 or greater${NC}"
	read -p "Press ENTER to continue!"
	mkdir MultiMC
	cd MultiMC
	ln -s ~/../jsteinebronn/Documents/MultiMC/assets .
	ln -s ~/../jsteinebronn/Documents/MultiMC/bin .
	ln -s ~/../jsteinebronn/Documents/MultiMC/libraries .
	
	cp -r ~/../jsteinebronn/Documents/MultiMC/instances .
	cp -r ~/../jsteinebronn/Documents/MultiMC/meta .
	cp -r ~/../jsteinebronn/Documents/MultiMC/icons .
	cp -r ~/../jsteinebronn/Documents/MultiMC/themes .
	cp -r ~/../jsteinebronn/Documents/MultiMC/translations .
	
	cp ~/../jsteinebronn/Documents/MultiMC/MultiMC .
	cp ~/../jsteinebronn/Documents/MultiMC/multimc.cfg .
	cp ~/../jsteinebronn/Documents/MultiMC/metacache .
	cp ~/../jsteinebronn/Documents/MultiMC/notifications.json .
fi

cd ~/MultiMC
umask 0000
./MultiMC

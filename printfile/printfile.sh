#/bin/bash

RED='\033[1;31m'
NC='\033[0m' # No Color

# Check if file exists
if ! test -f $1; then
	echo "File $1 could not be found"
   exit 0
fi
# Set up the regex and test output
re='.*pages? on (.*) sheets?.*'
OUTPUT=$(a2ps $1 -P void 2>&1)

# Check if the regex matches and finds a number gequal 4 for # sheets used
# Confirm whether we actually meant to use 4 or more sheets of paper!
[[ "$OUTPUT" =~ $re ]]
if [ ${BASH_REMATCH[1]} -ge 4 ] ; then 
	
	echo -e -n "${RED}About to print ${BASH_REMATCH[1]} pages!${NC} Are you sure you meant to do this? "
	read -p "y/n: " -n 1 -r
	echo
	if [[ ! $REPLY =~ ^[Yy]$ ]] ; then
		echo "Aborting potentially erroneous print job"
		exit 0
	fi
fi

# Check if this file was just printed and confirm if so
if test -f "$HOME/last_printfile"; then
	DIFF=$(diff -b $1 $HOME/last_printfile)
	if [ -z "$DIFF" ] ; then
		echo -e -n "${RED}About to print the same file you just printed!${NC} Are you sure you meant to do this? "
		read -p "y/n: " -n 1 -r
		echo
		if [[ ! $REPLY =~ ^[Yy]$ ]] ; then
			echo "Aborting potentially erroneous print job"
			exit 0
		fi
	fi
fi

JUDGE_ROOM="harbin,warsaw,stpetersburg,ekaterinburg,marrakech"
THIS_PC=$(hostname -s)
echo "Printing $1 from $THIS_PC..."

a2ps -2 -o tmp.ps $1

# Figure out what printer to use
if [[ "$JUDGE_ROOM" == *"$THIS_PC"* ]]; then
    echo -e "${RED}Judge Room Printer${NC}"
    lp -d P202A tmp.ps 
else
    echo -e "${RED}Main PTL Printer${NC}"
    lp -d P202 tmp.ps
fi

rm tmp.ps

# Copy the file so we don't reprint the same file
cp $1 $HOME/last_printfile

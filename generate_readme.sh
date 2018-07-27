#!/bin/sh

cat README_header.md > help.md

#for cmdfile in $(ls habu/cli/cmd_*.py)
for cmdfile in $(ls habu/cli/cmd_*.py)
do
    cmdname=$(echo $cmdfile | awk -F '/' {'print $NF'} | sed s/'^cmd_'/'habu.'/g | tr '_' '.' | sed s/'.py$'//g)
    echo "\n\n## $cmdname\n\n" >> help.md
    echo "\`\`\` {.sourceCode .bash}" >> help.md
    python3 $cmdfile --help >> help.md
    echo "\`\`\`" >> help.md
    #sudo python3 $cmdfile --help > /dev/null 2>&1
    #if [ "$?" != "0" ]
    #then
    #    echo "Error running help for $cmdfile"
    #fi
done


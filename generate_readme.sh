#!/bin/sh

cat README_header.md > help.md

#for cmdfile in $(ls habu/cli/cmd_*.py)
for cmdfilepath in $(ls habu/cli/cmd_*.py)
do
    cmdfile=$(echo $cmdfilepath | awk -F '/' {'print $NF'})
    cmdname=$(echo $cmdfile | sed s/'^cmd_'/'habu.'/g | tr '_' '.' | sed s/'.py$'//g)

    echo "\n\n## $cmdname\n\n" >> help.md
    echo "\`\`\` {.sourceCode .bash}" >> help.md
    python3 $cmdfilepath --help | sed s/$cmdfile/$cmdname/g >> help.md
    echo "\`\`\`" >> help.md
    #sudo python3 $cmdfile --help > /dev/null 2>&1
    #if [ "$?" != "0" ]
    #then
    #    echo "Error running help for $cmdfile"
    #fi
done


#!/bin/sh

cat README_header.md > README.md


for cmdfilepath in $(ls habu/cli/cmd_*.py)
do
    cmdfile=$(echo $cmdfilepath | awk -F '/' {'print $NF'})
    cmdname=$(echo $cmdfile | sed s/'^cmd_'/'habu.'/g | tr '_' '.' | sed s/'.py$'//g)
    cmdidx=$(echo $cmdname | sed s/'^habu.'/''/g)

    echo "\n[$cmdidx](#$cmdname)" >> README.md
    #echo "\[\n\n## $cmdname\n\n" >> README.md
    #echo "\`\`\` {.sourceCode .bash}" >> README.md
    #python3 $cmdfilepath --help | sed s/$cmdfile/$cmdname/g >> README.md
    #echo "\`\`\`" >> README.md
done



for cmdfilepath in $(ls habu/cli/cmd_*.py)
do
    cmdfile=$(echo $cmdfilepath | awk -F '/' {'print $NF'})
    cmdname=$(echo $cmdfile | sed s/'^cmd_'/'habu.'/g | tr '_' '.' | sed s/'.py$'//g)

    echo "\n\n## $cmdname\n\n" >> README.md
    echo "\`\`\` {.sourceCode .bash}" >> README.md
    python3 $cmdfilepath --help | sed s/$cmdfile/$cmdname/g >> README.md
    echo "\`\`\`" >> README.md
done


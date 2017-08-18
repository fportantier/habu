
remove_underscores = 'X5O_!P%@_AP[4_\PZX_54(P_^)7C_C)7}_$EIC_AR-S_TAND_ARD-_ANTI_VIRU_S-TE_ST-F_ILE!_$H+H_*'

def eicar():
    return(remove_underscores.replace('_', ''))

if __name__ == '__main__':
    print(eicar())

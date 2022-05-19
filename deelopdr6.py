"""
Auteur: Winny 't Hoen
Dit programma zoekt naar delenties en inserties in het verkregen consensus file,
en de consensus file van het referenciegenoom.
"""
import sys
import os

def opvragen():
    os.system("""cat alignment_file_vcf.vcf | egrep -v '^#' | awk '{print$4}' > ref.txt""")
    os.system("""cat alignment_file_vcf.vcf | egrep -v '^#' | awk '{print$5}' > alt.txt""")
    totaal = os.popen("""cat alignment_file_vcf.vcf | egrep -v '^#' | awk '{print$5}' | wc -l""").read()
    return totaal

def deletie_insertie(ref_n, new_n, deleties, insertie):
    deletie_vb = [',<*>\n']
    new_n_list = new_n.split(',')
    if new_n_list[-1] == '<*>\n':
        deleties += 1
        return deleties, insertie
    if new_n_list[-1] != '<*>\n' and len(new_n) > len(ref_n) and ref_n != '':
        insertie += 1
        return deleties, insertie
    else:
        return deleties, insertie
        

def main():
    totaal = opvragen()
    deletie = 0
    insertie = 0
    with open('ref.txt', 'r') as ref, open('alt.txt', 'r') as mutation, open(snakemake.output.conclusie, 'w') as concluus:
        doorgaan = True
        while doorgaan:
            ref_n = ref.readline()
            new_n = mutation.readline()
            deletie, insertie = deletie_insertie(ref_n, new_n, deletie, insertie)
            if ref_n == '':
                doorgaan = False
                break
        concluus.write("Aantal deleties: %s \n" % (deletie))
        concluus.write("Aantal inserties: %s \n" % (insertie))
        concluus.write("Totaal: %s \n" % (totaal))
        perc_inserties = (100/int(totaal)*int(insertie))
        perc_deleties = (100/int(totaal)*int(deletie))
        concluus.write("%s procent van de reads hebben een insertie ten opzichte van het referenciegenoom. \n" % (format(perc_inserties, '.2f')))
        concluus.write("%s procent van de reads hebben een deletie ten opzichte van het referenciegenoom. \n" % (format(perc_deleties, '.2f')))
        
def usage_information():
    print("""
    Usage Information Deelopdracht 6
    
    i. Functie van het script
    Dit script zoekt of er delenties of inserties zitten,
    in de verkregen vcf file te bekijken.
    ref = recentiegenoom / alt = mutatie / alt = '<*>' == deletie
    Er wordt gekeken naar;
    - De lengte van de mutatie
    - De verhouding van de resultaten

    ii. Manier van gebruik
    Het script wordt alsvolgt aangeroepen;
    snakemake --snakefile snakefile_s1101573 six

    iii. Voorbeeld aanroepen script
    snakemake --snakefile snakefile_s1101573 six
    """)

try:
    if sys.argv[1] == "-h":
        usage_information()
except:
    main()

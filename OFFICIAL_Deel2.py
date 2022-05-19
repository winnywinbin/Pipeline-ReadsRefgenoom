"""
Auteur: Winny 't Hoen
In dit programma worden de reads bekeken en op basis van hun kwaliteit scores getrimt.
De manier van trimmen is de Sliding Window.
"""
import sys

def main():
    """De files met reads worden ingeladen -> snakefile.input.fw snakefile.input.frv
    met lege files waar de juiste reads in worden geladen -> snakemake.output.new_fw snakemake.output.new_rv"""
    with open(snakemake.input.fw, 'r') as file, open(snakemake.input.rv, 'r') as file2, open(snakemake.output.new_fw, "w") as new_fw, open(snakemake.output.new_rv, "w") as new_rv:
        count = 0
        doorgaan = True
        while doorgaan:
            goedkeuring_f = 1
            goedkeuring_r = 1
            hed_f = file.readline()
            seq_f = file.readline()
            hed2_f = file.readline()
            q_f = file.readline()
            hed_r = file2.readline()
            seq_r = file2.readline()
            hed2_r = file2.readline()
            q_r = file2.readline()
            """De loop wordt gestopt als er geen nieuwe read meer aanwezig is."""
            if hed_f == '':
                doorgaan = False
                break
            """De window wordt gemaakt. Vervolgens wordt gelijk de gemiddelde kwaliteitscore berekend.
                Dit wordt gedaan door sum() -> omdat de kwaliteitcodes als ascii in het bestand aangegeven wordt.
                Vervolgens wordt de quelity line en de sequentie getrimt op basis van de gevonden aantallen."""
            for letter in range(len(q_f)):
                window = [ord(x) for x in q_f[letter:letter+3]]
                gem = sum(window)/3
                if gem > 53:
                    q_f = q_f[letter:]
                    seq_f = seq_f[letter:]
                    break
            r_q_f = q_f[::-1]
            r_seq_f = seq_f[::-1]
            """Hetzelfde wordt uitgevoerd maar dan worden de reads omgedraaid."""
            for letter in range(len(r_q_f)):
                window = [ord(x) for x in r_q_f[letter:letter+3]]
                gem = sum(window)/3
                if gem > 53:
                    dus = r_q_f[letter+1:]
                    dus_seq = r_seq_f[letter+1:]
                    official_f = dus[::-1]
                    official_seq_f = dus_seq[::-1]
                    break
            """Hier wordt aangegeven of het het waard is om de read in het bestand te houden.
                0 = niet waard, 1 = (default) wel waard.
                Bij een hele korte read is het het namelijk niet waard mee te nemen."""
            if len(official_f) <= 20:
                goedkeuring_f = 0
            """Alle stappen worden herhaald voor de reversed read."""
            for letter in range(len(q_r)):
                window = [ord(x) for x in q_r[letter:letter+3]]
                gem = sum(window)/3
                if gem > 53:
                    q_r = q_r[letter:]
                    seq_r = seq_r[letter:]
                    break
            r_q_r = q_r[::-1]
            r_seq_r = seq_r[::-1]
            for letter in range(len(r_q_r)):
                window = [ord(x) for x in r_q_r[letter:letter+3]]
                gem = sum(window)/3
                if gem > 53:
                    dus = r_q_r[letter+1:]
                    dus_seq_r = r_seq_r[letter+1:]
                    official_r = dus[::-1]
                    official_seq_r = dus_seq_r[::-1]
                    break
            if len(official_r) <= 20:
                goedkeuring_r = 0
            """Als allebij de reads lang genoeg zijn, worden de reads overgezet naar het nieuwe bestand."""
            if goedkeuring_f == 1 and goedkeuring_r == 1:
                new_fw.write(hed_f)
                new_fw.write(official_seq_f)
                new_fw.write('\n')
                new_fw.write(hed2_f)
                new_fw.write(official_f)
                new_fw.write('\n')
                new_rv.write(hed_r)
                new_rv.write(official_seq_r)
                new_rv.write('\n')
                new_rv.write(hed2_r)
                new_rv.write(official_r)
                new_rv.write('\n')

def usage_information():
    print("""
    Usage Information Deelopdracht 2
    
    i. Functie van het script
    Dit script trimt de reads op basis van hun quality waarde.
    Er wordt gekeken naar;
    - De kwaliteitsscore
    - De lengte van de read na het trimmen
    - Paired end reads, als er een read verwijderd wordt,
    wordt de paired read ook niet meegenomen.

    ii. Manier van gebruik
    Het script wordt alsvolgt aangeroepen;
    snakemake --snakefile snakefile_s1101573 two

    iii. Voorbeeld aanroepen script
    snakemake --snakefile snakefile_s1101573 two
    """)
    

try:
    if sys.argv[1] == "-h":
        usage_information()
except:
    main()

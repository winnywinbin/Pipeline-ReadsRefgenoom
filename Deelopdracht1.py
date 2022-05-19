"""
In dit script wordt er gekeken naar de inventarisatie van de reads.
Belangrijke informatie wordt bekeken; lange/kleinste read, gemiddelde lengte, GC content.
Auteur: Winny 't Hoen
Datum: eind 2019/ begin 2020
Vak: BNGP Opdracht NGS Pipeline bouwen
"""
import sys

def main():
    with open(snakemake.input.a, 'r') as file, open(snakemake.input.b, 'r') as file2, open(snakemake.output.data, "w") as f:
        count = 0
        lengte_reads_f = 0
        lengte_reads_r = 0
        minimum_read_f = 1000
        maximum_read_f = 0
        minimum_read_r = 1000
        maximum_read_r = 0
        gc_alle_f = 0
        gc_alle_r = 0
        while True:
            hed_f = file.readline()
            seq_f = file.readline()
            hed2_f = file.readline()
            q_f = file.readline()
            hed_r = file2.readline()
            seq_r = file2.readline()
            hed2_r = file2.readline()
            q_r = file2.readline()
            count += 1
            lengte_reads_f += len(seq_f)
            if hed_f == "":
                break
            if len(seq_f) < minimum_read_f:
                minimum_read_f = len(seq_f)
            if len(seq_f) > maximum_read_f:
                maximum_read_f = len(seq_f)
            gc_content_f = 0
            for letter in seq_f:
                if letter == 'G' or letter == 'C':
                    gc_content_f += 1
            gc_alle_f += gc_content_f
            lengte_reads_r += len(seq_r)
            if len(seq_r) < minimum_read_r:
                minimum_read_r = len(seq_r)
            if len(seq_r) > maximum_read_r:
                maximum_read_r = len(seq_r)   
            gc_content_r = 0
            for letter in seq_r:
                if letter == 'G' or letter == 'C':
                    gc_content_r += 1
            gc_alle_r += gc_content_r

        f.write("Forward: Aantal reads: %s \n" % (count))
        f.write("Forward: Totale lengte reads: %s \n" %(lengte_reads_f))
        f.write("Forward: Gemiddelde lengte reads: %s \n" % (format(lengte_reads_f/count-1, '.0f')))
        f.write("Forward: Minimale lengte: %s \n" % (minimum_read_f))
        f.write("Forward: Maximale lengte: %s \n" % (maximum_read_f))
        f.write("Forward: Gemiddelde gc content: %s \n" % (format(gc_alle_f/count, '.0f')))
        f.write("Reversed: Aantal reads: %s \n" % (count))
        f.write("Reversed: Totale lengte reads: %s \n" %(lengte_reads_r))
        f.write("Reversed: Gemiddelde lengte reads: %s \n" % (format(lengte_reads_r/count-1, '.0f')))
        f.write("Reversed: Minimale lengte: %s \n" % (minimum_read_r))
        f.write("Reversed: Maximale lengte: %s \n" % (maximum_read_r))
        f.write("Reversed: Gemiddelde gc content: %s \n" % (format(gc_alle_r/count, '.0f')))

def usage_information():
    print("""
    Usage Information Deelopdracht 1
    
    i. Functie van het script
    Dit script voert een inventarisatie uit van twee FastQ bestanden.
    Er wordt gekeken naar;
    1) Het aantal reads
    2) Gemiddelde lengte reads
    3) Minimum en maximum lengte van de reads
    4) GC-content per read.

    ii. Manier van gebruik
    Het script wordt alsvolgt aangeroepen;
    snakemake --snakefile snakefile_s1101573 one

    iii. Voorbeeld aanroepen script
    snakemake --snakefile snakefile_s1101573 one
    """)
    

try:
    if sys.argv[1] == "-h":
        usage_information()
except:
    main()
        

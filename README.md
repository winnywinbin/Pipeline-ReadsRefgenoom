# Pipeline-ReadsRefgenoom
Deze pipeline maakt gebruik van verschillende scripten en applicaties, met als doel om belangrijke gegevens uit een alignment tussen paired end reads en een referenciegenoom te halen.

i. Functie pipeline
		Deze pipeline maakt gebruik van verschillende scripten en applicaties,
		met als doel om belangrijke gegevens uit een alignment tussen paired end reads en een referenciegenoom te halen.
		
		ii. Manier van gebruik (aanroepen)
		De snakerige kan worden aangeroepen in de terminal, alsvolgt:
		snakemake —snakefile snakefile_s1101573 [rule]

		iii. Voorbeeld starten pipeline
		Om de gehele pipeline te laten runnen:
		snakemake —snakefile snakefile_s1101573 all
		De pipeline kan ook per rule aangeroepen worden.
		De rules: one, two, three, four, five en six
		De gekozen rule moet worden ingevoerd alsvolgt:
		snakemake —snakefile snakefile_s1101573 [rule]
		Voor informatie over de scripts die worden gebruikt:
		Deelopdrachten: 
		- Deelopdracht1.py
		- OFFICIAL_Deel2.py
		- OFFICIAL_Deelopdracht3.py
		- deelopdr6.py
		python3 [Deelopdracht 1,2,3,6] -h
		
		iv. Overzicht output bestanden
		- UitkomstDeelopdr1.txt
		- Forward_reads.fastq
		- Reversed_reads.fastq
		- UitkomstDataGetrimdeReads.txt
		- align_output.sam
		- refgenome
		- bam_output.bam
		- bam_sorted.bam
		- pileur_file_.pileup
		- align_bcf.bcf
		- alignment_file_vcf.vcf
		- consensus_file.fastq
		- Deelopdr6_interpretaties.txt

		Opmerking:
		De enorme hoeveelheid deleties heeft te maken met script2,
		die teveel van de reversed knipt, en niet forward reads.

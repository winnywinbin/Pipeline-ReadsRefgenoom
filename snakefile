rule one:
	input:
		a="/home/bngp/reads/bngsa_nietinfected_1.fastq",
		b="/home/bngp/reads/bngsa_nietinfected_2.fastq"
	output:
		data="UitkomstDeelopdr1.txt"
	script:
		"Deelopdracht1.py"

rule two:
	input:
		fw="/home/bngp/reads/bngsa_nietinfected_1.fastq",
		rv="/home/bngp/reads/bngsa_nietinfected_2.fastq"
	output:
		new_fw="Forward_reads.fastq",
		new_rv="Reversed_reads.fastq"
	script:
		"OFFICIAL_Deel2.py"

rule three:
	input:
		trim_fw= rules.two.output.new_fw,
		trim_rv= rules.two.output.new_rv
	output:
		trim_data="UitkomstDataGetrimdeReads.txt"
	script:
		"OFFICIAL_Deelopdracht3.py"

rule four:
	input:
		forward = rules.two.output.new_fw,
		reverse = rules.two.output.new_rv,
	params:
		idx = "/home/s1101573/inlevermap/indexes/Infected_consensus"
	output:
		sam = "align_output.sam"
	shell: 
		"""
		bowtie2-build /home/bngp/refgenome/infected_consensus.fasta /home/s1101573/inlevermap/indexes/Infected_consensus
		bowtie2 -x /home/s1101573/inlevermap/indexes/Infected_consensus -1 {input.forward} -2 {input.reverse} -S {output.sam} || true
		"""

rule genome:
	input: 
		refgen = "/home/bngp/refgenome/infected_consensus.fasta"
	output: 
		refgen_file = "refgenome"
	shell:
		"cp {input} {output}"

rule five:
        input:
                samfile = rules.four.output.sam,
		fa = rules.genome.output.refgen_file
        output:
                vcf_file = "alignment_file_vcf.vcf",
		consensus_file = "consensus_file.fastq"
        shell:
                """
                samtools view -S -b {input.samfile} > /home/s1101573/inlevermap/bam_output.bam;
                samtools sort /home/s1101573/inlevermap/bam_output.bam -o /home/s1101573/inlevermap/bam_sorted.bam;
		samtools mpileup -u -E -f {input.fa} /home/s1101573/inlevermap/bam_sorted.bam > /home/s1101573/inlevermap/pileur_file_.pileup;
		bcftools view -Ou /home/s1101573/inlevermap/pileur_file_.pileup > /home/s1101573/inlevermap/align_bcf.bcf || true;
                bcftools view /home/s1101573/inlevermap/align_bcf.bcf | vcfutils.pl varFilter > {output.vcf_file};
		cat /home/s1101573/inlevermap/pileur_file_.pileup | bcftools call -c | vcfutils.pl vcf2fq > {output.consensus_file}
		"""

rule six:
	output:
		conclusie = "Deelopdr6_interpretaties.txt"
	script:
		"deelopdr6.py"		

rule help:
	run:	
		print('''
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
		''')
rule all:
        input:
                expand([rules.one.output.data,
                        rules.two.output.new_fw,
                        rules.two.output.new_rv,
			rules.three.output.trim_data,
			rules.four.output.sam,
			rules.five.output.vcf_file,
			rules.five.output.consensus_file,
			rules.six.output.conclusie])

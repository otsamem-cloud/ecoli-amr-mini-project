# Antibiotic resistance genes in 30 public *Escherichia coli* genomes: a bioinformatics mini-project

*October 2026*

## Summary

Across 30 complete *Escherichia coli* genomes drawn from NCBI, the number of antibiotic resistance determinants ranges from 0 to 30 per genome, and it varies as much within a single origin as between origins.

The 30 genomes (5 per origin: human, pig, chicken, cattle, dog, environment) were drawn at random, with a fixed seed, from the 5,459 complete RefSeq genomes. They were analyzed with AMRFinderPlus 4.2.7 (database 2026-08-07.1) and typed by MLST. A method test on five reference strains came first.

Main results:

- 361 AMR-type detections (287 acquired genes, 65 point mutations, 9 disrupted genes); three genomes have none.
- 22 genomes receive an MLST type, spread over 18 types; four types are shared by two genomes each, and eight genomes have no type.
- Two thirds of the acquired genes are on plasmids (191 of 287) and one third on the chromosome (96), often in blocks of a few tens of kb.
- All 9 Chinese genomes in the panel have at least 7 detections, whereas 7 of the 10 American and Swiss genomes have 0 or 1.

These results describe genotypes, not measured resistance. With 5 genomes per origin, no statistical test is possible, and the panel is not representative of the species.

## Background and question

This mini-project asks which antibiotic resistance genes are carried by public *Escherichia coli* genomes, and how their profiles differ from one strain to another.

Antimicrobial resistance is a central issue in microbiology. Sequencing can describe the genetic determinants of resistance without culture or antibiogram, provided one keeps in mind that the presence of a gene does not prove that the strain is resistant.

The work uses public data only, as a bioinformatics exercise. It follows the sequence question, data, method, analysis, results, interpretation. A method test on five reference genomes (K-12 MG1655, SE11, UTI89, SMS-3-5 and ETEC H10407) preceded the 30-genome panel.

## Data

The panel contains 30 complete *E. coli* genomes, 5 for each of six origins, drawn at random with a fixed seed from the NCBI RefSeq genomes.

### Method test

AMRFinderPlus detects nothing in K-12 MG1655 (GCF_000005845.2) or in ETEC H10407. It finds one detection in SE11 (tet(C), on plasmid pSE11-1), one in UTI89 (marR_S3N mutation) and 17 in SMS-3-5 (10 acquired genes on plasmid pSMS35_130 and 7 chromosomal mutations). The NCBI records of these strains give no host, isolation source or country: they served to validate the analysis chain, not to compare origins.

### Panel selection

The metadata of the 5,459 complete *E. coli* genomes, RefSeq-annotated and excluding atypical genomes and genomes derived from metagenomes, were retrieved with the datasets tool in October 2026. Empty values (missing, not applicable, not collected, etc.) were treated as absent. Host or isolation source is filled in for 4,740 of the 5,459 genomes (87%).

The origin was assigned with keyword rules applied to the host, then to the isolation source. The categories used contain 2,497 human genomes, 343 cattle, 336 environment, 324 chicken, 269 pig and 136 dog. The other categories are not used: laboratory (125), food (112), mouse (45), clinical or feces without a specified host (202), other (351) and unknown (719).

Five genomes were drawn per category (random_state = 42), giving 30 genomes. The same script on the same file returns the same panel.

### Integrity checks

The 30 genomes were downloaded with datasets (46.2 MB). The 32 files of the package were checked with md5sum (32 of 32 correct), and every accession in the list has its sequence folder.

## Methods

The analysis runs on Ubuntu 24.04 (WSL), with three separate conda environments (amr_env, analyse, typage) to avoid version conflicts.

| Tool | Version | Role |
| --- | --- | --- |
| AMRFinderPlus | 4.2.7, database 2026-08-07.1 | detection of resistance genes and mutations (options -n and -O Escherichia) |
| mlst | 2.35.0 | MLST typing (option --scheme ecoli) |
| NCBI datasets | 18.38.0 | metadata and genome download |
| Biopython | 1.88 | reading FASTA files |
| pandas | 3.0.6 | summary tables |
| conda (Miniforge) | 26.7.2 | environment management |

Figures are produced with matplotlib. The steps are:

1. Retrieve the metadata of the 5,459 genomes with `datasets summary genome` and clean them with pandas.
2. Assign an origin by keywords, then draw 5 genomes per category with a fixed seed.
3. Download the 30 genomes with `datasets download genome accession` and check their md5 checksums.
4. Run AMRFinderPlus on each genome, then merge the results and attach them to the origin.
5. Type each genome with mlst.
6. Read the sequences with Biopython to find out whether each detection is on the chromosome or on a plasmid (the word “plasmid” appears in the FASTA header), then compute the positions of the acquired genes on the chromosome.
7. Produce the final table and the figures.

The check for step 6 is the following: each genome has exactly one chromosome, and no sequence has a size inconsistent with its type. Each step is written as a script; the [README](README.md) gives the order of the commands.

## Results

The number of AMR-type detections ranges from 0 to 30 per genome, and genomes of the same origin differ as much as genomes of different origins.

### Detections per genome and per origin

AMRFinderPlus reports 378 rows for the 30 genomes: 361 of AMR type (287 acquired genes, 65 point mutations, 9 disrupted genes) and 17 of STRESS type (biocide tolerance genes, counted separately). Three genomes have no AMR detection.

| Origin | Genomes | Minimum | Median | Maximum |
| --- | --- | --- | --- | --- |
| cattle | 5 | 0 | 1 | 23 |
| dog | 5 | 1 | 12 | 28 |
| environment | 5 | 0 | 13 | 17 |
| human | 5 | 1 | 19 | 22 |
| pig | 5 | 3 | 11 | 17 |
| chicken | 5 | 0 | 27 | 30 |

With 5 genomes per origin, these medians describe the panel and do not allow origins to be ranked. Country seems to matter as much: all 9 Chinese genomes have at least 7 detections (from 7 to 30), whereas 7 of the 10 American and Swiss genomes have 0 or 1. Because country is mixed with origin (3 of the 5 chickens come from China), the two effects cannot be separated.

### Antibiotic classes

Eight classes are the most frequent: beta-lactams, aminoglycosides, quinolones, tetracyclines, trimethoprim, sulfonamides, phenicols and macrolides. The most heavily loaded genomes combine most of them, whatever their origin.

AMRFinderPlus also assigns composite classes, such as AMINOGLYCOSIDE/QUINOLONE: an element of this type is not counted in the QUINOLONE column, which therefore underestimates quinolone-related determinants. The MULTIDRUG class groups several families and is not comparable with the other rows.

![Antibiotic classes detected per genome and per origin](results/panel30_heatmap.png)

Figure 1: antibiotic classes detected (AMR-type elements, AMRFinderPlus 4.2.7, database 2026-08-07.1), one genome per row, grouped by origin; a black line separates the origins, and genomes without detection appear as pale rows.

### MLST typing

mlst typing relies on 8 loci (uidA, trpB, trpA, icdA, pabB, putP, polB, dinB), which, judging by their names, correspond to the Institut Pasteur scheme. Its numbers cannot be compared with those of the Achtman scheme. Twenty-two genomes receive a type, spread over 18 distinct types.

Four types are shared by two genomes each: ST87 (two Chinese cattle), ST88 (two chickens from Hebei), ST43 (two humans, United States and Italy) and ST2 (a British human and a Swiss wastewater sample). Eight genomes have no type: one gene is missing (1 genome), one allele is new (4 genomes) or the allele combination is not listed (3 genomes).

The type does not determine the resistance content: the two ST43 genomes have 10 and 22 detections. The two Swiss dogs do not have the same type, and the ST87 cattle and the ST88 chicken from Hebei belong to distinct lineages despite almost identical class profiles.

### Location: chromosome or plasmid

The 30 genomes have one chromosome and 0 to 8 plasmids, for a total size of 4.70 to 6.06 Mb. Of the 287 acquired genes, 191 are on plasmids and 96 on the chromosome (in 15 genomes). The 74 point or disrupted mutations are all on the chromosome, as expected.

The acquired genes on the chromosome are classic resistance genes (sul2, tet(A), tet(B), blaTEM-1, aadA1, blaCMY-2), the same as on plasmids. The number of plasmids does not predict resistance: one genome with 8 plasmids has 4 detections, one with 7 plasmids has one, whereas genomes with 1 or 3 plasmids have more than 20.

### Gene blocks on the chromosome

For five genomes, the positions of the acquired genes on the chromosome were examined one by one.

| Genome | Origin | Observation |
| --- | --- | --- |
| GCF_029625135.1 | cattle (ST87) | two blocks 188 kb apart: 4 genes over 10 kb, then 12 genes over 37 kb |
| GCF_988243845.1 | human, United Kingdom | 3 tandem copies of blaOXA-244 (about 6 kb), then 11 genes over 27 kb |
| GCF_024585985.1 | pig, Cuba | 11 genes over 26 kb, then 2 isolated copies of blaCMY-2 |
| GCF_059727225.1 | dog, Japan | 4 separate sites, including 2 copies of blaCTX-M-14 |
| GCF_024585365.1 | chicken, Cuba | 2 isolated genes (blaTEM-1 and tet(B)), 3.2 Mb apart |

The blocks of the British human genome and the Cuban pig have the same gene order: tet(B), catA1, dfrA, aadA, sul1, mrx(A) and mph(A), blaTEM, sul2, aph(3'')-Ib, aph(6)-Id. Only the dfrA (dfrA17 or dfrA12) and aadA (aadA5 or aadA2) genes change, and the two blocks are at different positions on the chromosome (4.23 Mb and 1.23 Mb). According to the literature, these two genes are typically class 1 integron cassettes, followed by sul1; this point was not verified here.

The two ST88 chickens each carry 6 genes over 28.1 kb at the same place on the chromosome (about 4.47 Mb), which is consistent with a common lineage.

These blocks look like elements integrated into the chromosome. Neither the neighboring sequences (transposases, integrases) nor the assemblies were examined: an assembly artifact is not excluded.

The British genome comes from a “rectal screening swab”. According to the literature (to be verified), blaOXA-244 is an OXA-48-type variant, a carbapenemase. If confirmed, this screening sample may have targeted bacteria carrying such genes, which would bias the selection of this genome.

## Limitations and corrections

This work is a descriptive exercise: the limitations below prevent any general conclusion about *E. coli*.

### Limitations

- Unrepresentative panel: it comes from complete genomes deposited in NCBI, of which 46% are human (2,497 of 5,459).
- Sample sizes: 5 genomes per origin allow no statistical test.
- Country and origin mixed: 9 of the 30 genomes come from China, including 3 of the 5 chickens.
- Non-independent genomes: four pairs share an MLST type (ST2, ST43, ST87 and ST88).
- Ambiguous origins: “calf box” may refer to the pen; wastewater (the “environment” category) contains bacteria of human or animal origin; a “rectal screening swab” is a screening sample.
- Missing data: 5 genomes without a collection date and 2 without a country; dates range from 2006 to 2024.
- Keyword categories: rules written for this project, with 351 “other” and 719 “unknown” genomes set aside.
- Genotype, not phenotype: no antibiogram confirms the resistances.
- MLST: 8 loci have limited resolution, and 8 genomes have no type.
- Gene blocks: neighboring sequences and assemblies were not examined.

### Corrections made during the analysis

- A first count added antibiotic genes and biocide genes together; it was redone on the AMR type only, with the 17 biocide rows counted separately.
- A cross-tabulation had dropped the genomes without detection; they are now kept through a join on the list of 30 genomes.
- The first categorization rules recognized “canine”, “calf” and “seawater” poorly, and could confuse “pig” and “pigeon”; they were corrected with word boundaries.
- A supposed kinship between two Swiss dogs (neighboring accession numbers) is not confirmed by typing: their types differ.
- The MLST scheme was first taken to be the Achtman one; the locus names indicate the Institut Pasteur one.
- A first calculation of the span of genes on the chromosome did not distinguish several blocks; gene-by-gene positions showed two blocks in the cattle genome from Hebei.

## Conclusion

This panel does not allow us to say that origin explains resistance content: the variation within an origin is as large as between origins.

The detections are mostly classic acquired resistance genes, carried two thirds by plasmids and one third by the chromosome, often in blocks of a few tens of kb. The analysis chain (metadata, sampling, download, AMRFinderPlus, MLST, location) works end to end and can be rerun identically.

Next steps:

- enlarge the panel and keep only one genome per MLST type;
- compare the genes themselves between genomes of different lineages, to test the shared-block hypothesis;
- examine the sequences around the chromosomal blocks;
- compare the genotypes with antibiograms.

## Use of AI

The Python scripts used in this project were written with the help of an AI assistant (Claude, by Anthropic).

## Appendix: the 30 panel genomes

The table gives, for each genome, the origin, the country, the MLST type, the number of AMR detections and their split between chromosome and plasmids. A dash marks information missing from the NCBI record.

| Genome | Origin | Country | ST | AMR detections | Chromosome / plasmids |
| --- | --- | --- | --- | --- | --- |
| GCF_005221725.1 | cattle | — | 628 | 0 | 0 / 0 |
| GCF_049570325.1 | cattle | United States (South Dakota) | new allele | 1 | 1 / 0 |
| GCF_030384705.1 | cattle | Switzerland | 26 | 1 | 1 / 0 |
| GCF_029227895.1 | cattle | China (Loess Plateau) | 87 | 15 | 1 / 14 |
| GCF_029625135.1 | cattle | China (Hebei) | 87 | 23 | 16 / 7 |
| GCF_046107165.1 | dog | Switzerland | unlisted combination | 1 | 0 / 1 |
| GCF_046108985.1 | dog | Switzerland | 490 | 1 | 0 / 1 |
| GCF_001900675.1 | dog | — | 24 | 12 | 3 / 9 |
| GCF_059727225.1 | dog | Japan (Tokyo) | new allele | 13 | 13 / 0 |
| GCF_053169045.1 | dog | Thailand (Bangkok) | 1362 | 28 | 7 / 21 |
| GCF_902810405.1 | environment | United States | unlisted combination | 0 | 0 / 0 |
| GCF_029991185.1 | environment | Switzerland (Zug) | 506 | 6 | 5 / 1 |
| GCF_051521855.1 | environment | Panama | new allele | 13 | 2 / 11 |
| GCF_017639145.1 | environment | Switzerland (Basel) | 2 | 15 | 3 / 12 |
| GCF_055687985.1 | environment | China (Heyuan) | 1331 | 17 | 12 / 5 |
| GCF_016903615.1 | human | United States (WA) | 1 | 1 | 1 / 0 |
| GCF_048585575.1 | human | Italy | 43 | 10 | 7 / 3 |
| GCF_988243845.1 | human | United Kingdom | 2 | 19 | 18 / 1 |
| GCF_034119705.1 | human | China (Guangzhou) | 471 | 20 | 7 / 13 |
| GCF_024917335.1 | human | United States (Houston) | 43 | 22 | 21 / 1 |
| GCF_030296275.1 | pig | Japan (Iwate) | 1760 | 3 | 2 / 1 |
| GCF_030013715.1 | pig | Belgium | 132 | 4 | 1 / 3 |
| GCF_048160275.1 | pig | China (Guangxi) | unlisted combination | 11 | 0 / 11 |
| GCF_024585985.1 | pig | Cuba (Calimete) | gene not found | 16 | 15 / 1 |
| GCF_043995745.1 | pig | China (Yangzhou) | 637 | 17 | 2 / 15 |
| GCF_054903135.1 | chicken | United States (GA) | new allele | 0 | 0 / 0 |
| GCF_057586655.1 | chicken | China (Guizhou) | 632 | 7 | 5 / 2 |
| GCF_029625115.1 | chicken | China (Hebei) | 88 | 27 | 10 / 17 |
| GCF_024585365.1 | chicken | Cuba (Quivican) | 19 | 28 | 7 / 21 |
| GCF_029318935.1 | chicken | China (Hebei) | 88 | 30 | 10 / 20 |

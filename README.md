# PMPred: Pathogenic Mutation Prediction

PMPred is a linux based tool for scoring the deleteriousness of nonsense variants as well as insertion/deletions variants in the human genome (currently supported builds: GRCh37/hg19).

The pipeline is built using Nextflow, a workflow tool to run tasks across multiple compute infrastructures in a very portable manner. To predict the pathogenic effect of mutations, PMPred measures the significance of changes between molecular functions of the wildtype and altered sequences. Indeed, the method calculates the pathogenic rate of frameshift indels and nonsense mutations in terms of function loss without specific training. In addition, it calculates the position of variants on target genes and conducts domain prediction analysis to provide a detailed information of each variant. As a result of this process, an annotated list regarding the consequences of these variants on conserved domains and their pathogenic rate is provided to the user.

## Pipeline summary

&nbsp;&nbsp;&nbsp; 1.Convert VCF file to ANNOVAR input format (convert2annovar.pl)<br/>
&nbsp;&nbsp;&nbsp; 2.Variant annotation (annotate_variation.pl)<br/>
&nbsp;&nbsp;&nbsp; 3.Infer mutated protein sequence(coding_change.pl)<br/>
&nbsp;&nbsp;&nbsp; 4.Convert sequences to fasta format (annovar2unigo)<br/>
&nbsp;&nbsp;&nbsp; 5.Remove empty lines (grep)<br/>
&nbsp;&nbsp;&nbsp; 6.Function prediction (UniGOPred)<br/>
&nbsp;&nbsp;&nbsp; 7.Domain prediction (InterProScan)<br/>
&nbsp;&nbsp;&nbsp; 8.Pathogenicity prediction (prediction.py)<br/>

## Usage
### Input 

Users who have a list of nonsense or indel variants that they wish to functionally characterise can use the PMPred package to run the classification algorithms.<br/>

Data must be a VCF containing phased genotype data; no other formats are currently supported.

### Output

The output format is a csv file reporting all variant according to pathogenic rate in ascending order. It has the following fields:

&nbsp;&nbsp;&nbsp; 1.Variant<br/> 
&nbsp;&nbsp;&nbsp; 2.Transcript stable ID<br/>
&nbsp;&nbsp;&nbsp; 3.Gene Symbol<br/>
&nbsp;&nbsp;&nbsp; 4.Pvalue<br/>
&nbsp;&nbsp;&nbsp; 5.Correlation<br/>
&nbsp;&nbsp;&nbsp; 6.Location(Distance from beginning)<br/>
&nbsp;&nbsp;&nbsp; 7.Pathogenic class<br/>
&nbsp;&nbsp;&nbsp; 8.Wildtype domain<br/>
&nbsp;&nbsp;&nbsp; 9.Altered domain<br/>

## Quick start

1.Install python

Follow the instructions on python.org to install Python version 3.0 or newer. Pip, python's package manager, must be included in the installation.

2.Install Nextflow

Download the distribution package by copying and pasting this command in your terminal:

```
curl -fsSL https://get.nextflow.io | bash
```
It creates the nextflow executable file in the current directory. You may want to move it to a folder accessible from your $PATH.<br/>
Nextflow documentation is available at this link http://docs.nextflow.io

3.Download Annovar data

Annovar data is available at this link https://www.openbioinformatics.org/annovar/annovar_download_form.php

4.Install InterProScan

>To install the InterProScan 5 software you then need to complete the following steps:
>
>* Obtaining the core InterProScan software
>```
>mkdir my_interproscan
>cd my_interproscan
>wget https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.59-91.0/interproscan-5.59-91.0-64-bit.tar.gz
>wget https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.59-91.0/interproscan-5.59-91.0-64-bit.tar.gz.md5
>```
>
>(Direct link: https://ftp.ebi.ac.uk/pub/software/unix/iprscan/5/5.59-91.0/interproscan-5.59-91.0-64-bit.tar.gz)
>
>* Extract the tar ball:
>```
>tar -pxvzf interproscan-5.59-91.0-*-bit.tar.gz
>```
>
>This is a completely self-contained version that includes member database specific binaries and model / signature files. This should run 'out of the box' on a Linux system. Note that it excludes analyses that contain components for which you are obliged to acquire your own license.
>
>* Index hmm models
>
>Before you run interproscan for the first time, you should run the command:
>```
>python3 setup.py interproscan.properties
>```
>
>This command will press and index the hmm models to prepare them into a format used by hmmscan.<br/>
>For more information on downloading, installing and running InterProScan please see the InterProScan readthedocs.

5.Download UniGOPred data

UniGOPred data is available at this link ?

6.Dependencies

Other dependencies are available in requirements.txt file.
```
pip install -r requirements.txt
```
7.Start running your own analysis!
```
nextflow run main.nf --input test.vcf
```

#!/usr/bin/env nextflow

params.vcf = "$baseDir/annovar/example/*.vcf"
params.humandb = "$baseDir/annovar/humandb"
params.annovar1 = "$baseDir/annovar/convert2annovar.pl"
params.annovar2 = "$baseDir/annovar/annotate_variation.pl"
params.annovar3 = "$baseDir/annovar/coding_change.pl"
params.annunigo = "$baseDir/filter/annovar2unigopred.py"
params.interpro = "$baseDir/my_interproscan/interproscan-5.53-87.0/interproscan.sh"
params.unigopred1 = "$baseDir/unigopred_docker/html/UniGOPred/runGOpredMF.rb"
params.unigopred2 = "$baseDir/unigopred_docker/html/UniGOPred/GOterms50MF.txt"
params.predict = "$baseDir/prediction/prediction.py"
params.prlen = "$baseDir/prlen/proteinlength.xlsx"
params.folder = "$baseDir/uploads"
myDir = file(params.folder)
myDir.mkdirs()

vcf_file     = file(params.vcf)
humandb = params.humandb
ANNOVAR      = params.annovar1
ANNOVAR2      = params.annovar2
ANNOVAR3      = params.annovar3
ANNUNIGO      = params.annunigo
INTERPRO      = params.interpro
UNIGO1      = params.unigopred1
UNIGO2      = params.unigopred2
PRD      = params.predict
PRLEN      = params.prlen

process 'convert2annovar' {

  input:
      file vcf from vcf_file

  output:
      path "${vcf.baseName}.avinput" into vcf_ch

  script:
  """
  $ANNOVAR -format vcf4 $vcf > ${vcf.baseName}.avinput

  """
}

process 'annotate_variation' {

  input:
      file avinput from vcf_ch

  output:
      path "*.avinput.exonic_variant_function" into vcf_ch2

  script:
  """
  $ANNOVAR2 -geneanno -dbtype refGene -buildver hg19 $avinput $humandb/
  """
}

process 'coding_change' {

  input:
      file exonic_variant_function from vcf_ch2

  output:
      path "${exonic_variant_function.baseName}.txt" into vcf_ch3

  script:
  """
  $ANNOVAR3 $exonic_variant_function $humandb/hg19_refGene.txt $humandb/hg19_refGeneMrna.fa -includesnp > ${exonic_variant_function.baseName}.txt
  """
}

process 'annovar2unigo' {

  input:
      file txt from vcf_ch3

  output:
      path "${txt.baseName}.fasta" into vcf_ch4

  script:
  """
  python $ANNUNIGO $txt ${txt.baseName}.fasta
  """
}

process 'grp' {

  input:
      file fasta from vcf_ch4

  output:
      path "${fasta.baseName}.fasta" into vcf_ch5, vcf_ch6

  script:
  """
  grep . $fasta
  """
}

process 'interproscan' {

  input:
      file fasta from vcf_ch5

  output:
      path "*.tsv" into vcf_ch7

  script:
  """
  $INTERPRO -appl Pfam -i $fasta
  """
}

process 'unigopred' {

  input:
      file fasta from vcf_ch6

  output:
      path "test2/results" into vcf_ch8

  script:
  """
  ruby $UNIGO1 $UNIGO2 $fasta test2 6 10
  """
}

process 'prediction' {

  input:
      path results from vcf_ch8
      file tsv from vcf_ch7

  output:
      path "results" into vcf_ch9
      path "results/*.csv" into vcf_ch10

  script:
  """
  python $PRD $results $PRLEN $tsv
  """
}

process 'rename' {

  input:
      file csv from vcf_ch10

  output:
      path "PMPred.csv" into vcf_ch11

  script:
  """
  #!/usr/bin/env python3
  import os
  os.rename('$csv', 'PMPred.csv')
  """
}

vcf_ch11.subscribe { it.copyTo(myDir) }

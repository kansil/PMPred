from flask import Flask, render_template, request, flash, redirect
import os, shutil
import pandas
import re
import mygene
from scipy.stats import pearsonr
import sys
from scipy import stats
from pathlib import Path

path2r = Path(sys.argv[1])
UPLOAD_FOLDER = os.path.join(path2r)
prlen = pandas.read_excel(sys.argv[2])
prlen = pandas.DataFrame(prlen)
interproscan = pandas.read_csv(sys.argv[3], sep='\t', header=None)
interproscan.columns = ("1","2","3","4","5","6","7","8","9","10","11","12","13")
table = []
for root, dirs, files in os.walk(UPLOAD_FOLDER):
    for filename in files:
        if not os.path.isdir(os.path.join(UPLOAD_FOLDER, filename.split("_")[0])):
            output = os.mkdir(os.path.join(UPLOAD_FOLDER, filename.split("_")[0]))
    for filename in files:
        if filename.endswith("WILDTYPE.preds"):
            shutil.move(os.path.join(UPLOAD_FOLDER, filename), os.path.join(UPLOAD_FOLDER, filename.split("_")[0]))
        if filename.endswith("ALTERED.preds"):
            shutil.move(os.path.join(UPLOAD_FOLDER, filename), os.path.join(UPLOAD_FOLDER, filename.split("_")[0]))
for root, dirs, files in os.walk(UPLOAD_FOLDER):
    for filename in files:
        if filename.endswith("ALTERED.preds"):
            col_name_mut = ["GOTERM", "v1", "v2", "v3", "Prediction Score_y"]
            df_alt = pandas.read_csv(os.path.join(root, filename), delimiter='\t', names=col_name_mut)
            df_alt_by_goterm = df_alt.sort_values('GOTERM')
            df_alt_by_goterm = df_alt_by_goterm[["GOTERM", "Prediction Score_y"]]
            df_alt_by_goterm.to_csv(os.path.join(root, filename) + r'.csv')
        if filename.endswith("WILDTYPE.preds"):
            col_name_wild = ["GOTERM", "v1", "v2", "v3", "Prediction Score_x"]
            df_nm = pandas.read_csv(os.path.join(root, filename), delimiter='\t', names=col_name_wild)
            df_nm_by_goterm = df_nm.sort_values('GOTERM')
            df_nm_by_goterm = df_nm_by_goterm[["GOTERM", "Prediction Score_x"]]
            df_nm_by_goterm.to_csv(os.path.join(root, filename) + r'.csv')
 
dl = 0
for root, dirs, files in os.walk(UPLOAD_FOLDER):
    count = 0
    dom = []
    wildtype = []
    altered = []
    for filename in files:
        if filename.endswith(".preds.csv"):
            if filename.endswith("ALTERED.preds.csv"):
                NM = re.search('NM_(.+?)c.', filename).group(1)
                NM = "NM_" + NM
                var = re.search('c.(.+?)_ALTERED', filename).group(1)
                var = "c." + var
                line_unigo = re.search('(.+?)NM', filename).group(1)
                loc = (re.findall('\d+', filename))[2]
                mg = mygene.MyGeneInfo()
                genename = mg.querymany([NM], scopes='refseq')
                gname = genename[0]['symbol']
                gname = gname.upper()
                for i in range(len(prlen['Gene_names'])):
                    if prlen.iloc[i, 2] == gname:
                        length = prlen.iloc[i, 1]
                        prc = ((int(loc) // 3) / int(length)) * 100
                        prc = float("{0:.0f}".format(prc))
                        prc = str(prc) + "% away from N-terminus"
                for i in range(len(interproscan)):
                    line_interpro = re.search('line\|(.+?)NM', interproscan["1"][i]).group(1)
                    dsc = interproscan["1"][i]
                    if str(line_interpro) == str(line_unigo):
                        if dsc[-4] == "E":
                            wildtype.append(interproscan["13"][i]) if interproscan["13"][i] not in wildtype else wildtype
                        if dsc[-4] == "D":
                            altered.append(interproscan["13"][i]) if interproscan["13"][i] not in altered else altered
            if count == 0:
                ndf1 = pandas.read_csv(os.path.join(root, filename), delimiter=',')
            if count == 1:
                ndf2 = pandas.read_csv(os.path.join(root, filename), delimiter=',')
                mg = pandas.merge(ndf1, ndf2, on=['GOTERM'])
                mg['Score_diffr'] = abs(mg['Prediction Score_x'] - mg['Prediction Score_y'])
                mg_d = mg.sort_values('Score_diffr', ascending=False)
                mg_dif = mg_d.nlargest(50, ['Score_diffr'])
                t, e = (stats.ttest_rel(mg_dif['Prediction Score_x'], mg_dif['Prediction Score_y']))
                corr, _ = pearsonr(mg_dif['Prediction Score_x'], mg_dif['Prediction Score_y'])
                if float(corr) < 0.99:
                    pth = "P"
                if float(corr) >= 0.99:
                    pth = "B"
                mg_dif.to_csv(os.path.join(root, filename) + r'.csv')
                thisdict = {
                    "Variant": var,
                    "Transcript": NM,
                    "Gene": gname,
                    "Pvalue": float(e),
                    "Correlation": float(corr),
                    "Location": prc,
                    "Pathogenicity": pth,
                    "WildtypeDomain": wildtype,
                    "AlteredDomain": altered
                }
                table.append(thisdict)
                dl = dl + 1
            count += 1
newdict = {}
for k, v in [(key, d[key]) for d in table for key in d]:
    if k not in newdict:
        newdict[k] = [v]
    else:
        newdict[k].append(v)
df = pandas.DataFrame(newdict)
pandas.options.display.float_format = '{:}'.format
df.to_csv(os.path.join(root) + r'.csv', index=False, header=True)

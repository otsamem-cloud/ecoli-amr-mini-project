#!/bin/bash
DATA=/mnt/c/Bioinfo_RAM/Data/panel30/ncbi_dataset/data
OUT=/mnt/c/Bioinfo_RAM/Results/panel30

command -v amrfinder > /dev/null || { echo "amrfinder introuvable : lance d'abord 'conda activate amr_env'"; exit 1; }
mkdir -p "$OUT"

for f in "$DATA"/GCF_*/*_genomic.fna; do
  id=$(basename "$f" _genomic.fna)
  if [ -s "$OUT/$id.tsv" ]; then
    echo "déjà fait : $id"
    continue
  fi
  echo "== $id"
  amrfinder -n "$f" -O Escherichia -o "$OUT/$id.tsv.tmp" > "$OUT/$id.log" 2>&1 \
    && mv "$OUT/$id.tsv.tmp" "$OUT/$id.tsv" \
    || echo "ÉCHEC : $id (voir $OUT/$id.log)"
done
echo "Terminé."

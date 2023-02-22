# JANCE

This project is cloned from [original ANCE repository](https://github.com/microsoft/ANCE.git).

JANCE is a project for creating japanese dense retriever with ANCE.

A warmped xlm-roberta-base model, trained with English MS Marco and Japanese mMarco , is uploaded on huggingface.
https://huggingface.co/k-ush/xlm-roberta-base-ance-en-jp-warmup

## Dataset Preparetion

Downloads dataset with original ANCE dataset download script beforehand.

⚠︎WARN: This script overwrite original English Dataset.

``` sh
$ poetry init
$ poetry shell
$ python data/gen_jp_data.py
```
Then, you'll get Japanese version of following dataset.
```
triples.train.small.tsv
collection.tsv
queries.dev.small.tsv
queries.train.tsv
top1000.dev
```


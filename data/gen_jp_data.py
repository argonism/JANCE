from pathlib import Path

import ir_datasets
from tqdm import tqdm

DATA_DIR = Path(__file__).parent.absolute()


def gen_triples_small_tsv():
    target_path = DATA_DIR.joinpath(
        "raw_data/triples.train.small.tsv"
    )
    dataset = ir_datasets.load("mmarco/v2/ja/train")
    query_table = {
        query.query_id: query.text for query in dataset.queries_iter()
    }
    docstore = dataset.docs_store()
    with target_path.open("w") as fw:
        for triple in tqdm(
            dataset.docpairs_iter(), total=dataset.docpairs_count()
        ):
            query = query_table[triple.query_id]
            positive = docstore.get(triple.doc_id_a).text
            negative = docstore.get(triple.doc_id_b).text
            line = (
                "\t".join(
                    [
                        query,
                        positive,
                        negative,
                    ]
                )
                + "\n"
            )
            fw.write(line)


def gen_collection_tsv():
    dataset = ir_datasets.load("mmarco/v2/ja")
    target_path = DATA_DIR.joinpath("raw_data/collection.tsv")
    with open(target_path, "w") as fw:
        for doc in tqdm(
            dataset.docs_iter(), total=dataset.docs_count()
        ):
            line = "\t".join([doc.doc_id, doc.text]) + "\n"
            fw.write(line)


def gen_queries_tsv():
    def write_queries_tsv(output_path, queries_iter, total=None):
        with output_path.open("w") as fw:
            for query in tqdm(queries_iter, total=total):
                line = "\t".join([query.query_id, query.text]) + "\n"
                fw.write(line)

    dev_path = DATA_DIR.joinpath("raw_data/queries.dev.small.tsv")
    dataset = ir_datasets.load("mmarco/v2/ja/dev/small")
    write_queries_tsv(
        dev_path,
        dataset.queries_iter(),
        total=dataset.queries_count(),
    )

    train_path = DATA_DIR.joinpath("raw_data/queries.train.tsv")
    dataset = ir_datasets.load("mmarco/v2/ja/train")
    write_queries_tsv(
        train_path,
        dataset.queries_iter(),
        total=dataset.queries_count(),
    )


def gen_top1000_dev():
    top1000_path = DATA_DIR.joinpath("raw_data/top1000.dev")
    dataset = ir_datasets.load("mmarco/v2/ja/dev/small")
    query_table = {
        query.query_id: query.text for query in dataset.queries_iter()
    }
    docstore = dataset.docs_store()
    jp_top1000 = []
    with top1000_path.open() as f:
        for line in tqdm(f):
            qid, pid, _, _ = line.split("\t")
            jp_query = query_table[qid]
            jp_passage = docstore.get(pid).text
            jp_top1000.append((qid, pid, jp_query, jp_passage))

    with top1000_path.open("w") as fw:
        for row in tqdm(jp_top1000):
            line = "\t".join(row) + "\n"
            fw.write(line)


def gen_all():
    gen_queries_tsv()
    gen_collection_tsv()
    gen_triples_small_tsv()
    gen_top1000_dev()


if __name__ == "__main__":
    gen_all()

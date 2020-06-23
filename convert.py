"""Convert template tsv and populate manifest/ and references/protocols/"""
import argparse
import pathlib
import pandas as pd

def mk_participant_manifest(path, template_tsv, cohort_cols = []):
    '''
	template to manifest
    Source Name -> biosample_id
    characteristics[invididual] -> local_participant_id
    join characteristics[phenotype], characteristics[compound]

    characteristics[organism]	characteristics[organism part]	characteristics[cell type]	characteristics[ancestry category]	characteristics[age]	characteristics[sex]	characteristics[disease]	characteristics[individual]	assay name	comment[data file]	comment[fraction identifier]	comment[label]	comment[instrument]	comment[cleavage agent details]
    '''
    pm_cols = ['local_participant_id', 'cohort', 'biosample_id']
    t_cols = ['characteristics[organism part]',	'characteristics[cell type]', 'characteristics[ancestry category]',	'characteristics[age]',
	          'characteristics[sex]', 'characteristics[disease]', 'characteristics[developmental stage]']
    if not cohort_cols:
        cohort_cols = ['characteristics[phenotype]', 'characteristics[compound]', 'characteristics[disease]']

    biosample_cols = ['source name', 'characteristics[biological replicate]', 'comment[technical replicate]']
    t = pd.read_csv(template_tsv, sep='\t')
    t.columns = map(str.lower, t.columns)
    t = t.rename(columns={'characteristics[individual]':'local_participant_id'})

    t.loc[:, 'cohort'] = t.apply(lambda row: '___'.join([str(row[x]) for x in cohort_cols if x in t.columns]), axis=1)
    t.loc[:, 'biosample_id'] = t.apply(lambda row: '___'.join([str(row[x]) for x in biosample_cols if x in t.columns]), axis=1)
    t[pm_cols + [x for x in t_cols if x in t.columns]].to_csv(path / 'participant_manifest.csv', index=False)

def mk_manifests(path, template_tsv, cohort_cols):
    mk_participant_manifest(path, template_tsv, cohort_cols)


def main(args=None):
    pathlib.Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    d = pathlib.Path(args.out_dir)
    cohort_cols = []
    if args.cohort_cols:
        with open(args.cohort_cols) as f:
            cohort_cols = [l.strip() for l in f]
    mk_manifests(d, args.template_tsv, cohort_cols)
    # mk_protocols(d)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Populate manifest and references/protocols"
    )
    parser.add_argument(
        "template_tsv",
        help="ex https://github.com/arcus/proteomics-metadata-standard/blob/master/templates/sdrf-default.tsv",
    )
    parser.add_argument("out_dir", help="Output directory")
    parser.add_argument(
        "cohort_cols",
        help="ex https://github.com/arcus/proteomics-metadata-standard/blob/master/templates/sdrf-default.tsv",
        default = '',
        nargs='?'
    )
    args = parser.parse_args()
    main(args)

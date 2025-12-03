import json
import re
import warnings
from pathlib import Path

import click

from discopy_data.data.loaders.raw import load_texts, load_texts_fast

# quiet upstream adapters warning triggered by trankit/tokenizers
warnings.filterwarnings(
    "ignore",
    message="Passing list objects for adapter activation is deprecated",
    category=FutureWarning,
)


def _read_text(src):
    """Read input (bytes or str) and return a UTF-8 string.

    Falls back to per-byte substitution on decode errors to keep length stable.
    """
    data = src.buffer.read() if hasattr(src, "buffer") else src.read()
    if isinstance(data, str):
        return data
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        b = bytearray(data)
        patches = 0
        while True:
            try:
                text = b.decode("utf-8")
                break
            except UnicodeDecodeError as e:
                b[e.start] = 0x27  # replace offending byte, keep length
                patches += 1
        return text


@click.command()
@click.option('-i', '--src', default='-', type=click.File('rb'))
@click.option('-o', '--tgt', default='-', type=click.File('w'))
@click.option('-t', '--tokenize-only', is_flag=True)
@click.option('-f', '--fast', is_flag=True)
@click.option(
    '--docid-from-filename', is_flag=True, 
    help="Use input filename (stem) as docID instead of hashed text."
)
def main(src, tgt, tokenize_only, fast, docid_from_filename):
    document_loader = load_texts_fast if fast else load_texts
    text = _read_text(src)
    
    base_name = None
    if docid_from_filename and hasattr(src, "name") \
        and src.name not in ("-", "<stdin>"):
        base_name = Path(src.name).stem

    for idx, doc in enumerate(
        document_loader(
            re.split(r'\n\n\n+', text), tokenize_only=tokenize_only
        )
    ):
        if base_name:
            doc_id = base_name if idx == 0 else f"{base_name}#{idx}"
            doc.doc_id = doc_id
            doc.meta['fileID'] = doc_id
        tgt.write(json.dumps(doc.to_json()) + '\n')


if __name__ == '__main__':
    main()

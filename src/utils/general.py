from typing import List

from spacy.language import Language


def process_texts(pipeline: Language, texts: List[str]):
    """
    Processes a list of texts using a SpaCy pipeline to clean and lemmatize them.

    Args:
        pipeline (Language): A SpaCy language pipeline.
        texts (List[str]): A list of input texts to process.

    Returns:
        List[str]: A list of cleaned and lemmatized texts.
    """
    texts_clean = []

    for doc in pipeline.pipe(
        texts=texts,
        disable=["ner"]
    ):
        
        lemmas = []
        for token in doc:
            if not any([token.is_stop, token.is_punct]):
                lemmas.append(token.lemma_.lower())
        texts_clean.append(" ".join(lemmas) if lemmas else None)

    return texts_clean

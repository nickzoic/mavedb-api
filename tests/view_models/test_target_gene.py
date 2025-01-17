from mavedb.view_models.target_gene import TargetGeneCreate

import pytest


def test_create_target_gene(client):
    name = "UBE2I"
    category = "Regulatory"
    external_identifiers = [{"identifier": {"dbName": "Ensembl", "identifier": "ENSG00000103275"}, "offset": 1}]
    target_sequence = {
        "sequenceType": "dna",
        "sequence": "ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGA"
        "TGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAA"
        "TGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTGTTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAAT"
        "GACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACAC"
        "TGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGG"
        "AACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGCAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTA"
        "CTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTAT"
        "TGCTGATAAATCTGGAGCCGGTGAGCGTGGGTCTCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGA"
        "CGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA",
    }
    externalIdentifier = TargetGeneCreate(
        name=name,
        category=category,
        external_identifiers=external_identifiers,
        target_sequence=target_sequence,
    )
    assert externalIdentifier.name == "UBE2I"
    assert externalIdentifier.category == "Regulatory"


def test_create_invalid_category(client):
    name = "UBE2I"
    invalid_category = "invalid name"
    external_identifiers = [{"identifier": {"dbName": "Ensembl", "identifier": "ENSG00000103275"}, "offset": 0}]
    target_sequence = {
        "sequenceType": "dna",
        "sequence": "ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGA"
        "TGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAA"
        "TGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTGTTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAAT"
        "GACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACAC"
        "TGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGG"
        "AACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGCAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTA"
        "CTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTAT"
        "TGCTGATAAATCTGGAGCCGGTGAGCGTGGGTCTCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGA"
        "CGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA",
    }
    with pytest.raises(ValueError) as exc_info:
        TargetGeneCreate(
            name=name,
            category=invalid_category,
            external_identifiers=external_identifiers,
            target_sequence=target_sequence,
        )
    assert (
        "invalid name is not a valid target category. Valid categories are Protein coding, Regulatory, and Other"
        " noncoding" in str(exc_info.value)
    )


def test_create_invalid_sequence_type(client):
    name = "UBE2I"
    category = "Regulatory"
    external_identifiers = [{"identifier": {"dbName": "Ensembl", "identifier": "ENSG00000103275"}, "offset": 0}]
    target_sequence = {
        "sequenceType": "dnaa",
        "sequence": "ATGAGTATTCAACATTTCCGTGTCGCCCTTATTCCCTTTTTTGCGGCATTTTGCCTTCCTGTTTTTGCTCACCCAGAAACGCTGGTGAAAGTAAAAGA"
        "TGCTGAAGATCAGTTGGGTGCACGAGTGGGTTACATCGAACTGGATCTCAACAGCGGTAAGATCCTTGAGAGTTTTCGCCCCGAAGAACGTTTTCCAA"
        "TGATGAGCACTTTTAAAGTTCTGCTATGTGGCGCGGTATTATCCCGTGTTGACGCCGGGCAAGAGCAACTCGGTCGCCGCATACACTATTCTCAGAAT"
        "GACTTGGTTGAGTACTCACCAGTCACAGAAAAGCATCTTACGGATGGCATGACAGTAAGAGAATTATGCAGTGCTGCCATAACCATGAGTGATAACAC"
        "TGCGGCCAACTTACTTCTGACAACGATCGGAGGACCGAAGGAGCTAACCGCTTTTTTGCACAACATGGGGGATCATGTAACTCGCCTTGATCGTTGGG"
        "AACCGGAGCTGAATGAAGCCATACCAAACGACGAGCGTGACACCACGATGCCTGCAGCAATGGCAACAACGTTGCGCAAACTATTAACTGGCGAACTA"
        "CTTACTCTAGCTTCCCGGCAACAATTAATAGACTGGATGGAGGCGGATAAAGTTGCAGGACCACTTCTGCGCTCGGCCCTTCCGGCTGGCTGGTTTAT"
        "TGCTGATAAATCTGGAGCCGGTGAGCGTGGGTCTCGCGGTATCATTGCAGCACTGGGGCCAGATGGTAAGCCCTCCCGTATCGTAGTTATCTACACGA"
        "CGGGGAGTCAGGCAACTATGGATGAACGAAATAGACAGATCGCTGAGATAGGTGCCTCACTGATTAAGCATTGGTAA",
    }
    with pytest.raises(ValueError) as exc_info:
        TargetGeneCreate(
            name=name,
            category=category,
            external_identifiers=external_identifiers,
            target_sequence=target_sequence,
        )
    assert f"'{target_sequence['sequenceType']}' is not a valid sequence type" in str(exc_info.value)


def test_create_not_match_sequence_and_type(client):
    name = "UBE2I"
    category = "Regulatory"
    external_identifiers = [{"identifier": {"dbName": "Ensembl", "identifier": "ENSG00000103275"}, "offset": 0}]
    target_sequence = {"sequenceType": "dna", "sequence": "ARCG"}
    with pytest.raises(ValueError) as exc_info:
        TargetGeneCreate(
            name=name,
            category=category,
            external_identifiers=external_identifiers,
            target_sequence=target_sequence,
        )
    assert f"invalid {target_sequence['sequenceType']} sequence provided" in str(exc_info.value)


def test_create_invalid_sequence(client):
    name = "UBE2I"
    category = "Regulatory"
    external_identifiers = [{"identifier": {"dbName": "Ensembl", "identifier": "ENSG00000103275"}, "offset": 0}]
    target_sequence = {"sequenceType": "dna", "sequence": "AOCG%"}
    with pytest.raises(ValueError) as exc_info:
        TargetGeneCreate(
            name=name,
            category=category,
            external_identifiers=external_identifiers,
            target_sequence=target_sequence,
        )
    assert f"invalid {target_sequence['sequenceType']} sequence provided" in str(exc_info.value)

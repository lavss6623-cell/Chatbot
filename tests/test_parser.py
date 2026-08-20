from src.tnea_search import TNEASearch
from src.query_parser import TNEAQueryParser


def create_parser():
    search = TNEASearch()
    return TNEAQueryParser(search)


def test_parse_cse_bc_cutoff():
    parser = create_parser()

    result = parser.parse(
        "I got 187 cutoff and I'm BC. I want CSE."
    )

    assert result["cutoff"] == 187.0
    assert result["community"] == "BC"
    assert result["branch"] == "cse"


def test_parse_ece_mbc_cutoff():
    parser = create_parser()

    result = parser.parse(
        "My cutoff is 190 and I'm MBC. I want ECE."
    )

    assert result["cutoff"] == 190.0
    assert result["community"] == "MBC"
    assert result["branch"] == "ece"


def test_parse_it_sc_decimal_cutoff():
    parser = create_parser()

    result = parser.parse(
        "I scored 175.5 and I'm SC, can I get IT?"
    )

    assert result["cutoff"] == 175.5
    assert result["community"] == "SC"
    assert result["branch"] == "it"


def test_parse_short_form_query():
    parser = create_parser()

    result = parser.parse(
        "187 BC CSE"
    )

    assert result["cutoff"] == 187.0
    assert result["community"] == "BC"
    assert result["branch"] == "cse"


def test_parse_mechanical_oc_decimal_cutoff():
    parser = create_parser()

    result = parser.parse(
        "My cutoff is 192.5, OC, looking for Mechanical."
    )

    assert result["cutoff"] == 192.5
    assert result["community"] == "OC"
    assert result["branch"] == "mechanical"


def test_parse_aids_mbc_cutoff():
    parser = create_parser()

    result = parser.parse(
        "I got 180 marks in MBC and want AIDS."
    )

    assert result["cutoff"] == 180.0
    assert result["community"] == "MBC"
    assert result["branch"] == "aids"


def test_parse_eee_st_decimal_cutoff():
    parser = create_parser()

    result = parser.parse(
        "I scored 185.5 and I belong to ST. I want EEE."
    )

    assert result["cutoff"] == 185.5
    assert result["community"] == "ST"
    assert result["branch"] == "eee"


def test_parse_empty_input():
    parser = create_parser()

    result = parser.parse("")

    assert result == {
        "cutoff": None,
        "community": None,
        "branch": None,
        "district": None,
    }


def test_parse_whitespace_input():
    parser = create_parser()

    result = parser.parse("   ")

    assert result == {
        "cutoff": None,
        "community": None,
        "branch": None,
        "district": None,
    }
from re import search

import pandas as pd

from src.tnea_search import TNEASearch

import pytest


def create_search():
    search = TNEASearch()

    print("\nDEBUG CLASS:", TNEASearch)
    print("DEBUG MODULE:", TNEASearch.__module__)
    print("DEBUG HAS COMPARE:", hasattr(TNEASearch, "compare_colleges"))
    print("DEBUG DICT:", TNEASearch.__dict__.keys())

    return search


def test_college_search():
    search = create_search()

    results = search.search_college("Anna University")

    assert isinstance(results, pd.DataFrame)
    assert not results.empty


def test_branch_search():
    search = create_search()

    results = search.search_branch("computer science")

    assert isinstance(results, pd.DataFrame)
    assert not results.empty


def test_community_cutoff():
    search = create_search()

    result = search.get_community_cutoff(
        "Anna University",
        "COMPUTER SCIENCE AND ENGINEERING",
        "BC"
    )

    assert isinstance(result, pd.DataFrame)
    assert not result.empty


def test_colleges_by_cutoff():
    search = create_search()

    results = search.colleges_by_cutoff(
        cutoff=187,
        community="BC",
        branch="CSE"
    )

    assert isinstance(results, pd.DataFrame)
    assert not results.empty


def test_colleges_by_cutoff_contains_expected_columns():
    search = create_search()

    results = search.colleges_by_cutoff(
        cutoff=187,
        community="BC",
        branch="CSE"
    )

    # These are the important fields needed by the
    # recommendation layer.
    assert "college_name" in results.columns
    assert "branch" in results.columns


def test_recommend_colleges():
    search = create_search()

    recommendations = search.recommend_colleges(
        cutoff=187,
        community="BC",
        branch="CSE",
        district="Coimbatore",
        limit=10
    )

    assert isinstance(recommendations, pd.DataFrame)
    assert not recommendations.empty


def test_recommendation_limit():
    search = create_search()

    recommendations = search.recommend_colleges(
        cutoff=187,
        community="BC",
        branch="CSE",
        district="Coimbatore",
        limit=10
    )

    assert len(recommendations) <= 10


def test_recommendations_match_requested_district():
    search = create_search()

    recommendations = search.recommend_colleges(
        cutoff=187,
        community="BC",
        branch="CSE",
        district="Coimbatore",
        limit=10,
    )

    assert not recommendations.empty

    assert (
        recommendations["district"].str.lower()
        == "coimbatore"
    ).all()
    search = create_search()

    student_cutoff = 154

    recommendations = search.recommend_colleges(
        cutoff=student_cutoff,
        community="OC",
        branch="CSE",
        district="Coimbatore",
        limit=10
    )

    if not recommendations.empty:

        assert "margin" in recommendations.columns
        assert "category" in recommendations.columns

    
@pytest.mark.parametrize(
    "cutoff, community, branch , district",
    [
    (154, "OC", "CSE", "Coimbatore"),
    (190, "MBC", "ECE", "Salem"),
    (175.5, "SC", "IT", "Chennai"),
    (192.5, "OC", "Mechanical", "Madurai"),
    (180, "MBC", "AIDS", "Salem"),
    (185.5, "ST", "EEE", "Coimbatore"),
]
)
 
def test_recommendations_for_multiple_profiles(
    cutoff,
    community,
    branch,
    district,
):
    search = create_search()

    recommendations = search.recommend_colleges(
        cutoff=cutoff,
        community=community,
        branch=branch,
        district=district,
        limit=10,
    )

    assert isinstance(
        recommendations,
        pd.DataFrame,
    )

    assert len(recommendations) <= 10

    if not recommendations.empty:

        # Correct branch
        assert (
            recommendations["branch"]
            == search.resolve_branch(branch)
        ).all()

        # Correct district
        assert (
            recommendations["district"].str.lower()
            == district.lower()
        ).all()

        # Historical cutoff must not exceed student's cutoff
        assert (
            recommendations["cutoff"]
            <= cutoff
        ).all()

        # Required fields
        assert "college_name" in recommendations.columns
        assert "college_code" in recommendations.columns
        assert "branch" in recommendations.columns
        assert "district" in recommendations.columns
        assert "cutoff" in recommendations.columns
        
def test_recommendation_cutoff_does_not_exceed_student_cutoff():
    search = create_search()

    student_cutoff = 187

    recommendations = search.recommend_colleges(
        cutoff=student_cutoff,
        community="BC",
        branch="CSE",
        district="Coimbatore",
        limit=10,
    )

    assert not recommendations.empty

    assert (
        recommendations["cutoff"]
        <= student_cutoff
    ).all()

def test_get_college_by_code():
    search = create_search()

    results = search.get_college_by_code(1)

    assert isinstance(results, pd.DataFrame)
    assert not results.empty
    assert (results["college_code"] == 1).all()


def test_get_college_by_code_invalid():
    search = create_search()

    results = search.get_college_by_code(999999)

    assert isinstance(results, pd.DataFrame)
    assert results.empty


def test_compare_colleges():
    search = create_search()

    results = search.compare_colleges(
        1,
        4,
        "CSE",
        "BC"
    )

    assert isinstance(results, pd.DataFrame)
    assert len(results) == 2

    assert set(results["college_code"]) == {1, 4}

    assert (
        results["branch"]
        == search.resolve_branch("CSE")
    ).all()

    assert (
        results["community"] == "BC"
    ).all()

    assert "cutoff" in results.columns


def test_compare_colleges_invalid_code():
    search = create_search()

    results = search.compare_colleges(
        1,
        999999,
        "CSE",
        "BC"
    )

    assert isinstance(results, pd.DataFrame)
    assert results.empty


def test_compare_colleges_invalid_community():
    search = create_search()

    with pytest.raises(ValueError):
        search.compare_colleges(
            1,
            4,
            "CSE",
            "XYZ"
        )


def test_compare_colleges_unavailable_branch():
    search = create_search()

    results = search.compare_colleges(
        1,
        2,
        "CSE",
        "BC"
    )

    assert isinstance(results, pd.DataFrame)
    assert results.empty

def test_search_district():
    search = create_search()

    results = search.search_district("Coimbatore")

    assert isinstance(results, pd.DataFrame)
    assert not results.empty
    assert "college_code" in results.columns
    assert "college_name" in results.columns
    assert "district" in results.columns


def test_search_district_case_insensitive():
    search = create_search()

    upper = search.search_district("COIMBATORE")
    lower = search.search_district("coimbatore")

    assert len(upper) == len(lower)
    assert len(upper) == 54


def test_search_district_invalid():
    search = create_search()

    results = search.search_district("XYZ")

    assert isinstance(results, pd.DataFrame)
    assert results.empty


def test_search_district_no_duplicate_colleges():
    search = create_search()

    results = search.search_district("Coimbatore")

    assert results["college_code"].is_unique

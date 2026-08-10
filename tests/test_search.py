from src.tnea_search import TNEASearch


search = TNEASearch()


# ==================================================
# TEST 1: COLLEGE SEARCH
# ==================================================

print("\n==============================")
print("COLLEGE SEARCH")
print("==============================")

colleges = search.search_college(
    "Anna University"
)

print(
    colleges.head(10).to_string(
        index=False
    )
)


# ==================================================
# TEST 2: BRANCH SEARCH
# ==================================================

print("\n==============================")
print("BRANCH SEARCH")
print("==============================")

branches = search.search_branch(
    "computer science"
)

print(
    branches.head(10).to_string(
        index=False
    )
)


# ==================================================
# TEST 3: COMMUNITY CUTOFF
# ==================================================

print("\n==============================")
print("COMMUNITY CUTOFF")
print("==============================")

cutoff = search.get_community_cutoff(
    "Anna University",
    "COMPUTER SCIENCE AND ENGINEERING",
    "BC"
)

print(
    cutoff.to_string(
        index=False
    )
)


# ==================================================
# TEST 4: COLLEGES FOR STUDENT
# ==================================================

print("\n==============================")
print("COLLEGES FOR STUDENT")
print("==============================")

results = search.colleges_by_cutoff(
    cutoff=187,
    community="BC",
    branch="CSE"
)


print(
    results.head(10).to_string(
        index=False
    )
)

# ==================================================
# TEST 5: RECOMMENDATIONS
# ==================================================

print("\n==============================")
print("RECOMMENDATIONS")
print("==============================")

recommendations = search.recommend_colleges(
    cutoff=187,
    community="BC",
    branch="CSE",
    limit=10
)

print(
    recommendations.to_string(
        index=False
    )
)
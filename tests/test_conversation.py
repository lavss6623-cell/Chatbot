from src.conversation import ConversationState


state = ConversationState()


print("INITIAL STATE:")
print(state)


state.update({
    "branch": "CSE"
})

print("\nAFTER BRANCH:")
print(state)


state.update({
    "cutoff": 187
})

print("\nAFTER CUTOFF:")
print(state)


state.update({
    "community": "BC"
})

print("\nAFTER COMMUNITY:")
print(state)


print("\nMISSING:")
print(
    state.missing_for_recommendation()
)
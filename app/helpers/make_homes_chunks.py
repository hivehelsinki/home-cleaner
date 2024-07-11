def make_homes_chunks(homes):
    chuncks = []
    for i in range(0, len(homes), 50):
        chuncks.append(homes[i : i + 50])

    return chuncks

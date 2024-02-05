# MyNeta.info data crawler/web crawler for data aggregation

- `candidate_scraper.py` has the code to parse the data from the cadidate URL
- `main.py` is the entry point which has the code crawl through all the districts in a state and retrieved candidate ID's and parses it with the cadidate_scraper supporter.
    - `parse1` has a speedup of approximately 2.5x when compared with `parse`
    - `tqdm` progress bar gives information about the estimated time it takes to parse one cadidate and all candidates. [learnt from previous experiences lol]
    - there are 2 progress bars. The 2nd one shows up after the first one ends.
        - green progress bar is for districts
        - red progress bar is for candidates

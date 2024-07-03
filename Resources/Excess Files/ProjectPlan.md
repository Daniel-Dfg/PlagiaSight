## __Phase 1 : data extraction and algorithms "brute applications"__

__Goals :__

1) extract the text data from a `.txt` doc
            - tokenization (text cleaning + dividing the text in single units)
            - Stop Word removal
            - Lemmatization
            - Getting the data in a certain structure (which one and why ?)
2) Apply a few simple algorithms on the given data (which ones and why?), and display the "barebones" results (without further interpretations or suggestions)
            - This must be applied to words only to keep this phase simple (e.g no lookup for synonyms across the texts and no sentence tone, length or structure analysis)
            
## __Phase 2 : expanding the database; basic web scraping__

__Goals :__

1) Basic text *understanding* and web scraping
            - getting the "keywords" of a text (its subject) to know what data to get on the web
            - Scraping the HTML data from a few preset sources (like Wikipedia)
            - Convert this data into useable stuff (phase 1 code will have to be adapdated)
            - Compare this to the input data
2) Refining the analysis; combining together the first few algorithms implemented in phase 1 to start drawing conclusions about the potential plagiarism.
        
## __Phase 3 : analysis refinement and graphical interface

__Goals :__

1) Make a GUI using `Qt`
2) Refine the analysis and make use of the aformentioned GUI to display more results, and in a more "visual" way too (diagrams... if it's useful)
    - "Refining the analysis" could mean;
        - Use more sophisticated methods to compare words themselves (like checking if someone used a synonym of a word, and implementing more comparison algorithms)
        - Include *sentence* analysis; length, punctuation usage, and structure (finding the Part Of Speech (POS) of each word, etc)
        - Drawing more elaborate conclusions about the similarities between texts by *linking* further our implemented algorithms
        - Warn the user when they provide a "bad" input: for instance, if their doc consists of only one sentence, there's no way to really tell if there's "plagiarism" between the input and the source. It must be told to the user.

## __Phase 4 : scraping the web further, and introduction to semiology (see Inspiring Project n°5)

__Goals :__

1) Scrap the web further by using not only predefind sites, but also some recent newspapers, blogs...
2) Bring the analysis system to its maximal precision by completing the system charged of analyzing sentences. For instance, tone, and structure should be further taken in consideration [a more precise idea of this will have to be found along the way]
3) Cross-examine the sites to see if the user plagiarized from several sites at a time (very hard, will probably not be done and is not a priority)
4) Using phase 4.2, refine the conclusions to the user by;
            - Showing them how they plagiarized; sentence structure ? synonym abuse ? etc. along with an example showing how they could've plagiarized from this or that site
            - Suggesting solutions, using our refined analysis.
            
This is not definitive. Several "inter-phases" of optimization, debugging, and User Experience (UX) improvement will have to be done, along with brainstorming sessions.

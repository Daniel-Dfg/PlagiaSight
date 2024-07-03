A brief description of existing plagiarism checkers, and how they can help one building their own.

These projects have been ordered to follow a hierarchical order in terms of "complexity" and number of plagiarism detection concepts unknown of us, but please keep in mind that this order is absolutely not to be *strictly*  followed. Jumping across these projects to find the right ideas for ours will be our goal here.

The remarks below are opinions at best, they were written to help us make this project rather than to critique others'. 

1) [Simple-Plagiarism-Chercker by **abhilampard**](https://github.com/abhilampard/Simple-Plagiarism-Checker/tree/master)

   __PROS__
    - Very simple detection methods; TF and cosine similarity (good to start with)
    - Basic usage of the `re` module, useful to learn about text conversions to lowercase and punctuation removal for instance
   
   __CONS__
    - Quite old and doesn't make the best usage of the data structures available in Python
    - Contains some fundemental flaws; unclear input feedback (~meaningless percentage because of using such basic computation methods), and faulty computation method for the TF
    
2) [PlagiarismRemover by **simranvolunesia**](https://github.com/simranvolunesia/PlagiarismRemover)

    __PROS__
    - Not a plagiarism detector, but gives ideas to actually detect plagiarism
    - simple, yet enlightening usage of the `nltk` library (tokenization, getting synonyms of a word, their Part of Speech (POS)... In essence, a great introduction to the power of this library

    __NEUTRAL__
    - To keep the program simple, the only way it "removes plagiarism" is by word subsitution with random synonyms; it keeps actual plagiarism really easy to detect. Could incentivize us to come up with other methods to evaluate the amount of plagiarized content (like text and sentence structure, tone...)

    __CONS__
    - Presence of bad programming practices that make the code harder to read than it should be, even for such a small project (such as the two functions `plagiarism_remover` and `plagiarism_removal` with almost clashing names, despite the fact that they are actually complementary and do not do the same thing)
    - Decent documentation, but lack of explaination over what the code itself does at times
    
3) [Plagiarism Checker by **mozzaart23**](https://github.com/Moozzaart23/PlagiarismChecker/tree/master)

   __PROS__
    - Slightly more advanced detection methods; TF-IDF (to span the analysis across multiple documents) and KL Divergence
    - Usage of interesting librairies: notably `pandas`, `numpy`, `nltk` (as well as `re`)
    - Project built over multiple files, effectively making the understanding of the whole easier for readers by making the overarching structure of the project clear
   
    __CONS__
    - The code is not always totally explicit and lacks comments
    
4) [Text-Mining by **ShreshthSaxena**](https://github.com/ShreshthSaxena/Text-Mining)
    
    __PROS__
    - An actual assignment for school/uni, it seems; could give us ideas to structure our code and project files rigorously
    - Usage of unseen concepts for us; similarity matrix, Jaccard index, hierarchical clustering, LSA (we'll probably not use all of these, since the "Text-Mining" projects allows an analysis on multiple docs at a time)
    - Heavy usage of aformentioned extern librairies
    - Simple reports about each phase of the assignment to give an idea of the results to obtain using these methods
    - Lots of sample data to work with; many iterations over a same subject (search engines here)

   __CONS__
   - Little to no explaination on *why* to use this or that concept in this or that order
   - Code often not explicit, little to no comments and unclear overarching structure among project files
   

5) [Writing-Styles-Classification-Using-Stylometric-Analysis by **Hassaan-Elahi**](https://github.com/Hassaan-Elahi/Writing-Styles-Classification-Using-Stylometric-Analysis)

    __PROS__
    - Not really a plagiarism checker, but a great source of ideas to analyze a text reinforced by a fleshed-out documentation
    - Extremely well documented, easy to use
    - The code itself is well commented
      
   __NEUTRAL__
    - Probably "too advanced" at our current level to fully understand; could be used to foreshadow certain concepts that we would discover along the making of this project
    

    

    

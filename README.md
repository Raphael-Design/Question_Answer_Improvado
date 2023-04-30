REQUIRED LIBRARIES

    #pip install pandas

    #pip install openpyxl

    #pip install selenium

    #pip install -U spacy

    #python -m spacy download en_core_web_sm

    #pip install transformers

    #pip install torch

HOW TO RUN

You can just run the question_processing.py file, and type on the terminal which question you want to make when requested and the answer will be saved as a JSON file in the same folder as the program.

OBSERVATION

The Document_Index_Maker.py file is only used for creating the "Document_Index_List.xlsx" which is an index of all the blog posts on the Improvado website (using web scraping) and should only be run if the blog post list needs to be updated.

This project contains a chromedriver in its folder, which can change according to the Chrome version of the user running the program.

HOW WELL DOES IT WORK

This Program generated interesting initial results, firstly it generates a list of blog posts related to the search that is placed at the end of the JSON and will lead the user to information that he is interested in, and the answer above it does give some information on the question made. However, it can still be significantly improved as it will be described below.

IMPROVEMENTS

The best improvement would be to train a specific model for this system instead of using a pre-trained one from PyTorch (That was only used for speeding up the creation), which would guarantee better answers for the user.

Another improvement that can be made is the division of the code in classes or files instead of blocks, which can be good for debugging and reusing the code and its parts on different applications.

Finally, an interface should be the final step for this project, as well as the implementation of a database, allowing for saving frequently asked questions and faster replies.

CONTACT

This Project was made by Raphael de Paula e Souza as a submission on the homework for Improvado ML Pipelines developer.

email: raphaelsouza2912@gmail.com

phone: +55 31 9 93249895

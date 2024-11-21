# Solemn oath
In the spirit of the challenge, I hereby swear that I will not use ChatGPT, Claude, or any other LLM to write any code in this fork.
(Although of course, I am no stranger to them)

# Reader's note
- I have marked with TODOs many of the 'next steps' that I did not have time to implement.

# Marking Criteria Comments
- **Functionality**: Does the classifier work as expected?
    - All local files are classified correctly
    - I have also added a few randomly selected examples from the top of Google image search to guard against overfitting
    - TODO: assess on external files
- **Scalability**: Can the classifier scale to new industries and higher volumes?
    - The containerisation means that, with an appropriate load balancer/API in front of the app, it could scale horizontally very easily
    - The selection of lightweight packages, and the minimisation of the container image both make the scaling process more lightweight
    - The emsemble methodology was designed with scalability to new use-cases in mind
- **Maintainability**: Is the codebase well-structured and easy to maintain?
    - Class interface and ensemble methodology support extensibility, can you think of a new classification approach? Add it!
    - I believe the structure of the constants file also lends itself to easy maintenance, including the filetype definition
- **Creativity**: Are there any innovative or creative solutions to the problem?
    - You decide!
- **Testing**: Are there tests to validate the service's functionality?
    - As ever, more tests would probably be better.
    - I have hooked up the existing tests to the new logic,
- **Deployment**: Is the classifier ready for deployment in a production environment?
    - Containerised
    - prod pixi environment

# Approach - Classifier
I have taken an ensemble approach, rather than placing all the eggs in a single basket, I let a few different targeted approaches 'vote' on the result. As long is the math is right, this can allows targeted algorithms (that are strong on a certain doc type) have higher influence when they are very confident.
- The EnsembleClassifier can be instantiated with any number of IndividualClassifiers
- Each IndividualClassifier adheres to the interface, and provides predictions with it's own methodology, e.g. face recognition.
- The probability is supplemented with a confidence in some cases
- The individual votes are collated by the EnsembleClassifier to find the strongest positive class score. TODO: implement negative class scoring
- An idea I would love to try (but ran out of time) would be to use Word2Vec embedding to assess the similarity of scraped words to the keywords

### Insights
- Don't put overdue emphasis on the filename, since it highly unreliabile in general. We can use it, but we should limit the confidence of results derived from it.

# Local development
### Non-pixi deps
The OCR library uses Google's tesseract model, which requires a java installation before use. https://tesseract-ocr.github.io/tessdoc/Installation.html

MacOs installation via brew:
```
brew install tesseract
```

Linux installation::
```
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```
### pixi deps
```
curl -fsSL https://pixi.sh/install.sh | bash
pixi shell
```

# Running the container locally
If using a Mac with Apple Silicon, please be aware that you will need to build and run the container while setting the platform, e.g.:

```
docker build . -t classifier --platform linux/amd64
docker run --rm -it --platform linux/amd64 classifier:latest
```

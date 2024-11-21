## Solemn oath
In the spirit of the challenge, I hereby swear that I will not use ChatGPT, Claude, or any other LLM to write any code in this fork. 
(Although of course, I am no stranger to them)

# Approach - Classifier

- I have taken an ensemble approach, rather than placing all the eggs in a single basket, I let a few different targeted approaches 'vote' on the result. As long is the math is right, this can allows targeted algorithms (that are strong on a certain doc type) have higher influence when they are very confident. 

### Insights
- Don't put overdue emphasis on the filename, since it highly unreliabile in general. We can use it, but we should limit the confidence of results derived from it.


## Marking Criteria
- **Functionality**: Does the classifier work as expected?
- **Scalability**: Can the classifier scale to new industries and higher volumes?
- **Maintainability**: Is the codebase well-structured and easy to maintain?
- **Creativity**: Are there any innovative or creative solutions to the problem?
- **Testing**: Are there tests to validate the service's functionality?
- **Deployment**: Is the classifier ready for deployment in a production environment?
    - Containerised
    - prod pixi environment  

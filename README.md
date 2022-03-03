# docker-nlp-paraphrase-summary-api
Docker image wrapping an API that provides summary of websites and paraphrases it.

Provides two endoints that can be used to summarize a website and to paraphrase sentences

## summarize website

`http://localhost:8000/summarize/`

`curl -X 'GET' \
  'http://localhost:8000/summarize/?url=https%3A%2F%2Fwww.bbc.com%2Ftravel%2Farticle%2F20220302-seychelles-bird-island-a-paradise-with-too-many-palm-trees&nrSentences=10' \
  -H 'accept: application/json'`

example (remember url encoding)

https://www.bbc.com/travel/article/20220302-seychelles-bird-island-a-paradise-with-too-many-palm-trees

```
import urllib.parse
urllib.parse.quote(url)
```

`http://localhost:8000/summarize/https%3A//www.bbc.com/travel/article/20220302-seychelles-bird-island-a-paradise-with-too-many-palm-trees`

returns:

"On Bird, there are no motorised vehicles and the airstrip must be checked for tortoises before planes receive permission to land. Most sooty terns only land when nesting and rearing their young. In the decade following 1895, Bird exported nearly 20,000 tons (20 million kg) of guano (bird droppings) as fertiliser to the sugarcane growers of Mauritius. Even the island's shape resembles a bird: if you look at a satellite image of Bird Island, it resembles in outline a coquettish dove adrift in the Indian Ocean. I If you stand on the northernmost tip of Bird Island, it can feel like you're looking at eternity: there is ocean as far as the eye can see. But in the past half-century, Bird tells a parallel story of natural renewal, one almost without peer in the world of birds. And it all has to do with the ultimate contradiction: Bird was once a tropical island with too many palm trees. In the other direction, north of Bird, the Indian Ocean is deep, wide and uninterrupted by any landfall all the way to the Arabian Peninsula. Half of the 180 people on board died; the other half made it to Bird Island. It can feel like stepping into one of those episodes when you travel to Bird."

## paraphrase

`http://localhost:8000/paraphrase/`

Returns None if no paraphrase found, otherwise the sentence

Example:
Artificial Intelligence will be the future

`curl -X 'GET' \
  'http://localhost:8000/paraphrase/Artificial%20Intelligence%20will%20be%20the%20future' \
  -H 'accept: application/json'`

returns:
"artificial intelligence is the future"
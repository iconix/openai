# @deephypebot
_Nadja Rhodes -- OpenAI Scholar Final Project_

## Description
_tl;dr- generating conditional song reviews on Twitter._

The [theme of my summer](https://iconix.github.io/dl/2018/06/03/project-ideation#finding-my-niche) as an OpenAI Scholar has been explorations around music + text. I find the language around music - manifested by hundreds of ["nice, small blogs"](https://www.theverge.com/2018/1/2/16840940/spotify-algorithm-music-discovery-mix-cds-resolution) on the internet - to be a deep and unique well of creative writing.

As such, my final project will pay homage to these labors of love on the web and attempt to **generate consistently good and entertaining new writing about songs, based on a set of characteristics about the song and knowledge of past human music writing**.

The project will culminate in a **Twitter bot (@deephypebot)** that will monitor other music feeds for songs and automatically generate thoughts/opinions/writing about the songs.

## Project Architecture

![Project architecture diagram](/media/deephypebot-architecture.svg)

### Training data

My training data consists of 35,000+ blog posts with writing about individual songs. The count started at about 80K post links from 5 years of popular songs on the music blog aggregator [Hype Machine](https://hypem.com/) - then I filtered for English, non-aggregated (i.e., excluding "round up"-style posts about multiple songs) posts about songs that can be found on Spotify. There was some additional attrition due to many post links no longer existing. I did some additional manual cleanup of symbols, markdown, and writing that I deemed _non_-reviews.

From there, I split the reviews into sentences, which are a good length for a _variational autoencoder_ (VAE) model to encode.

### Neural network

A _language model_ (LM) is an approach to generating text by estimating the probability distribution over sequences of linguistic units (characters, words, sentences). This project is centered around a _sequence-to-sequence variational autoencoder_ (seq2seq VAE) backbone that generates text with a _latent constraints generative adversarial network_ (LC-GAN) head that helps control aspects of the text generated.

The seq2seq VAE consists of an LSTM-based encoder and decoder, and once trained, the decoder can be used independently as a language model conditioned on latent space `z` (more on seq2seq VAEs [here](https://iconix.github.io/dl/2018/06/29/energy-and-vae#seq2seq-vae-for-text-generation)).

Then the LC-GAN can be used to fine-tune the input `z` to this LM to generate samples with specific attributes, such as realism or readability (more on the LC-GAN [here](https://iconix.github.io/dl/2018/07/28/lcgan)). It can also be used to condition generations on attributes like song audio features or artist genres.

### Making inference requests to the network

Once the neural network is trained and deployed, this project will use it to generate new writing conditioned on either [audio features](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/) or [genre](https://developer.spotify.com/documentation/web-api/reference/artists/get-artist/) information pulled from the Spotify API (depending on which conditioning seems to work better).

This will require detecting the song and artist discussed in tweets that show up on @deephypebot's timeline and then sending this information to Spotify. Then Spotify's response will be sent to the neural network.

### From samples to tweets

Text generation is [a notoriously messy affair](https://iconix.github.io/dl/2018/06/20/arxiv-song-titles#text-generation-is-a-messy-affair) where "you will not get quality generated text 100% of the time, even with a heavily-trained neural network." While much effort will be put into having as automated and clean a pipeline as possible, some human supervision is prudent.

Once generations for a new proposed tweet are available, an email will be sent to the human curator (me), who will select and lightly edit for grammar and such before releasing to @deephypebot for tweeting.

## Resources

**Reading...**
- "Starting an Open Source Project" by GitHub [[guide](https://opensource.guide/starting-a-project/)] - #oss
- "Rules of Machine Learning: Best Practices for ML Engineering" by Google [[guide](https://developers.google.com/machine-learning/guides/rules-of-ml/)] - #eng
- "Dockerizing a Python 3 Flask App Line-by-Line" by Zach Bloomquist [[guide](https://medium.com/bitcraft/dockerizing-a-python-3-flask-app-line-by-line-400aef1ded3a)] - #eng
- "Build Your Own Twitter Bots!" [[code](https://github.com/handav/twitter-bots)] [[video](https://egghead.io/courses/create-your-own-twitter-bots)] - #twitterbot
    - A class by fellow Scholar, [Hannah Davis](http://www.hannahishere.com/)!
- "Make-A-Twitter-Bot Workshop" by Allison Parrish [[guide](https://gist.github.com/aparrish/3ee64d07f0a00b08618a)] - #twitterbot
- Sohn, K., Yan, X., Lee, H. Learning Structured Output Representation using Deep Conditional Generative Models [CVAE [paper](http://papers.nips.cc/paper/5775-learning-structured-output-representation-using-deep-conditional-generative-models.pdf)] -[](http://papers.nips.cc/paper/5775-learning-structured-output-representation-using-deep-conditional-generative-models.pdf)#vae
- Bernardo, F., Zbyszynski, M., Fiebrink, R., Grierson, M. (2016). Interactive Machine Learning for End-User Innovation [[paper](http://research.gold.ac.uk/19767/)] - #onlinelearning

**Software…**
- [Quilt](https://quiltdata.com/) for versioning and deploying data
- [Tweepy](https://github.com/tweepy/tweepy) or [Twython   ](https://github.com/ryanmcgrath/twython) for Python Twitter API access

## Timeline

**August 3**: _Project dev spec + preliminary tasks; LC-GAN experiments towards better/controllable samples_

- Preliminary project tasks
    - Developer spec
    - Data cleaning and versioning; permanent train/test split
    - Genre collection from Spotify
    - Metric definitions; benchmarking/baselines
        - Perplexity
        - Using discriminators to measure accuracy? (real/fake, genre, etc.)
    - Chat with Natasha and Jesse about more sophisticated modeling for later weeks
- LC-GAN experiments
    - Experiment with solo discriminator vs joint: e.g., realism vs realism + readability/grammaticality
    - Investigate differences in training discriminator on Gaussian random z’s vs. sample-based z’s
    - Experiment with maximizing a single quality (e.g., sentiment) of a sample
    - Do balanced class labels matter?

**August 10**: _Twitter bot + production pipeline ready_

- What Twitter feeds to watch
- How to watch Twitter feeds for songs
- How to build a Twitter bot
    - Twitter API registration
- How to request audio features and genres from an app
    - Spotify API registration
- Hook up a dummy/heuristic model
- Post-processing agent
- Samples -&gt; Email pipeline
- Email -&gt; Tweet pipeline
- [Bonus] Likes -&gt; Model pipeline

**August 17**: _More sophisticated modeling_

- Experiments on conditioning VAE vs. LC-GAN on topic models (LDA), sentiment (deepmoji), audio features/genre...
    - Would be cool to demonstrate Bayesian techniques and understanding through LDA
- Retrain VAE with focus on reconstruction error (lower KL constraint σ)
- Time to get best samples possible
    - Fancier VAEs?

**August 24**: _End-to-end integrations_

- How to deploy a model
- Select and integrate final production model

**August 31**: _Project due_

## Mentor support
_Mentor: [Natasha Jaques](https://twitter.com/natashajaques)_

- Assistance in reasoning over neural net architecture decisions
- Connection to LC-GAN paper author, Jesse Engel, for queries
- Assistance in understanding how LDA works
- Assistance in debugging model training
- Suggestions for model enhancement

### _Follow my progress this summer with this blog's [#openai](https://iconix.github.io/tags/openai) tag, or on [GitHub](https://github.com/iconix/openai)._

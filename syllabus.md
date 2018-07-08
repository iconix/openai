# Motivation

Design my own syllabus for self-study during the program.

## _themes_: techniques in generative text; learning song representations; language/sequence modeling enhanced by reinforcement learning or GANs

[[OpenAI Scholars intro blog post](https://iconix.github.io/dl/2018/05/30/openai-scholar)]
[[Designing a syllabus blog post](https://iconix.github.io/dl/2018/06/03/project-ideation)]

# Week 1: Setup

## Get and understand data; set up environment; build an n-gram model as a ‘shallow’ baseline; read LSTM, seq2seq, PyTorch tutorials

[[June 8 blog post](https://iconix.github.io/dl/2018/06/08/scholar-week1)]

_Resources_:

1.  [_Deep Learning_](https://www.deeplearningbook.org/) book, chapter 5 (machine learning basics)
2.  _Speech and Language Processing book_, [chapter 4](https://web.stanford.edu/~jurafsky/slp3/4.pdf) (language modeling with n-grams)
3.  "The unreasonable effectiveness of Character-level Language Models (and why RNNs are still cool)" by Yoav Goldberg [[blog](http://nbviewer.jupyter.org/gist/yoavg/d76121dfde2618422139)]
4.  Deep Learning with PyTorch: A 60 Minute Blitz [[tutorial](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)]

_Optional_:

1.  "The Unreasonable Effectiveness of Recurrent Neural Networks" by Andrej Karpathy [[blog](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)]
2.  Goodman, J. (2001). _A Bit of Progress in Language Modeling_. [[paper](https://arxiv.org/abs/cs/0108005)]
3.  Practical PyTorch Series 1: RNNs for NLP [[tutorial](https://github.com/spro/practical-pytorch)]
    - Good recommended reading section as well
4.  _Speech and Language Processing_ book, [chapter 8](https://web.stanford.edu/~jurafsky/slp3/8.pdf) (neural networks and neural language models)

# Week 2: LSTMs, part 1

## Define metrics for evaluating language model (LM) output; train an RNN (LSTM) on some sequential text data

[[June 15 blog post](https://iconix.github.io/dl/2018/06/15/scholar-week2)]

_Resources_:

1.  [_Deep Learning_](http://www.deeplearningbook.org/) book, chapters 10 (sequence modeling) and 11 (practical methodology)
2.  Graves, A. (2013). _Generating sequences with recurrent neural networks_. [[paper](https://arxiv.org/abs/1308.0850)]
3.  Merity, S., Keskar, N. S., Socher, R (2017). _Regularizing and Optimizing LSTM Language Models_. [[paper](https://arxiv.org/abs/1708.02182)] [[code](https://github.com/salesforce/awd-lstm-lm)]
4.  PyTorch: Generating Names with a Character-Level RNN [[tutorial](https://pytorch.org/tutorials/intermediate/char_rnn_generation_tutorial.html)]
5.  Deep Learning for NLP with PyTorch [[tutorial](https://pytorch.org/tutorials/beginner/deep_learning_nlp_tutorial.html)]
6.  [_Natural Language Processing_](https://github.com/jacobeisenstein/gt-nlp-class/blob/master/notes/eisenstein-nlp-notes.pdf) book (draft), chapter 6 (language models)

_Optional_:

1.  course.fast.ai lessons [6](http://course.fast.ai/lessons/lesson6.html) (rnns) + [7](http://course.fast.ai/lessons/lesson7.html) (grus, lstms)
2.  Karpathy, A. (2015). _Visualizing and Understanding Recurrent Networks_. [[video](https://skillsmatter.com/skillscasts/6611-visualizing-and-understanding-recurrent-networks)] [[paper](https://arxiv.org/abs/1506.02078)]
3.  Colah, C. (2014). _Deep Learning, NLP, and Representations_. [[blog](http://colah.github.io/posts/2014-07-NLP-RNNs-Representations/)]
4.  Bengio, Y (2003). _A Neural Probabilistic Language Model_. [[blog](http://www.scholarpedia.org/article/Neural_net_language_models)] [[paper](http://www.jmlr.org/papers/volume3/bengio03a/bengio03a.pdf)]

# Week 3: LSTMs, part 2

## Modify the LSTM to take context as part of the input and see if text improves!

- Genres from Genius.com
- Audio features from [Spotify](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/)

[[June 22 blog post](https://iconix.github.io/dl/2018/06/22/scholar-week3)]

_Resources_:

1.  Learning song representations with [deep learning for structured data](http://www.fast.ai/2018/04/29/categorical-embeddings/)

**Fun extra blog post #1**: Train an LSTM on song titles and something stodgy, like deep learning paper titles

- Inspired by [‘AI scream for ice cream’](http://aiweirdness.com/post/173797162852/ai-scream-for-ice-cream) (aiweirdness generating metal band ice cream flavors)
- Related posts: [AIWeirdness: 'Generated ice cream flavors: now it’s my turn'](http://aiweirdness.com/post/173990761332/generated-ice-cream-flavors-now-its-my-turn); [Kottke: ‘Ask an Ice Cream Professional’](https://kottke.org/18/05/ask-an-ice-cream-professional-ai-generated-ice-cream-flavors); [Janelle’s Twitter thread on it](https://twitter.com/JanelleCShane/status/997190921958473729)


# Week 4: seq2seq

## Train a seq2seq model with VAE loss; compare to LSTM results

[[June 29 blog post](https://iconix.github.io/dl/2018/06/29/energy-and-vae)]

_Resources_:

1.  [_Deep Learning_](http://www.deeplearningbook.org/) book, chapter 14 (autoencoders)
2.  Sutskever, I., Vinyals, O., and Le, Q. V. (2014). _Sequence to sequence learning with neural networks_. [[paper](https://arxiv.org/abs/1409.3215)]
3.  Bowman, S. R., Vilnis, L., Vinyals, O., Dai, A.M., Jozefowicz, R., Bengio, S (2016). _Generating Sentences from a Continuous Space_. [[paper](https://arxiv.org/abs/1511.06349)]
4.  Introduction to Variational Autoencoders [[video](https://youtu.be/9zKuYvjFFS8)]
5.  course.fast.ai lesson [11](http://course.fast.ai/lessons/lesson11.html) (seq2seq, attention)

_Optional_:

1.  OpenAI: Generative Models [[blog](https://blog.openai.com/generative-models/)]
2.  Introducing Variational Autoencoders (in Prose and Code) [[blog](http://blog.fastforwardlabs.com/2016/08/12/introducing-variational-autoencoders-in-prose-and.html)]
3. Under the Hood of the Variational Autoencoder (in Prose and Code) [[blog](http://blog.fastforwardlabs.com/2016/08/22/under-the-hood-of-the-variational-autoencoder-in.html)]
4.  Kingma, D.P., Welling, M (2014). _Auto-Encoding Variational Bayes_. [[paper](https://arxiv.org/abs/1312.6114)]
5.  Practical PyTorch: Translation with a Sequence to Sequence Network and Attention [[tutorial](https://github.com/spro/practical-pytorch/blob/master/seq2seq-translation/seq2seq-translation-batched.ipynb)]

# Week 5: Classification and Attention

## Use LSTM-LM transfer learning to do classification; learn all about attention

[[July 6 blog post](https://iconix.github.io/dl/2018/07/06/not-enough-attention)]

_Resources_:

1.  Bahdanau, D., Cho, K., Bengio, Y (2014). _Neural Machine Translation by Jointly Learning to Align and Translate_. [[paper](https://arxiv.org/abs/1409.0473)]
2.  Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, L., Polosukhin, I (2017). _Attention Is All You Need_. [transformer [paper](https://arxiv.org/abs/1706.03762)] [[blog](https://ai.googleblog.com/2017/08/transformer-novel-neural-network.html)]
3.  course.fast.ai lesson [11](http://course.fast.ai/lessons/lesson11.html) (seq2seq, attention)
4.  Distill.pub: Attention and Augmented Recurrent Neural Networks [[blog](https://distill.pub/2016/augmented-rnns/)]

_Optional_:

1.  How to Visualize Your Recurrent Neural Network with Attention in Keras [[blog](https://medium.com/datalogue/attention-in-keras-1892773a4f22)]
2.  [textgenrnn](https://github.com/minimaxir/textgenrnn)

# Week 6: Model interpretability, part 1

## Compare attention-based method of interpretability to other more explicit methods:

- LIME/Anchor
- Input gradients
- Neural deletion
- "Seeing what a neuron sees" à la Karpathy's char-rnn [[blog](http://karpathy.github.io/2015/05/21/rnn-effectiveness/)] [[paper](https://arxiv.org/abs/1506.02078)]

_Resources_:

1.  Distill.pub: The Building Blocks of Interpretability [[blog](https://distill.pub/2018/building-blocks/)]
2.  DeepMind: Understanding deep learning through neuron deletion [[blog](https://deepmind.com/blog/understanding-deep-learning-through-neuron-deletion/)]
3.  Ross, A. S., Hughes, M. C., Doshi-Velez, F. _Right for the Right Reasons: Training Differentiable Models by Constraining their Explanations_. [input gradients [paper](https://arxiv.org/abs/1703.03717)]
4. "Many opportunities for discrimination in deploying machine learning systems" by Hal Daumé III [[blog](https://nlpers.blogspot.com/2018/06/many-opportunities-for-discimination-in.html)]
5. How neural networks learn - Part I: Feature Visualization [[video](https://www.youtube.com/watch?v=McgxRxi2Jqo)]

_Optional_:

1.  Ribeiro, M.T., Singh, S., Guestrin, C. _Why Should I Trust You?: Explaining the Predictions of Any Classifier_. [LIME [project](https://github.com/marcotcr/lime)] [[paper](https://arxiv.org/abs/1602.04938)]
2.  Ribeiro, M.T., Singh, S., Guestrin, C. _Anchors: High-Precision Model-Agnostic Explanations_. [Anchor [project](https://github.com/marcotcr/anchor)] [[paper](https://homes.cs.washington.edu/~marcotcr/aaai18.pdf)]
3. "Awesome Interpretable Machine Learning": an opinionated list of resources facilitating model interpretability (introspection, simplification, visualization, explanation) [[repo](https://github.com/lopusz/awesome-interpretable-machine-learning)]


# Week 7: Model interpretability, part 2

## Study forms of bias in my models

- Could start with selection bias from source text
- Inspect embeddings and latent dimensions, à la  [David Ha's World Models](https://worldmodels.github.io/)

_Resources_:
1.  Hardt, M., Price, E., Srebro, N. _Equality of Opportunity in Supervised Learning_. [[paper](https://arxiv.org/abs/1610.02413)]
2.  World Models: Can agents learn inside of their own dreams? [[demo](https://worldmodels.github.io/)]

_Optional_:

# Week 8: Advanced topics

## Improve model with RL or a GAN discriminator

_Resources_:

1.  [_Deep Learning_](http://www.deeplearningbook.org/) book, chapter 20 (deep generative models)
2.  Li, J., Monroe, W., Ritter, A., Galley, M., Gao, J., Jurafsky, D. _Deep Reinforcement Learning for Dialogue Generation_. [[paper](https://arxiv.org/abs/1606.01541)]
3.  Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A., and Bengio, Y. (2014). _Generative adversarial nets_. [[paper](https://arxiv.org/abs/1406.2661)]
4.  PyTorch: Reinforcement Learning (DQN) tutorial [[tutorial](https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html)]
5.  Yoav Goldberg. "Adversarial training for discrete sequences (like RNN generators) is hard" [[blog](https://medium.com/@yoav.goldberg/an-adversarial-review-of-adversarial-generation-of-natural-language-409ac3378bd7)]
6.  course.fast.ai lesson [12](http://course.fast.ai/lessons/lesson12.html) (gans) + [13](http://course.fast.ai/lessons/lesson13.html) (gans, style transfer)

_Optional_:

1.  Jaques, N., Gu, S., Bahdanau, D., Hernández-Lobato, J. M., Turner, R. E., Eck, D. _Tuning Recurrent Neural Networks with Reinforcement Learning_ [[blog](https://magenta.tensorflow.org/2016/11/09/tuning-recurrent-networks-with-reinforcement-learning/)] [[paper](https://arxiv.org/abs/1611.02796)]
2.  Arulkumaran, K., Deisenroth, M. P., Brundage, M., Bharath, A. A. _A Brief Survey of Deep Reinforcement Learning_. [[paper](https://arxiv.org/abs/1708.05866)]

**Fun extra blog post #2**: could digest Goldberg’s argument for why the “Adversarial Generation of Natural Language” paper isn’t worthwhile

- There was a bit of a [tweetstorm](https://twitter.com/yoavgo/status/872831207163265024) (that turned into a [blog post](https://medium.com/@yoav.goldberg/an-adversarial-review-of-adversarial-generation-of-natural-language-409ac3378bd7)) around Yoav Goldberg and his argument for why this "[Adversarial Generation of Natural Language](https://arxiv.org/abs/1705.10929)" paper is garbage, and why he is generally upset about deep learning practitioners coming to natural language and thinking they can “solve” it (particularly with GANs). Might be interesting to digest the debate in a blog post.
- Related posts: post comments like [Hu's](https://medium.com/@zhitinghu/we-thank-yoav-for-the-comments-on-our-vae-generation-paper-titled-as-controllable-text-generation-73d8c8058bb6) and [Bahdanau's](https://medium.com/@dzmitrybahdanau/in-general-i-dont-want-to-participate-in-public-holy-wars-so-i-will-make-just-two-points-7f41e075e81e); Goldberg’s [clarifications](https://medium.com/@yoav.goldberg/clarifications-re-adversarial-review-of-adversarial-learning-of-nat-lang-post-62acd39ebe0d); Yann LeCun’s [response](https://www.facebook.com/yann.lecun/posts/10154498539442143) to Goldberg; Goldberg’s [response](https://medium.com/@yoav.goldberg/a-response-to-yann-lecuns-response-245125295c02) to LeCun

_Note that the Week 8 project will lead directly into my final (4-week) project!_

# Final project ideas

## Music blog review generation

- Structured, topical, specific to attributes of the song (similar to ‘essay writing’ goals).
- Conditioned on song representation, source blog (?), sentiment...
    - Could choose a limited set of source blogs ("voices"): e.g., Pitchfork, most consistent blogger on HypeM Time Machine, etc.
- Datasets: blog scrape, Spotify API track [audio analysis](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/) and [audio features](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/), Genius API’s [song](https://docs.genius.com/#songs-h2) tags, description, lyrics

## Lyric generation

- Structured, topical, specific to attributes of the song. Genius annotate-ability as a measure of interesting-ness (?)
- Conditioned on song representation
- Datasets: [https://www.kaggle.com/rakannimer/billboard-lyrics](https://www.kaggle.com/rakannimer/billboard-lyrics), Spotify API track [audio analysis](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/) and [audio features](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/), Genius API’s [song](https://docs.genius.com/#songs-h2) tags, description

What do I mean by _song representation_? I want to encode data from the Spotify/Genius knowledge graph for the song (e.g., title, genre, similarity to other songs, audio features, lyrics, description...) and use it to condition/seed the generated text.

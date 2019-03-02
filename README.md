## N-gram Language Model

### Data
- train_shakespeare.txt (train file)
- dev_shakespeare.txt (test file)
- new_shakespeare.txt (generated file, based on bigram, beam size 30)

### Files
- main.py
- corpus.py
- lm.py
- beam.py
- test_ngram.py

### Model
- trained_model_ngram.pkl (Saved after training)

### Requirement
	`pip install docopt`
	`pip install click`


### How-to

`python
  main.py train [--n <n>] [--path <path>]
  main.py generate [--lines <n>] 
  main.py perplexity [--path <path>]
  main.py common [--number <n>]
  main.py testcase
  main.py --help`

`Options:
  --n <n>     		Number of n-gram
  --path <path>     Train/Test file path
  --lines <n>		No. of lines to be generated
  --number <n>		No. of n-gram to show
  --help     		Show this screen`

`python test_ngram.py`
# data_madness
Data Science Job Market

### Conda
Setup conda environment from file:
```
conda env create -f data_madness_env.yml
```

and then activate the environment as ususal:
```
conda activate data_madness
```

Before pushing code, if you have made changes to the environment, run the following:
```
conda env export > data_madness_env.yml
```

### Troubleshooting

#### 1. GoogleSearch import fails with conda environment

If an error occurs in
```
from serpapi import GoogleSearch
```

run
```
pip install google-search-results
```

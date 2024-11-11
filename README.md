# Engine DJ Utilities 

#### Some Utilities for [Engine DJ](https://enginedj.com/)

## How To Run

### MAKE SURE YOU MAKE A BACKUP OF THE 'Engine Library' FOLDER FIRST!

First, install the requirements. This should be done in a virtualenv.
This is done by running 

```pip install -r requirements.txt```

Each script has some help for each of the arguments. To see this, just run

```python <scriptname.py> --help```.

For example, to run the script which converts the energy IDv3 tag to rating on
Windows it would look something like 

```python energy-to-rating.py "C:\Users\<username>\Music\Engine Library"```

Now, when you open Engine DJ, all of the ratings should be filled in according
to the energy tag on your music files. If they don't have one, the rating is
left untouched.

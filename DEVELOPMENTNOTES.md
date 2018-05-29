

# Debuging

To install module locally without publishing a version:

```
###python3 setup.py sdist
python setup.py install
passwordmanpro_cli
```


# Release process

commit to git and check travis to ensure it is compiling properly.

```
git tag -l #find latest tag


git tag 0.0.1
python3 setup.py sdist
python3 setup.py register sdist upload
git push --tags
```


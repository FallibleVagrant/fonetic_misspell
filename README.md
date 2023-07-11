### fonetic_misspell

This Python script converts English text into IPA, then back again. Proper spelling is lost in translation.

Essentially:
>A pristine sentence like this, with nary a blemish.

becomes:
>a pressteen zentanss llaik diz, wed nerii a bllehmesh.

It uses the wonderful [English-to-IPA](https://github.com/mphilli/English-to-IPA) for its converting needs, which is itself based on the Carnegie-Mellon University Pronouncing Dictionary.
This script wouldn't exist without their work.

### Installation ### 

I've included a local copy of English-to-IPA that the project imports directly, so all you need is the Python interpreter if you want to mess around with it in the same directory.
If you want to use it in another environment, you'll want to install English-to-IPA as a module and uncomment the import statement at the top of fonetic_misspell.py.

### Notes ###

Once we have the input in IPA form, we replace each IPA symbol with a sound that approximates it, chosen randomly from a list we define.
A sample dictionary is provided for your scrutiny.

If a dictionary file is not supplied to fonetic_misspell, an internal default is used.

Words not in the CMU Pronouncing Dictionary are marked with an asterisk, and are significantly less transmogrified.
Capitalization is lost in translation.

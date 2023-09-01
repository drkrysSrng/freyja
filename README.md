<img align="left" height="70" src="doc/images/freyja.png" alt="freyja">

# FREYJA Obfuscation List of Tools

## Installation

* Creating virtual environment
```bash
cd dev
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

* We need to have pyinstaller:

```bash
pip install pyinstaller
```

* To create the binary:

```bash
pyinstaller -F freyja.py
```

* Then copy the binary to `/usr/local/bin`

```bash
cp dist/freyja /usr/local/bin/
```

## Usage
![usage](doc/images/usage.png)

### Entropy
* To get Shannon entropy, well use this option:
If we want to see the entropy line per line, we will see lines with an Entropy higher than 3.75, non-human writen.
```commandline
freyja -f filein.js -e line
```
![line_entropy](doc/images/line_entropy.png)

If we want to see the file entropy:
```commandline
freyja -f filein.js -e file
```
![file_entropy](doc/images/file_entropy.png)

### Deobfuscation tool

### Entropy
Based on Shannon Algorithm, I have made this tool in order to analyze files to check the probabilities of a file or the lines of a file to be obfuscated or not.
Usually the obfuscated code returns probability values higher than a **3.75**:

## Javascript Examples to test
git clone https://github.com/HynekPetrak/javascript-malware-collection.git


## MBA and OPAQUE examples
* Here we have some examples to test MBA and OPAQUE obfuscation techniques.


<img align="left" height="70" src="doc/images/freyja.png" alt="freyja">

# Freyja Deobfuscation Tool

## Installation

* Creating virtual environment
```bash
cd dev
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
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

### Javascript Desobfuscation
* To desobfuscate a JavaScript file, we use this command:
```commandline
python freyja -f ./samples/simple_js_malware_code/do_not_run.js -o output.js -l 2
freyja -f ./samples/simple_js_malware_code/do_not_run.js -o output.js -l 2
```
* `-f`: File to deobfuscate
* `-o`: The output file, if not, it will be out.js
* `-l`: Set the level 0..10
  * Level 0: All options 
  * Level 1: Just Beautify the File.
  * Level 2: Parse Hex numbers to String.
  * Level 3: Parse Unicode characters.
  * Level 4: Deobfuscate toString with numbers.
  * Level 5: Deobfuscate toString with Hex numbers.
  * Level 6: Deobfuscate Eval with a list of numbers.
  * Level 7: Deobfuscate unescape function inside chars.
  * Level 8: Deobfuscate char sets.
  * Level 9: Deobfuscate parseInt function.
  * Level 10: Append Chars.

### Base64 Search:
* To look for base64 strings and decode them:

```commandline
python freyja -b -f file.js -o output.json 
```

## Examples
```
python freyja.py -f do_not_run.js -e line
python freyja.py -f do_not_run.js -e file
python freyja.py -f ejercicio6.js -l 1
python freyja.py -f b122473d00566758d09c695d191b368e0c815c65e8acc0f00da7a88e45cc8a9e.js -l 2
python freyja.py -f /b122473d00566758d09c695d191b368e0c815c65e8acc0f00da7a88e45cc8a9e.js -l 3
python freyja.py -f simple_js_malware_code/do_not_run.js -l 4
python freyja.py -f simple_js_malware_code/do_not_run.js -l 5
python freyja.py -f .sample_2_extracted/sample_2.js -l 6
python freyja.py -f 20160311_01284d18e603522cc8bdabed57583bb3.js -l 7
python freyja.py -f freyja -f do_not_run.js -l 8
python freyja.py -f out.js -l 9 #out from 4
python freyja.py -f out.js -l 10
python freyja.py -b example.txt -o example.json
```
## MBA and OPAQUE examples
* Here we have some examples to test MBA and OPAQUE obfuscation techniques.

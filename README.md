# hacktivate
Hacktivates iPhones vulnerable to Checkm8 via the Checkra1n jailbreak.
# Notice
Currently this tool ONLY bypasses iCloud. Full hacktivation features are currently being looked into and should come eventually.

# Usage
To install the python dependencies you need pipenv. Read here: https://pypi.org/project/pipenv/

## After pipenv is installed
1. Open a terminal, and `cd` into the hacktivate directory.
2. Run `pipenv install`. This installs all the python libraries.
3. Run `pipenv shell`. This opens a pipenv interactive window.
4. Run `python hacktivate.py --install` to download the nessecary files.
5. Run `python hacktivate.py --hacktivate` to start the hacktivation process. If you're having trouble with SSH, run `python hacktivate.py --hacktivate --alternate`. This uses iProxy on port 44 instead 22.

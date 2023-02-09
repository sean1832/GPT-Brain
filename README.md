# Auto Setup
### What you need
- Install python `3.11`
- OpenAI API keys

### .bat file
1. Run `setup.bat`
2. Enter OpenAI API Key

# Manual Setup
### Python
1. Make sure to install python `3.11`
1. Create venv using `python -m venv venv` under root project root directory
2. Enter venv using `venv\Scripts\activate`
3. Update pip by using `python -m pip install --upgrade pip`
4. Installing required libraries using `pip3 install -r requirement.txt`

### API Key file
1. Create API Key file using cmd with command `if not exist .user\ (md .user\) & echo [YOUR API KEYS]> .user\API-KEYS.txt`



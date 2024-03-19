### Score CVs with OpenAI

#### Setup
- Create a virtual environment: `python3 -m venv venv`
- Start using venv: `source venv/bin/activate`
- Install dependencies: `pip3 install -r requirements.txt`
- Create a new file named `.env`
- Add `OPENAI_API_KEY` to `.env`
- Add `CV_FILES` to `.env`. This is the path to the folder containing the CV files to be scored.

#### Usage
- Add the CV files in the `CV_FILES` folder
- Run `python3 script.py`
- The results will be saved in `results.json`

#### Configurations
- Prompt related settings can be changed in `instructions.py`
- Script related settings can be changed in `settings.py`
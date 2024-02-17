## 💻 How to setup:

Install conda
```
link - https://youtu.be/-sNX_ZMVpQM?si=er4eYhsjyuF4vJ52
```

Generate OpenAI API key
```
link - https://www.youtube.com/watch?v=gBSh9JI28UQ
```

Open Anaconda terminal (for windows you can search "anaconda prompt" in the search bar) and type the following commands

Creating conda environment
```
conda create -p venv python==3.8 -y
```

activate conda environment
```
conda activate venv/    (for windows)

source activate venv/   (for linux)
```

Install requirements
```
pip install -r requirements.txt
```

API Key 
```
Replace the API key that you generated in config.py file
```

Run the code
```
python main.py
```

Go to http://127.0.0.1:5000 when the server is up
New file (interaction_history.json) will be created and you can see [user_quer, response] getting populated
# NetMotif

## Local Development Setup

Follow the steps below to set up the project for local development using [uv](https://github.com/astral-sh/uv):

### 1. Clone the Repository

Start by cloning this repository to your local machine:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Install `uv` if you don't have it

If you don't have uv installed, use one of the commands below, or refer [here](https://github.com/astral-sh/uv?tab=readme-ov-file#installation):

```bash
# On macOS and Linux.
$ curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows.
$ powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip.
$ pip install uv
```

### 3. Activate the Virtual Environment

```bash
# On MacOS and Linux.
$ source .venv/bin/activate

# On Windows.
$ .venv\Scripts\activate
```

### 4. Install Project Dependencies

```bash
uv sync
```

### 5. Run the Streamlit App

```bash
streamlit run app.py
```

This will launch the app, and you can access it by navigating to http://localhost:8501 in your browser.

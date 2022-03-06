# Pollination Apps

A python library to setup and deploy Apps to Pollination!

## Installation

```
> pip install pollination-apps
```

## Documentation

You can access the full docs for this package and its CLI
[here](https://pollination.github.io/pollination-apps/).

## Local Development

1. Clone this repo locally

   ```console
   git clone git@github.com:ladybug-tools/pollination-apps
   ```

   or

   ```console
   git clone https://github.com/ladybug-tools/pollination-apps
   ```

2. Install dependencies:

   ```console
   cd pollination-apps
   pip install -r dev-requirements.txt
   pip install -r requirements.txt
   ```

3. Run Tests:

   ```console
   python -m pytest tests/
   ```

4. Generate Documentation:

   ```python
   sphinx-apidoc -f -e -d 4 -o ./docs/modules ./pollination-apps
   sphinx-build -b html ./docs ./docs/_build
   ```

5. Preview Documentation:

   ```console
   python -m http.server --directory ./docs/_build/
   ```

   Now you can see the documentation preview at http://localhost:8000

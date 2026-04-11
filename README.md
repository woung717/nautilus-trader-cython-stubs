# Type stubs for NautilusTrader

<img width="1792" height="846" alt="image" src="https://github.com/user-attachments/assets/efbaadb8-0103-4b74-bc00-fac456e95e57" />

`nautilus-trader-cython-stubs` provides **`.pyi` type stubs** for the [NautilusTrader](https://github.com/nautechsystems/nautilus_trader) trading platform, specifically for its **Cython interface**.

These stubs serve the following purposes:

- Enhance **IntelliSense and docstring support** in **Visual Studio Code** (via Pylance) and other IDEs  
- Provide consistent **type annotations** and **docstring visibility** for Cython modules  
- Enable proper **import resolution** for Cython-based APIs 

## Installation

**Installation script**

Run `install.py` python script with your installed `nautilus_trader` directory (e.g. `{python_path}/lib/{python_version}/site-packages/nautilus_trader/`)

```bash
python ./install.py {python_path}/lib/{python_version}/site-packages/nautilus_trader
```

**OS Command**

Copy all files under the `stubs` directory into your installed `nautilus_trader` directory (e.g. `{python_path}/lib/{python_version}/site-packages/nautilus_trader/`) using `rsync` or any other tool, so that the `.pyi` stubs are located next to their corresponding Cython `.pyx` files. 

```bash
rsync -a ./stubs/ {path/to/python/site-packages}/nautilus_trader
```

## Validate stubs
To check if the current version of the .pyi stub is synchronized with the NautilusTrader API, run the following command:
 
```bash
cd nautilus-trader
git checkout {branch_name|tag_name} # branch or tag(release) of nautilus_trader 
cd ..
./scripts/validate_stubs.sh
```

Note: Python3 and Cython dependencies are required.

## AI Stub generation/fix (OpenRouter Account required)
To synchronized with the NautilusTrader API using AI, run the follwing command:

```bash
cd nautilus-trader
git checkout {branch_name|tag_name} # branch or tag(release) of nautilus_trader 
cd ..
python ./scripts/stub_agent.py # OpenRouter API Key setup required using env
```
Though the AI model can resolve most inconsistencies, some import parts should be checked and fixed manually by the developer.

## Limitations

- The stubs are **manually maintained** and may **lag behind** implementation changes. 
- If you find anything missing or inconsistent with the current API, feel free to [create an issue](https://github.com/woung717/nautilus-trader-cython-stubs/issues).
- These stubs cover only the Cython interface — upcoming Rust bindings are not included.


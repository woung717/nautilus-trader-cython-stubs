# Type stubs for NautilusTrader

`nautilus-trader-cython-stubs` provides **`.pyi` type stubs** for the [NautilusTrader](https://github.com/nautechsystems/nautilus_trader) trading platform, specifically for its **Cython interface**.

These stubs serve the following purposes:

- **IntelliSense and docstring support** in **Visual Studio Code** (via Pylance) and other IDEs  
- **import resolution** for Cython-based APIs 

## Installation
Copy all files under the `stubs` directory into your installed `nautilus_trader` directory (e.g. `{python_path}/lib/{python_version}/site-packages/nautilus_trader/`) using `rsync` or any other tool, so that the `.pyi` stubs are located next to their corresponding Cython `.pyx` files. 

For example:
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

## Limitations

- The stubs are **manually maintained** and may **lag behind** implementation changes. 
- If you find anything missing or inconsistent with the current API, feel free to [create an issue](https://github.com/woung717/nautilus-trader-cython-stubs/issues).
- These stubs cover only the Cython interface — upcoming Rust bindings are not included.


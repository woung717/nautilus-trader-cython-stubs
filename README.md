# nautilus-trader-cython-stubs: Type stubs for NautilusTrader

`nautilus-trader-cython-stubs` provides **`.pyi` type stubs** for the [NautilusTrader](https://github.com/nautechsystems/nautilus_trader) trading platform, specifically for its **Cython interface**.

These stubs serve the following purposes:

- Enhance **IntelliSense and docstring support** in **Visual Studio Code** (via Pylance) and other IDEs  
- Provide consistent **type annotations** and **docstring visibility** for Cython modules  
- Enable proper **import resolution** for Cython-based APIs (which is almost entire APIs)

## Usage

Copy all files under the `stubs` directory into your installed `nautilus_trader` directory (e.g. `{python_path}/lib/{python_version}/site-packages`) using `rsync` or any other tool, so that the `.pyi` stubs are located next to their corresponding Cython `.pyx` files.

## Limitations

- The stubs are **manually maintained** and may **lag behind** implementation changes. 
- If you find anything missing or inconsistent with the current API, feel free to [create an issue](https://github.com/woung717/nautilus-trader-cython-stubs/issues).
- These stubs cover only the Cython interface — upcoming Rust bindings are not included.


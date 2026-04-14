#!/usr/bin/env python3
"""
AI Agent for generating and iteratively fixing nautilus-trader Cython stubs.

Workflow per .pyx file:
  1. Generate .pyi stub via LLM (if it doesn't exist or --overwrite is set)
  2. Run validate_stub.py – check output for "All validations passed!"
  3. If validation fails, extract only the problematic sections and ask the
     LLM to fix them using tool calls (str_replace_in_file / insert_edit_into_file)
  4. Repeat up to --max-retries times

Usage:
    python scripts/stub_agent.py [--model MODEL] [--max-retries N]
                                  [--pyx-file PATH] [--overwrite] [-v]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import traceback
from dataclasses import dataclass
from glob import glob
from pathlib import Path
from typing import Any

import litellm


# =============================================================================
# Config - Centralized configuration values
# =============================================================================

@dataclass(frozen=True)
class Config:
    """Centralized configuration for the stub agent."""
    
    # Paths
    MODULE_PATH: str = "nautilus_trader/nautilus_trader/"
    STUB_PATH: str = "stubs/"
    SYMBOL_FILE: str = "nautilus_trader/nautilus_trader/core/nautilus_pyo3.pyi"
    
    # Validation
    VALIDATION_SUCCESS: str = "All validations passed!"
    
    # Model settings
    DEFAULT_MODEL: str = "openrouter/qwen/qwen3.5-plus-02-15"  #"openrouter/openai/gpt-4o"
    DEFAULT_MAX_RETRIES: int = 3
    
    # Fix loop parameters
    CONTEXT_LINES: int = 25  # lines of context around each error location
    MAX_TOOL_CALLS: int = 50  # guard against runaway tool-call loops


# =============================================================================
# ToolRegistry - Manages tool definitions and dispatch for LLM tool calls
# =============================================================================

class ToolRegistry:
    """Registry for LLM tool definitions and their implementations."""
    
    def __init__(self, project_root: Path) -> None:
        self._project_root = project_root
        self._tools: list[dict[str, Any]] = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": (
                        "Read a section of a file with line numbers for context. "
                        "Optionally restrict to start_line..end_line (1-indexed)."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the file (absolute or relative to project root).",
                            },
                            "start_line": {
                                "type": "integer",
                                "description": "First line to read (1-indexed, default: 1).",
                            },
                            "end_line": {
                                "type": "integer",
                                "description": "Last line to read (1-indexed, default: end of file).",
                            },
                        },
                        "required": ["file_path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "str_replace_in_file",
                    "description": (
                        "Replace an exact, unique string in a file with new content. "
                        "old_string must appear exactly once. Prefer this for precise, "
                        "targeted edits (e.g. fixing a single method signature)."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the file to edit.",
                            },
                            "old_string": {
                                "type": "string",
                                "description": "The exact text to find. Must be unique in the file.",
                            },
                            "new_string": {
                                "type": "string",
                                "description": "The replacement text.",
                            },
                        },
                        "required": ["file_path", "old_string", "new_string"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "insert_edit_into_file",
                    "description": (
                        "Replace a range of lines (start_line..end_line inclusive, 1-indexed) "
                        "with new_content. Use when the replacement involves multiple lines or "
                        "when str_replace_in_file would produce an ambiguous match."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to the file to edit.",
                            },
                            "start_line": {
                                "type": "integer",
                                "description": "First line to replace (1-indexed, inclusive).",
                            },
                            "end_line": {
                                "type": "integer",
                                "description": "Last line to replace (1-indexed, inclusive).",
                            },
                            "new_content": {
                                "type": "string",
                                "description": "Text to insert in place of the specified lines.",
                            },
                        },
                        "required": ["file_path", "start_line", "end_line", "new_content"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "diff",
                    "description": (
                        "Compute a unified diff between original and modified text. "
                        "Useful for previewing changes before committing them."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "original": {"type": "string", "description": "Original text."},
                            "modified": {"type": "string", "description": "Modified text."},
                            "filename": {
                                "type": "string",
                                "description": "Filename label for the diff header (optional).",
                            },
                        },
                        "required": ["original", "modified"],
                    },
                },
            },
        ]
    
    @property
    def tools(self) -> list[dict[str, Any]]:
        """Return the list of tool definitions for LLM."""
        return self._tools
    
    def _resolve(self, file_path: str) -> Path:
        """Resolve a file path relative to PROJECT_ROOT if not absolute."""
        p = Path(file_path)
        return p if p.is_absolute() else self._project_root / p
    
    def execute(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        """Execute a tool call by name with the given arguments."""
        dispatch: dict[str, Any] = {
            "read_file": self._tool_read_file,
            "str_replace_in_file": self._tool_str_replace_in_file,
            "insert_edit_into_file": self._tool_insert_edit_into_file,
            "diff": self._tool_diff,
        }
        fn = dispatch.get(name)
        if fn is None:
            return {"error": f"Unknown tool: {name}"}
        try:
            return fn(**args)  # type: ignore[call-arg]
        except TypeError as exc:
            return {"error": f"Bad arguments for {name}: {exc}"}
    
    def _tool_read_file(
        self,
        file_path: str,
        start_line: int = 1,
        end_line: int | None = None,
    ) -> dict[str, Any]:
        """Read a section of a file with line numbers."""
        path = self._resolve(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        lines = path.read_text(encoding="utf-8").splitlines()
        total = len(lines)
        s = max(1, start_line)
        e = min(total, end_line) if end_line else total
        numbered = "\n".join(f"{s + i:5d}: {line}" for i, line in enumerate(lines[s - 1 : e]))
        return {"content": numbered, "total_lines": total, "start_line": s, "end_line": e}
    
    def _tool_str_replace_in_file(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
    ) -> dict[str, Any]:
        """Replace an exact, unique string in a file."""
        path = self._resolve(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        content = path.read_text(encoding="utf-8")
        count = content.count(old_string)
        if count == 0:
            return {
                "error": (
                    f"old_string not found in {file_path}. "
                    "Make sure it matches the file exactly (whitespace, indentation)."
                )
            }
        if count > 1:
            return {
                "error": (
                    f"old_string appears {count} times in {file_path}. "
                    "Include more surrounding context to make it unique."
                )
            }
        path.write_text(content.replace(old_string, new_string, 1), encoding="utf-8")
        return {"success": True, "message": f"Replaced 1 occurrence in {file_path}."}
    
    def _tool_insert_edit_into_file(
        self,
        file_path: str,
        start_line: int,
        end_line: int,
        new_content: str,
    ) -> dict[str, Any]:
        """Replace a range of lines with new content."""
        path = self._resolve(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        total = len(lines)
        if start_line < 1 or start_line > total + 1:
            return {"error": f"start_line {start_line} is out of range (file has {total} lines)."}
        if end_line < start_line:
            return {"error": f"end_line {end_line} must be >= start_line {start_line}."}
        end_line = min(end_line, total)
        
        new_lines = new_content.splitlines(keepends=True)
        # Ensure new block ends with a newline when it sits mid-file
        after = lines[end_line:]
        if new_lines and after and not new_lines[-1].endswith("\n"):
            new_lines[-1] += "\n"
        
        result = lines[: start_line - 1] + new_lines + after
        path.write_text("".join(result), encoding="utf-8")
        return {
            "success": True,
            "message": f"Replaced lines {start_line}–{end_line} in {file_path}.",
        }
    
    def _tool_diff(self, original: str, modified: str, filename: str = "file") -> dict[str, Any]:
        """Compute a unified diff between original and modified text."""
        import difflib
        
        diff_lines = difflib.unified_diff(
            original.splitlines(keepends=True),
            modified.splitlines(keepends=True),
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}",
            lineterm="",
        )
        return {"diff": "".join(diff_lines)}


# =============================================================================
# ValidationService - Handles validation execution and error extraction/formatting
# =============================================================================

class ValidationService:
    """Service for running stub validation and extracting error information."""
    
    def __init__(self, project_root: Path) -> None:
        self._project_root = project_root
    
    def run_validation(self, pyx_file: Path, pyi_file: Path) -> tuple[bool, str]:
        """
        Run validate_stub.py for a pyx/pyi pair.
        
        Returns (passed, combined_output).
        'passed' is True iff VALIDATION_SUCCESS appears in the output.
        """
        result = subprocess.run(
            [sys.executable, "scripts/validate_stub.py", str(pyx_file), str(pyi_file)],
            capture_output=True,
            text=True,
            cwd=str(self._project_root),
        )
        output = (result.stdout + result.stderr).strip()
        return Config.VALIDATION_SUCCESS in output, output
    
    def extract_line_numbers(self, validation_output: str, filename: str) -> list[int]:
        """Extract line numbers from validation output for a given file."""
        pattern = rf'\({re.escape(filename)}:(\d+)\)'
        return sorted({int(m) for m in re.findall(pattern, validation_output)})
    
    def format_section(
        self,
        file_path: Path,
        line_numbers: list[int],
        context: int = Config.CONTEXT_LINES,
    ) -> str:
        """Return numbered-line excerpts from file_path around the given line numbers."""
        if not file_path.exists():
            return f"[File not found: {file_path}]"
        lines = file_path.read_text(encoding="utf-8").splitlines()
        total = len(lines)
        
        if not line_numbers:
            return "\n".join(f"{i+1:5d}: {line}" for i, line in enumerate(lines))
        
        include: set[int] = set()
        for ln in line_numbers:
            for i in range(max(1, ln - context), min(total, ln + context) + 1):
                include.add(i)
        
        result, prev = [], None
        for ln in sorted(include):
            if prev is not None and ln > prev + 1:
                result.append("     : ...")
            result.append(f"{ln:5d}: {lines[ln - 1]}")
            prev = ln
        return "\n".join(result)


# =============================================================================
# StubGenerator - Generates .pyi stubs from .pyx files using LLM
# =============================================================================

class StubGenerator:
    """Generates .pyi stub files from .pyx source using an LLM."""
    
    def __init__(self, symbol_code: str) -> None:
        self._symbol_code = symbol_code
    
    def _build_generation_prompt(self, cython_code: str) -> str:
        """Build the prompt for generating a stub file."""
        return f"""You are a Python programming assistant that generates .pyi stub file from the provided .pyx Cython source code.

Follow these rules strictly when extracting information and generating the .pyi stub:

# General Rules
- Only include Python-accessible symbols. Skip any cdef functions or variables that are not accessible from regular Python code.
- Preserve all docstrings (for classes and functions) exactly as they appear in the .pyx file. Do not alter or skip their content or formatting in any way.
- Do not import from cython or use cimport statements in the generated .pyi stub, skip them.
- Only standard Python imports which exist in .pyx should be included.
- Include all Python-accessible functions, classes (with inheritances), global variables, and class members (variables, methods, and properties) with types.
- Class variables should be type hinted with 'var: ClassVar[type]' with 'from typing import ClassVar', whereas instance variables should be type hinted with 'var: type'
- Don't type hint with generic types such as Dict, Type, etc. from typing module. Just use the original built-in type.
- If the type is not explicitly specified in the pyx code or documentation, do not infer it; keep it as-is.
- Preserve decorators like @property, @staticmethod, @classmethod, and @overload (only if present in the .pyx).
- If a parameter is nullable or optional (i.e., has a default value of None), write: param: type | None = None
- For collections such as dict or list, always include explicit type hints for their elements.
- Function bodies in stub files must be a single ellipsis (...)

# Primitive Type Conversion (Cython → Python)
int, long       -> int
uint64_t, int64_t, uint32_t, int32_t, uint16_t, int16_t, uint8_t, int8_t -> int
size_t, ssize_t -> int
float, double   -> float
str             -> str
bint            -> bool
void            -> None
object          -> Any
type            -> type

# Symbol Reference
The symbols below can be imported as: from nautilus_trader.core.nautilus_pyo3 import ...
Use them when a symbol referenced in the .pyx is not defined locally.
================
{self._symbol_code}
================

# Input (.pyx source)
================
{cython_code}
================

# Output
Respond only with the generated .pyi stub code. Do not include markdown formatting, explanations, or filenames.
"""
    
    def generate(self, pyx_file: Path, model: str) -> str:
        """Call the LLM to generate a .pyi stub from a .pyx file."""
        prompt = self._build_generation_prompt(pyx_file.read_text(encoding="utf-8"))
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content


# =============================================================================
# StubFixer - Iteratively fixes validation errors using tool calls
# =============================================================================

class StubFixer:
    """Iteratively fixes stub files by making targeted edits via LLM tool calls."""
    
    def __init__(
        self,
        registry: ToolRegistry,
        validation_service: ValidationService,
    ) -> None:
        self._registry = registry
        self._validation_service = validation_service
    
    @staticmethod
    def _serialize_message(msg) -> dict[str, Any]:
        """Convert a litellm response message to a plain dict for the messages list."""
        d: dict[str, Any] = {"role": msg.role, "content": msg.content or ""}
        if getattr(msg, "tool_calls", None):
            d["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ]
        return d
    
    def fix(
        self,
        pyx_file: Path,
        pyi_file: Path,
        validation_output: str,
        model: str,
        verbose: bool = False,
    ) -> None:
        """
        Ask the LLM to fix validation errors in pyi_file using targeted tool calls.
        
        Only the problematic sections of both .pyi and .pyx are sent as context.
        """
        pyi_lines = self._validation_service.extract_line_numbers(validation_output, pyi_file.name)
        pyx_lines = self._validation_service.extract_line_numbers(validation_output, pyx_file.name)
        
        pyi_section = self._validation_service.format_section(pyi_file, pyi_lines)
        pyx_section = self._validation_service.format_section(pyx_file, pyx_lines) if pyx_lines else None
        
        system_msg = (
            "You are an expert at fixing Python .pyi stub files generated from Cython .pyx source.\n\n"
            "# Stub file rules (must be respected when editing)\n"
            "- Only include Python-accessible symbols. cdef-only functions/variables must NOT appear.\n"
            "- Preserve all docstrings exactly as they appear in the .pyx file.\n"
            "- Do not add cython or cimport statements.\n"
            "- Class variables: ClassVar[type] (requires 'from typing import ClassVar').\n"
            "  Instance variables: plain 'var: type'.\n"
            "- Do not use generic typing aliases (Dict, List, Tuple, …); use the built-in types instead.\n"
            "- If a type is not explicitly stated in the .pyx, do not infer it — leave it as-is.\n"
            "- Preserve @property, @staticmethod, @classmethod, @overload decorators.\n"
            "- Optional/nullable parameters: 'param: type | None = None'.\n"
            "- Collection type hints must include element types (e.g. list[int], dict[str, Any]).\n"
            "- Function bodies must be a single ellipsis (...).\n\n"
            "# Primitive type conversion (Cython → Python)\n"
            "  bint → bool | double/float → float | int/long/uint*/int* → int\n"
            "  void → None | object → Any\n\n"
            "# Edit instructions\n"
            "- Fix ONLY the items described in the validation errors. Do not touch unrelated code.\n"
            "- Use str_replace_in_file for precise, single-occurrence replacements.\n"
            "- Use insert_edit_into_file when replacing a block of lines by line range.\n"
            "- Use read_file to fetch additional context if a line number is not shown.\n"
            "- Use diff only for preview — it does not modify the file.\n"
            "- Stop calling tools once all errors are fixed."
        )
        
        pyx_ctx = (
            f"\nCORRESPONDING .PYX SECTIONS (read-only reference):\n```\n{pyx_section}\n```\n"
            if pyx_section
            else ""
        )
        user_msg = (
            f"Fix all validation errors in `{pyi_file}`.\n\n"
            f"VALIDATION ERRORS:\n```\n{validation_output}\n```\n\n"
            f"CURRENT .PYI SECTIONS (around error lines):\n```python\n{pyi_section}\n```\n"
            f"{pyx_ctx}"
            "Use the tools to apply the minimum edits required."
        )
        
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ]
        
        calls_made = 0
        while calls_made < Config.MAX_TOOL_CALLS:
            response = litellm.completion(
                model=model,
                messages=messages,
                tools=self._registry.tools,
                tool_choice="auto",
            )
            
            resp_msg = response.choices[0].message
            messages.append(self._serialize_message(resp_msg))
            
            tool_calls = getattr(resp_msg, "tool_calls", None) or []
            if not tool_calls:
                if verbose:
                    content = resp_msg.content or ""
                    if content:
                        print(f"    LLM: {content[:200]}")
                break
            
            for tc in tool_calls:
                calls_made += 1
                name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError as exc:
                    result = {"error": f"JSON decode error in arguments: {exc}"}
                else:
                    result = self._registry.execute(name, args)
                
                if verbose:
                    status = "✓" if "success" in result else "✗"
                    summary = result.get("message") or result.get("error") or list(result.keys())
                    print(f"    {status} {name}() → {summary}")
                
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": json.dumps(result),
                    }
                )
        
        if calls_made >= Config.MAX_TOOL_CALLS:
            print(f"    ⚠ Reached MAX_TOOL_CALLS ({Config.MAX_TOOL_CALLS}) during fix.")


# =============================================================================
# StubCleaner - Cleans up orphaned stub files
# =============================================================================

class StubCleaner:
    """Cleans up orphaned .pyi stub files that have no corresponding .pyx source."""
    
    def __init__(self, module_root: Path, stub_root: Path) -> None:
        self._module_root = module_root
        self._stub_root = stub_root
    
    def cleanup(self) -> list[Path]:
        """
        Delete .pyi files under stub_root that have no matching .pyx in module_root.
        
        Also removes empty parent directories left behind.
        Returns the list of deleted files.
        """
        if not self._stub_root.exists():
            return []
        
        deleted: list[Path] = []
        for pyi_file in sorted(self._stub_root.rglob("*.pyi")):
            relative = pyi_file.relative_to(self._stub_root)
            pyx_file = self._module_root / relative.with_suffix(".pyx")
            if not pyx_file.exists():
                print(f"  Deleting orphaned stub (no .pyx): {pyi_file.relative_to(self._stub_root.parent)}")
                pyi_file.unlink()
                deleted.append(pyi_file)
                # Prune empty ancestor directories up to stub_root
                parent = pyi_file.parent
                while parent != self._stub_root:
                    try:
                        parent.rmdir()  # succeeds only if empty
                        parent = parent.parent
                    except OSError:
                        break
        
        return deleted


# =============================================================================
# StubProcessor - Orchestrates the full workflow for a single file
# =============================================================================

class StubProcessor:
    """Orchestrates the complete stub generation and fixing workflow for a single .pyx file."""
    
    def __init__(
        self,
        generator: StubGenerator,
        fixer: StubFixer,
        validation_service: ValidationService,
    ) -> None:
        self._generator = generator
        self._fixer = fixer
        self._validation_service = validation_service
    
    def process(
        self,
        pyx_file: Path,
        pyi_file: Path,
        model: str,
        max_retries: int,
        overwrite: bool,
        verbose: bool,
    ) -> tuple[bool, str]:
        """
        Process one .pyx → .pyi pair.
        
        - If stub already exists (and not --overwrite): skip generation, validate & fix.
        - If stub is missing (or --overwrite): generate once with LLM, then validate & fix.
        
        Returns (success, status_label).
        """
        # 1. Generate stub only when missing or forced
        is_new = not pyi_file.exists() or overwrite
        if is_new:
            print("  Generating stub via LLM...")
            content = self._generator.generate(pyx_file, model)
            pyi_file.parent.mkdir(parents=True, exist_ok=True)
            pyi_file.write_text(content, encoding="utf-8")
            print(f"  Generated → {pyi_file}")
        else:
            print(f"  Existing stub → {pyi_file}")
        
        prefix = "generated" if is_new else "existing"
        
        # 2. Initial validation
        passed, output = self._validation_service.run_validation(pyx_file, pyi_file)
        if verbose:
            print(f"  Validation:\n{output}\n")
        if passed:
            return True, f"{prefix}, already valid"
        
        if not verbose:
            print(f"  Validation failed – starting fix loop (max {max_retries} attempts)")
        
        # 3. Iterative fix loop
        for attempt in range(1, max_retries + 1):
            print(f"  Fix attempt {attempt}/{max_retries}...")
            self._fixer.fix(pyx_file, pyi_file, output, model, verbose=verbose)
            
            passed, output = self._validation_service.run_validation(pyx_file, pyi_file)
            if verbose:
                print(f"  Validation (attempt {attempt}):\n{output}\n")
            
            if passed:
                return True, f"{prefix}, fixed on attempt {attempt}"
            
            if not verbose:
                # Show a compact error summary
                error_lines = [ln for ln in output.splitlines() if ln.strip().startswith("•")]
                preview = "\n    ".join(error_lines[:5])
                if len(error_lines) > 5:
                    preview += f"\n    … ({len(error_lines) - 5} more errors)"
                print(f"  Still failing:\n    {preview}")
        
        return False, f"{prefix}, failed after {max_retries} retries"


# =============================================================================
# StubAgent - Entry point with CLI argument handling and batch processing
# =============================================================================

class StubAgent:
    """Main entry point for the stub agent with CLI handling and batch processing."""
    
    def __init__(self) -> None:
        self._config = Config()
        self._project_root = Path(__file__).parent.parent
    
    def _load_symbol_code(self) -> str:
        """Load symbol reference file content."""
        symbol_file = self._project_root / self._config.SYMBOL_FILE
        return symbol_file.read_text(encoding="utf-8") if symbol_file.exists() else ""
    
    def _collect_pyx_files(self, args: argparse.Namespace) -> list[Path]:
        """Collect .pyx files to process based on CLI arguments."""
        if args.pyx_file:
            return [args.pyx_file.resolve()]
        return [
            Path(p).resolve()
            for p in glob(str(self._project_root / args.module_path) + "/**/*.pyx", recursive=True)
        ]
    
    def _create_components(
        self,
        symbol_code: str,
        module_root: Path,
        stub_root: Path,
    ) -> tuple[ToolRegistry, ValidationService, StubGenerator, StubFixer]:
        """Create all the component classes needed for processing."""
        registry = ToolRegistry(self._project_root)
        validation_service = ValidationService(self._project_root)
        generator = StubGenerator(symbol_code)
        fixer = StubFixer(registry, validation_service)
        return registry, validation_service, generator, fixer
    
    def run(self, args: argparse.Namespace) -> int:
        """Run the stub agent with the given CLI arguments."""
        # Load symbol reference file
        symbol_code = self._load_symbol_code()
        if not symbol_code:
            print(f"Warning: symbol file not found at {self._project_root / self._config.SYMBOL_FILE}", file=sys.stderr)
        
        # Collect .pyx files to process
        pyx_files = self._collect_pyx_files(args)
        
        if not pyx_files:
            print("No .pyx files found.")
            return 0
        
        module_root = (self._project_root / args.module_path).resolve()
        stub_root = (self._project_root / args.stub_path).resolve()
        
        # Create components
        registry, validation_service, generator, fixer = self._create_components(
            symbol_code, module_root, stub_root
        )
        
        # ── Clean up stubs that have no corresponding .pyx ────────
        print("Scanning for orphaned stubs...")
        cleaner = StubCleaner(module_root, stub_root)
        deleted = cleaner.cleanup()
        if deleted:
            print(f"Deleted {len(deleted)} orphaned stub(s).")
        else:
            print("No orphaned stubs found.")
        print()
        
        # Create processor for per-file workflow
        processor = StubProcessor(generator, fixer, validation_service)
        
        print(f"Model        : {args.model}")
        print(f"Max retries  : {args.max_retries}")
        print(f"Files        : {len(pyx_files)}")
        print()
        
        passed_list: list[str] = []
        fixed_list: list[str] = []
        failed_list: list[str] = []
        deleted_count = len(deleted)
        
        for idx, pyx_file in enumerate(pyx_files, 1):
            try:
                relative = pyx_file.relative_to(module_root)
            except ValueError:
                relative = pyx_file.name  # type: ignore[assignment]
            pyi_file = stub_root / Path(str(relative)).with_suffix(".pyi")
            
            print(f"[{idx}/{len(pyx_files)}] {pyx_file.relative_to(self._project_root)}")
            
            try:
                success, status = processor.process(
                    pyx_file=pyx_file,
                    pyi_file=pyi_file,
                    model=args.model,
                    max_retries=args.max_retries,
                    overwrite=args.overwrite,
                    verbose=args.verbose,
                )
            except Exception:
                status = "exception"
                success = False
                print("  ❌ Unhandled exception:")
                traceback.print_exc()
            
            if success:
                icon = "✅"
                (passed_list if status == "already valid" else fixed_list).append(str(pyx_file))
            else:
                icon = "❌"
                failed_list.append(str(pyx_file))
            
            print(f"  {icon} {status}\n")
        
        # ── Summary ──────────────────────────────────────────────
        total = len(pyx_files)
        print("═" * 60)
        print(f"SUMMARY  {total} files processed")
        print(f"  🗑  Orphaned stubs deleted : {deleted_count}")
        print(f"  ✅ Already valid          : {len(passed_list)}")
        print(f"  ✅ Fixed by agent         : {len(fixed_list)}")
        print(f"  ❌ Failed                 : {len(failed_list)}")
        
        if failed_list:
            print("\nFailed files:")
            for f in failed_list:
                print(f"  • {f}")
        
        return 0 if not failed_list else 1


def main() -> None:
    """Main entry point for the stub agent."""
    parser = argparse.ArgumentParser(
        description="AI agent: generate & fix nautilus-trader Cython stubs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--model",
        default=os.environ.get("STUB_AGENT_MODEL", Config.DEFAULT_MODEL),
        help="LiteLLM model string.",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=Config.DEFAULT_MAX_RETRIES,
        help="Maximum fix attempts per file.",
    )
    parser.add_argument(
        "--pyx-file",
        type=Path,
        metavar="PATH",
        help="Process a single .pyx file instead of the entire module.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Regenerate stubs even when they already exist.",
    )
    parser.add_argument(
        "--api-key",
        metavar="KEY",
        help="API key (alternative: set OPENROUTER_API_KEY env var).",
    )
    parser.add_argument(
        "--module-path",
        default=Config.MODULE_PATH,
        help="Root directory of the .pyx source files.",
    )
    parser.add_argument(
        "--stub-path",
        default=Config.STUB_PATH,
        help="Root directory for generated .pyi files.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show full validation output and tool call details.",
    )
    args = parser.parse_args()
    
    if args.api_key:
        os.environ["OPENROUTER_API_KEY"] = args.api_key
    
    agent = StubAgent()
    sys.exit(agent.run(args))


if __name__ == "__main__":
    main()

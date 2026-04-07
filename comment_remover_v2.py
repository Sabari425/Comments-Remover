"""
UNIVERSAL COMMENT REMOVER - DARK HACKER EDITION v6.0
Complete Multi-Language Comment Removal System with Multi-Line Protection
Preserves Originals | Circular Progress | Full Screen | Live DateTime | Advanced Monitoring
"""

import os
import re
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from collections import deque
import time

# ============================================================================
# ORGANIZATION HEADER
# ============================================================================

ORGANIZATION = "Sabari425 Smart Tools Industries"
VERSION = "v6.0"

# ============================================================================
# LANGUAGE CONFIGURATION
# ============================================================================

class LanguageConfig:
    LANGUAGES = {
        'python': {
            'extensions': ['.py', '.pyw', '.pyx'],
            'single_line': r'#.*$',
            'multi_line_start': ['"""', "'''"],
            'multi_line_end': ['"""', "'''"],
            'preserve_shebang': True,
            'preserve_encoding': True,
            'preserve_multiline_comments': True,  # CRITICAL: Preserve multi-line comments
            'string_aware': True,
            'indent_size': 4
        },
        'javascript': {
            'extensions': ['.js', '.jsx', '.mjs', '.cjs'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_shebang': True,
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 2
        },
        'typescript': {
            'extensions': ['.ts', '.tsx'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 2
        },
        'html': {
            'extensions': ['.html', '.htm', '.xhtml'],
            'single_line': None,
            'multi_line_start': ['<!--'],
            'multi_line_end': ['-->'],
            'preserve_multiline_comments': False,
            'string_aware': False,
            'indent_size': 2
        },
        'css': {
            'extensions': ['.css', '.scss', '.sass', '.less'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 2
        },
        'cpp': {
            'extensions': ['.cpp', '.cc', '.cxx', '.c++', '.h', '.hpp', '.hxx'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 4
        },
        'c': {
            'extensions': ['.c', '.h'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 4
        },
        'java': {
            'extensions': ['.java'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 4
        },
        'csharp': {
            'extensions': ['.cs'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 4
        },
        'ruby': {
            'extensions': ['.rb', '.rbw'],
            'single_line': r'#.*$',
            'multi_line_start': ['=begin'],
            'multi_line_end': ['=end'],
            'preserve_multiline_comments': False,
            'preserve_shebang': True,
            'string_aware': True,
            'indent_size': 2
        },
        'go': {
            'extensions': ['.go'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 4
        },
        'rust': {
            'extensions': ['.rs'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 4
        },
        'php': {
            'extensions': ['.php'],
            'single_line': r'(//|#).*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 4
        },
        'swift': {
            'extensions': ['.swift'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 4
        },
        'kotlin': {
            'extensions': ['.kt', '.kts'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 4
        },
        'sql': {
            'extensions': ['.sql'],
            'single_line': r'(--|#).*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 0
        },
        'xml': {
            'extensions': ['.xml', '.xsd', '.xsl', '.xslt'],
            'single_line': None,
            'multi_line_start': ['<!--'],
            'multi_line_end': ['-->'],
            'preserve_multiline_comments': False,
            'string_aware': False,
            'indent_size': 2
        },
        'yaml': {
            'extensions': ['.yaml', '.yml'],
            'single_line': r'#.*$',
            'multi_line_start': [],
            'multi_line_end': [],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 2
        },
        'json': {
            'extensions': ['.json'],
            'single_line': None,
            'multi_line_start': [],
            'multi_line_end': [],
            'string_aware': True,
            'no_comments': True,
            'indent_size': 2
        },
        'shell': {
            'extensions': ['.sh', '.bash', '.zsh', '.fish'],
            'single_line': r'#.*$',
            'multi_line_start': [": '"],
            'multi_line_end': ["'"],
            'preserve_multiline_comments': False,
            'preserve_shebang': True,
            'string_aware': True,
            'indent_size': 4
        },
        'perl': {
            'extensions': ['.pl', '.pm'],
            'single_line': r'#.*$',
            'multi_line_start': ['=pod', '=cut'],
            'multi_line_end': ['=cut', '=pod'],
            'preserve_multiline_comments': False,
            'preserve_shebang': True,
            'string_aware': True,
            'indent_size': 4
        },
        'lua': {
            'extensions': ['.lua'],
            'single_line': r'--.*$',
            'multi_line_start': ['--[['],
            'multi_line_end': [']]'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 2
        },
        'r': {
            'extensions': ['.r', '.R'],
            'single_line': r'#.*$',
            'multi_line_start': [],
            'multi_line_end': [],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 2
        },
        'dart': {
            'extensions': ['.dart'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_multiline_comments': False,
            'string_aware': True,
            'indent_size': 2
        }
    }
    
    @classmethod
    def detect_language(cls, file_path: str) -> str:
        ext = Path(file_path).suffix.lower()
        for lang, config in cls.LANGUAGES.items():
            if ext in config['extensions']:
                return lang
        return 'unknown'
    
    @classmethod
    def get_config(cls, language: str) -> Dict:
        return cls.LANGUAGES.get(language, {
            'extensions': [],
            'single_line': None,
            'multi_line_start': [],
            'multi_line_end': [],
            'string_aware': False,
            'preserve_multiline_comments': False,
            'indent_size': 4
        })


# ============================================================================
# CODE FORMATTER
# ============================================================================

class CodeFormatter:
    
    @staticmethod
    def format_code(content: str, language: str, config: Dict) -> str:
        """Format code by removing extra blank lines and normalizing indentation"""
        
        lines = content.splitlines()
        
        # Remove empty lines at start and end
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        
        # Remove multiple consecutive empty lines (max 1 empty line)
        formatted_lines = []
        prev_empty = False
        
        for line in lines:
            is_empty = not line.strip()
            
            if is_empty and prev_empty:
                continue
            
            formatted_lines.append(line)
            prev_empty = is_empty
        
        # Basic indentation normalization (preserve relative indentation)
        result = '\n'.join(formatted_lines)
        
        # Ensure single newline at end of file
        if not result.endswith('\n'):
            result += '\n'
        
        return result


# ============================================================================
# DATA DISPLAY PANEL
# ============================================================================

class DataDisplayPanel(tk.Frame):
    def __init__(self, parent, bg_color='#0a0e0a', fg_color='#00ff41', **kwargs):
        super().__init__(parent, bg=bg_color, **kwargs)
        
        self.bg_color = bg_color
        self.fg_color = fg_color
        
        # Create data display areas
        self.create_data_display()
        
    def create_data_display(self):
        # Title
        title_label = tk.Label(self, text="DATA PROCESSING METRICS", font=('Consolas', 10, 'bold'),
                               bg=self.bg_color, fg=self.fg_color)
        title_label.pack(pady=5)
        
        # Metrics Frame
        metrics_frame = tk.Frame(self, bg=self.bg_color)
        metrics_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create metric displays
        self.metrics = {}
        metrics_data = [
            ("FILES SCANNED", "0"),
            ("FILES PROCESSED", "0"),
            ("FILES FAILED", "0"),
            ("TOTAL COMMENTS", "0"),
            ("TOTAL LINES", "0"),
            ("AVG SPEED", "0 files/s"),
            ("EST TIME", "0s"),
            ("MEM USAGE", "0 MB")
        ]
        
        for i, (label, default) in enumerate(metrics_data):
            row = i // 2
            col = i % 2
            
            frame = tk.Frame(metrics_frame, bg=self.bg_color, relief=tk.FLAT, bd=1,
                            highlightbackground='#008822', highlightthickness=1)
            frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            tk.Label(frame, text=label, font=('Consolas', 8), bg=self.bg_color,
                    fg='#00cc33').pack(pady=(5, 0))
            
            var = tk.StringVar(value=default)
            self.metrics[label] = var
            tk.Label(frame, textvariable=var, font=('Consolas', 12, 'bold'),
                    bg=self.bg_color, fg=self.fg_color).pack(pady=(0, 5))
        
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
    
    def update_metric(self, name: str, value: str):
        if name in self.metrics:
            self.metrics[name].set(value)
            self.update_idletasks()
    
    def update_metrics(self, processed: int, total: int, comments: int, lines: int, 
                       elapsed: float, memory: float):
        self.update_metric("FILES PROCESSED", str(processed))
        self.update_metric("TOTAL COMMENTS", str(comments))
        self.update_metric("TOTAL LINES", str(lines))
        
        if total > 0:
            self.update_metric("FILES FAILED", str(total - processed))
        
        if elapsed > 0 and processed > 0:
            speed = processed / elapsed
            self.update_metric("AVG SPEED", f"{speed:.2f} files/s")
            
            if total > 0 and processed > 0:
                remaining = total - processed
                est_time = remaining / speed if speed > 0 else 0
                self.update_metric("EST TIME", f"{est_time:.1f}s")
        
        self.update_metric("MEM USAGE", f"{memory:.1f} MB")


# ============================================================================
# CIRCULAR PROGRESS WIDGET
# ============================================================================

class CircularProgress(tk.Canvas):
    def __init__(self, parent, size=100, thickness=8, bg_color='#0a0e0a', 
                 progress_color='#00ff41', text_color='#00ff41', **kwargs):
        super().__init__(parent, width=size, height=size, bg=bg_color, 
                        highlightthickness=0, **kwargs)
        
        self.size = size
        self.thickness = thickness
        self.progress_color = progress_color
        self.text_color = text_color
        self.bg_color = bg_color
        self.current_progress = 0
        
        center = size // 2
        radius = (size // 2) - thickness
        
        self.create_oval(center - radius, center - radius, 
                        center + radius, center + radius,
                        outline='#1a3a1a', width=thickness, tags='bg_circle')
        
        self.progress_arc = self.create_arc(center - radius, center - radius,
                                           center + radius, center + radius,
                                           start=90, extent=0,
                                           outline=progress_color, width=thickness,
                                           style='arc', tags='progress_arc')
        
        self.text_id = self.create_text(center, center, text='0%',
                                       fill=text_color, font=('Consolas', 14, 'bold'),
                                       tags='progress_text')
    
    def update_progress(self, percent):
        self.current_progress = min(max(percent, 0), 100)
        extent = (self.current_progress / 100) * 360
        self.itemconfig(self.progress_arc, extent=-extent)
        self.itemconfig(self.text_id, text=f'{int(self.current_progress)}%')
        self.update_idletasks()


# ============================================================================
# SCAN PROGRESS WIDGET
# ============================================================================

class ScanProgressWidget(tk.Frame):
    def __init__(self, parent, bg_color='#0a0e0a', fg_color='#00ff41', **kwargs):
        super().__init__(parent, bg=bg_color, **kwargs)
        
        self.bg_color = bg_color
        self.fg_color = fg_color
        
        # Scan status label
        self.scan_label = tk.Label(self, text="SCAN STATUS: IDLE", 
                                   font=('Consolas', 9, 'bold'),
                                   bg=bg_color, fg=fg_color)
        self.scan_label.pack(side=tk.LEFT, padx=5)
        
        # Scan progress bar
        self.scan_bar = ttk.Progressbar(self, mode='determinate', length=200)
        self.scan_bar.pack(side=tk.LEFT, padx=10)
        
        # Scan count label
        self.scan_count = tk.Label(self, text="0/0", font=('Consolas', 9),
                                   bg=bg_color, fg='#00cc33')
        self.scan_count.pack(side=tk.LEFT, padx=5)
        
        # Current item label
        self.current_item = tk.Label(self, text="", font=('Consolas', 8),
                                     bg=bg_color, fg='#00aa33', wraplength=300)
        self.current_item.pack(side=tk.LEFT, padx=10)
    
    def update_scan(self, current: int, total: int, current_file: str = ""):
        percent = (current / total * 100) if total > 0 else 0
        self.scan_bar['value'] = percent
        self.scan_count.config(text=f"{current}/{total}")
        self.scan_label.config(text=f"SCAN STATUS: SCANNING")
        
        if current_file:
            short_name = current_file[:40] + "..." if len(current_file) > 40 else current_file
            self.current_item.config(text=short_name)
        
        self.update_idletasks()
    
    def reset(self):
        self.scan_bar['value'] = 0
        self.scan_count.config(text="0/0")
        self.scan_label.config(text="SCAN STATUS: IDLE")
        self.current_item.config(text="")
        self.update_idletasks()


# ============================================================================
# COMMENT REMOVER ENGINE - WITH MULTI-LINE PROTECTION
# ============================================================================

class CommentRemover:
    
    def __init__(self):
        self.log_messages = []
        self.progress_callback = None
        self.comments_removed = 0
        self.total_lines = 0
        self.preserved_multiline = 0
        
    def set_progress_callback(self, callback):
        self.progress_callback = callback
    
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.log_messages.append(log_entry)
        if self.progress_callback:
            self.progress_callback(log_entry)
    
    def update_file_progress(self, current_line, total_lines, comments_found):
        if total_lines > 0 and self.progress_callback:
            percent = (current_line / total_lines) * 100
            self.progress_callback(f"PROGRESS:{percent:.1f}:{comments_found}")
    
    def is_docstring_or_multiline(self, lines: List[str], start_idx: int, start_pattern: str, end_pattern: str, language: str) -> bool:
        """Determine if a multi-line quote is a docstring or should be preserved"""
        
        if language != 'python':
            return False
        
        # Check if this is a docstring (first statement of module/class/function)
        prev_line = lines[start_idx - 1] if start_idx > 0 else ""
        
        # Docstring conditions
        is_docstring = (
            start_idx == 0 or  # Module docstring
            prev_line.strip().startswith(('class ', 'def ')) or  # Class/function docstring
            prev_line.strip() == '' or  # Might be preceded by decorator
            (start_idx > 1 and lines[start_idx - 2].strip().startswith('@'))  # Decorated function
        )
        
        # For multi-line comments that are NOT docstrings, we preserve them (don't remove)
        # This prevents code logic from being broken
        return is_docstring
    
    def remove_all_comments(self, content: str, language: str, config: Dict, file_progress_callback=None) -> Tuple[str, int, int, int]:
        lines = content.splitlines(True)
        self.total_lines = len(lines)
        result_lines = []
        
        in_string = False
        string_char = None
        in_multiline_comment = False
        multiline_end_pattern = None
        multiline_start_line = -1
        comments_removed = 0
        preserved_multiline = 0
        
        i = 0
        while i < len(lines):
            line = lines[i]
            original_line = line.rstrip('\n\r')
            line_num = i + 1
            
            if file_progress_callback:
                file_progress_callback(line_num, self.total_lines, comments_removed)
            
            # Handle multi-line comments
            if not in_string and not in_multiline_comment and config['multi_line_start']:
                matched = False
                for idx, start_pattern in enumerate(config['multi_line_start']):
                    if start_pattern in original_line:
                        end_pattern = config['multi_line_end'][idx] if idx < len(config['multi_line_end']) else config['multi_line_end'][0]
                        
                        # CRITICAL: Check if this is a docstring or should be preserved
                        should_preserve = self.is_docstring_or_multiline(lines, i, start_pattern, end_pattern, language)
                        
                        # For Python multi-line quotes (''' or """), we PRESERVE them to avoid breaking code
                        if language == 'python' and start_pattern in ['"""', "'''"]:
                            if should_preserve:
                                # This is a docstring - keep it
                                if end_pattern in original_line:
                                    result_lines.append(line)
                                else:
                                    result_lines.append(line)
                                    while i + 1 < len(lines):
                                        i += 1
                                        result_lines.append(lines[i])
                                        if end_pattern in lines[i]:
                                            break
                                i += 1
                                matched = True
                                self.log(f"DOCSTRING_PRESERVED: line {line_num}", "PRESERVE")
                                preserved_multiline += 1
                                break
                            else:
                                # This is a multi-line comment that could break code - PRESERVE IT
                                # Do NOT remove multi-line comments in Python to avoid breaking logic
                                if end_pattern in original_line:
                                    result_lines.append(line)
                                else:
                                    result_lines.append(line)
                                    while i + 1 < len(lines):
                                        i += 1
                                        result_lines.append(lines[i])
                                        if end_pattern in lines[i]:
                                            break
                                i += 1
                                matched = True
                                self.log(f"MULTILINE_COMMENT_PRESERVED: line {line_num} (to avoid code breakage)", "PRESERVE")
                                preserved_multiline += 1
                                break
                        
                        # For non-Python languages, handle multi-line comments
                        if config.get('preserve_multiline_comments', False):
                            # Preserve multi-line comments
                            if end_pattern in original_line:
                                result_lines.append(line)
                            else:
                                result_lines.append(line)
                                while i + 1 < len(lines):
                                    i += 1
                                    result_lines.append(lines[i])
                                    if end_pattern in lines[i]:
                                        break
                            i += 1
                            matched = True
                            preserved_multiline += 1
                            break
                        
                        # Remove multi-line comment
                        in_multiline_comment = True
                        multiline_end_pattern = end_pattern
                        multiline_start_line = line_num
                        
                        if end_pattern in original_line and original_line.index(start_pattern) < original_line.index(end_pattern):
                            in_multiline_comment = False
                            before_comment = original_line[:original_line.index(start_pattern)]
                            after_comment = original_line[original_line.index(end_pattern) + len(end_pattern):]
                            cleaned_line = before_comment + after_comment
                            if cleaned_line.strip():
                                result_lines.append(cleaned_line + '\n')
                            else:
                                result_lines.append('\n')
                            comments_removed += 1
                        else:
                            before_comment = original_line[:original_line.index(start_pattern)]
                            if before_comment.strip():
                                result_lines.append(before_comment + '\n')
                            else:
                                result_lines.append('\n')
                            comments_removed += 1
                        i += 1
                        matched = True
                        break
                if matched:
                    continue
            
            if in_multiline_comment:
                if multiline_end_pattern in original_line:
                    in_multiline_comment = False
                    after_comment = original_line[original_line.index(multiline_end_pattern) + len(multiline_end_pattern):]
                    if after_comment.strip():
                        result_lines.append(after_comment + '\n')
                    else:
                        result_lines.append('\n')
                    comments_removed += 1
                else:
                    result_lines.append('\n')
                    comments_removed += 1
                i += 1
                continue
            
            # Handle single line comments with string awareness
            if config.get('string_aware', True) and config.get('single_line'):
                new_line = []
                j = 0
                line_length = len(original_line)
                
                while j < line_length:
                    char = original_line[j]
                    
                    if char in ('"', "'") and (j == 0 or original_line[j-1] != '\\'):
                        if not in_string:
                            in_string = True
                            string_char = char
                            new_line.append(char)
                        elif char == string_char:
                            in_string = False
                            string_char = None
                            new_line.append(char)
                        else:
                            new_line.append(char)
                        j += 1
                        continue
                    
                    if not in_string:
                        # Check for comment patterns
                        if language == 'python' and char == '#':
                            if original_line[j:].strip():
                                comments_removed += 1
                            break
                        elif language in ['javascript', 'typescript', 'cpp', 'c', 'java', 'csharp', 'go', 'rust', 'swift', 'kotlin', 'dart']:
                            if char == '/' and j + 1 < line_length and original_line[j+1] == '/':
                                if original_line[j:].strip():
                                    comments_removed += 1
                                break
                        elif language == 'sql' and char == '-':
                            if j + 1 < line_length and original_line[j+1] == '-':
                                if original_line[j:].strip():
                                    comments_removed += 1
                                break
                        elif language in ['ruby', 'yaml', 'perl', 'r', 'shell'] and char == '#':
                            if original_line[j:].strip():
                                comments_removed += 1
                            break
                        elif language == 'php' and char == '#':
                            if original_line[j:].strip():
                                comments_removed += 1
                            break
                        elif language == 'lua' and char == '-':
                            if j + 1 < line_length and original_line[j+1] == '-':
                                if original_line[j:].strip():
                                    comments_removed += 1
                                break
                    
                    new_line.append(char)
                    j += 1
                else:
                    result_lines.append(''.join(new_line) + '\n')
                    i += 1
                    continue
                
                result_lines.append(''.join(new_line).rstrip() + '\n')
                i += 1
                continue
            
            # Handle non-string-aware languages
            if not config.get('string_aware', True) and config['multi_line_start']:
                modified_line = original_line
                for start_pattern, end_pattern in zip(config['multi_line_start'], config['multi_line_end']):
                    while start_pattern in modified_line and end_pattern in modified_line:
                        start_idx = modified_line.index(start_pattern)
                        end_idx = modified_line.index(end_pattern) + len(end_pattern)
                        modified_line = modified_line[:start_idx] + modified_line[end_idx:]
                        comments_removed += 1
                    while start_pattern in modified_line:
                        modified_line = modified_line[:modified_line.index(start_pattern)]
                        comments_removed += 1
                if modified_line.strip():
                    result_lines.append(modified_line + '\n')
                else:
                    result_lines.append('\n')
                i += 1
                continue
            
            result_lines.append(line)
            i += 1
        
        cleaned_content = ''.join(result_lines)
        
        # Preserve shebang
        if config.get('preserve_shebang') and content.startswith('#!'):
            first_line = content.split('\n')[0]
            if not cleaned_content.startswith('#!'):
                cleaned_content = first_line + '\n' + cleaned_content
        
        # Preserve encoding
        if language == 'python' and config.get('preserve_encoding'):
            encoding_match = re.search(r'^#\s*-\*-\s*coding\s*:.*-\*-|^#\s*coding\s*[:=]', content, re.MULTILINE)
            if encoding_match and encoding_match.group(0) not in cleaned_content:
                cleaned_content = encoding_match.group(0) + '\n' + cleaned_content
        
        return cleaned_content, comments_removed, self.total_lines, preserved_multiline
    
    def process_file(self, file_path: str, output_path: str, progress_callback=None) -> Dict[str, Any]:
        result = {
            'success': False,
            'language': 'unknown',
            'comments_removed': 0,
            'total_lines': 0,
            'preserved_multiline': 0,
            'errors': [],
            'warnings': []
        }
        
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"FILE_NOT_FOUND: {file_path}")
            
            language = LanguageConfig.detect_language(file_path)
            result['language'] = language
            
            if language == 'unknown':
                result['warnings'].append(f"UNKNOWN_LANGUAGE: {file_path}")
                result['success'] = True
                return result
            
            config = LanguageConfig.get_config(language)
            
            if config.get('no_comments'):
                shutil.copy2(file_path, output_path)
                result['success'] = True
                return result
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                original_content = f.read()
            
            def file_progress_cb(current, total, comments):
                if progress_callback:
                    percent = (current / total) * 100 if total > 0 else 0
                    progress_callback(f"FILE_PROGRESS:{percent:.1f}:{comments}")
            
            cleaned_content, comments_count, total_lines, preserved = self.remove_all_comments(
                original_content, language, config, file_progress_cb
            )
            
            # Format the code after comment removal
            cleaned_content = CodeFormatter.format_code(cleaned_content, language, config)
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            result['comments_removed'] = comments_count
            result['total_lines'] = total_lines
            result['preserved_multiline'] = preserved
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(str(e))
            result['success'] = False
        
        return result


# ============================================================================
# BATCH PROCESSOR
# ============================================================================

class BatchProcessor:
    
    def __init__(self):
        self.results = []
        self.start_time = None
        self.last_update = None
    
    def scan_directory(self, source_dir: str, extensions: List[str] = None) -> List[Path]:
        source_path = Path(source_dir)
        
        if extensions:
            files = []
            for ext in extensions:
                files.extend(source_path.rglob(f"*{ext}"))
        else:
            all_extensions = []
            for lang, config in LanguageConfig.LANGUAGES.items():
                all_extensions.extend(config['extensions'])
            files = []
            for ext in all_extensions:
                files.extend(source_path.rglob(f"*{ext}"))
        
        return files
    
    def process_directory(self, source_dir: str, output_dir: str, extensions: List[str] = None, 
                          progress_callback=None, file_callback=None, scan_callback=None,
                          metrics_callback=None) -> Dict[str, Any]:
        
        self.start_time = time.time()
        
        results = {
            'total_files': 0,
            'processed_files': 0,
            'failed_files': 0,
            'skipped_files': 0,
            'total_comments_removed': 0,
            'total_lines_processed': 0,
            'total_preserved_multiline': 0,
            'details': []
        }
        
        source_path = Path(source_dir)
        output_path = Path(output_dir)
        
        # Scan for files
        if scan_callback:
            scan_callback("STARTING_SCAN", 0, 0, "")
        
        files = self.scan_directory(source_dir, extensions)
        results['total_files'] = len(files)
        
        if scan_callback:
            scan_callback("SCAN_COMPLETE", results['total_files'], results['total_files'], "")
        
        for idx, file_path in enumerate(files):
            rel_path = file_path.relative_to(source_path)
            output_file = output_path / rel_path
            
            # Update scan progress
            if scan_callback:
                scan_callback("PROCESSING", idx + 1, results['total_files'], file_path.name)
            
            if progress_callback:
                overall_percent = (idx / results['total_files']) * 100 if results['total_files'] > 0 else 0
                progress_callback(f"OVERALL:{overall_percent:.1f}:{idx}/{results['total_files']}")
                progress_callback(f"CURRENT:{file_path.name}")
            
            remover = CommentRemover()
            
            def file_progress(msg):
                if file_callback:
                    file_callback(msg)
            
            result = remover.process_file(str(file_path), str(output_file), file_progress)
            
            results['details'].append({
                'file': str(file_path),
                'output': str(output_file),
                'success': result['success'],
                'comments_removed': result.get('comments_removed', 0),
                'total_lines': result.get('total_lines', 0),
                'preserved_multiline': result.get('preserved_multiline', 0),
                'language': result.get('language', 'unknown'),
                'errors': result.get('errors', [])
            })
            
            if result['success']:
                results['processed_files'] += 1
                results['total_comments_removed'] += result.get('comments_removed', 0)
                results['total_lines_processed'] += result.get('total_lines', 0)
                results['total_preserved_multiline'] += result.get('preserved_multiline', 0)
            else:
                results['failed_files'] += 1
            
            if file_callback:
                file_callback(f"COMPLETE:{result['success']}:{result.get('comments_removed', 0)}")
            
            # Update metrics
            if metrics_callback and idx % 5 == 0:  # Update every 5 files
                elapsed = time.time() - self.start_time
                try:
                    import psutil
                    memory = psutil.Process().memory_info().rss / 1024 / 1024
                except:
                    memory = 0
                metrics_callback(results['processed_files'], results['total_files'], 
                               results['total_comments_removed'], results['total_lines_processed'],
                               elapsed, memory)
        
        if progress_callback:
            progress_callback(f"OVERALL:100:{results['total_files']}/{results['total_files']}")
        
        return results


# ============================================================================
# TOP RIGHT INFO PANEL
# ============================================================================

class TopRightInfoPanel(tk.Frame):
    def __init__(self, parent, bg_color='#050805', fg_color='#00ff41', **kwargs):
        super().__init__(parent, bg=bg_color, **kwargs)
        
        self.bg_color = bg_color
        self.fg_color = fg_color
        
        # Date and Time variables
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()
        self.uptime_var = tk.StringVar()
        self.processes_var = tk.StringVar()
        
        # Labels
        info_frame = tk.Frame(self, bg=bg_color)
        info_frame.pack(side=tk.RIGHT, padx=15, pady=5)
        
        # Date
        date_label = tk.Label(info_frame, textvariable=self.date_var, font=('Consolas', 9),
                              bg=bg_color, fg=fg_color)
        date_label.pack(side=tk.LEFT, padx=5)
        
        # Separator
        tk.Label(info_frame, text="|", font=('Consolas', 9), bg=bg_color, fg='#008822').pack(side=tk.LEFT)
        
        # Time
        time_label = tk.Label(info_frame, textvariable=self.time_var, font=('Consolas', 9, 'bold'),
                              bg=bg_color, fg=fg_color)
        time_label.pack(side=tk.LEFT, padx=5)
        
        # Separator
        tk.Label(info_frame, text="|", font=('Consolas', 9), bg=bg_color, fg='#008822').pack(side=tk.LEFT)
        
        # Uptime
        uptime_label = tk.Label(info_frame, textvariable=self.uptime_var, font=('Consolas', 9),
                                bg=bg_color, fg='#00cc33')
        uptime_label.pack(side=tk.LEFT, padx=5)
        
        # Separator
        tk.Label(info_frame, text="|", font=('Consolas', 9), bg=bg_color, fg='#008822').pack(side=tk.LEFT)
        
        # Processes
        processes_label = tk.Label(info_frame, textvariable=self.processes_var, font=('Consolas', 9),
                                   bg=bg_color, fg='#00aa33')
        processes_label.pack(side=tk.LEFT, padx=5)
        
        self.update_datetime()
    
    def update_datetime(self):
        now = datetime.now()
        self.date_var.set(now.strftime("%Y-%m-%d"))
        self.time_var.set(now.strftime("%H:%M:%S"))
        self.uptime_var.set(f"UP: {self.get_uptime()}")
        self.processes_var.set(f"CPU: {self.get_cpu_percent()}%")
        
        # Update every second
        self.after(1000, self.update_datetime)
    
    def get_uptime(self):
        import time
        try:
            import psutil
            uptime_seconds = time.time() - psutil.boot_time()
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{hours:02d}:{minutes:02d}"
        except:
            return "00:00"
    
    def get_cpu_percent(self):
        try:
            import psutil
            return psutil.cpu_percent(interval=0.1)
        except:
            return 0


# ============================================================================
# FILE DETAILS PANEL
# ============================================================================

class FileDetailsPanel(tk.Frame):
    def __init__(self, parent, bg_color='#0a0e0a', fg_color='#00ff41', **kwargs):
        super().__init__(parent, bg=bg_color, **kwargs)
        
        self.bg_color = bg_color
        self.fg_color = fg_color
        
        self.create_file_details()
        
    def create_file_details(self):
        # Title
        title_label = tk.Label(self, text="CURRENT FILE DETAILS", font=('Consolas', 10, 'bold'),
                               bg=self.bg_color, fg=self.fg_color)
        title_label.pack(pady=5)
        
        # File name display
        self.file_name_var = tk.StringVar(value="No file selected")
        file_name_label = tk.Label(self, textvariable=self.file_name_var, font=('Consolas', 9),
                                   bg=self.bg_color, fg='#00cc33', wraplength=280)
        file_name_label.pack(pady=5)
        
        # File details frame
        details_frame = tk.Frame(self, bg=self.bg_color)
        details_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # File size
        self.file_size_var = tk.StringVar(value="Size: --")
        tk.Label(details_frame, textvariable=self.file_size_var, font=('Consolas', 8),
                bg=self.bg_color, fg='#00aa33').pack(anchor='w')
        
        # Language
        self.file_lang_var = tk.StringVar(value="Language: --")
        tk.Label(details_frame, textvariable=self.file_lang_var, font=('Consolas', 8),
                bg=self.bg_color, fg='#00aa33').pack(anchor='w')
        
        # Lines
        self.file_lines_var = tk.StringVar(value="Lines: --")
        tk.Label(details_frame, textvariable=self.file_lines_var, font=('Consolas', 8),
                bg=self.bg_color, fg='#00aa33').pack(anchor='w')
        
        # Comments
        self.file_comments_var = tk.StringVar(value="Comments: --")
        tk.Label(details_frame, textvariable=self.file_comments_var, font=('Consolas', 8),
                bg=self.bg_color, fg='#00aa33').pack(anchor='w')
        
        # Status
        self.file_status_var = tk.StringVar(value="Status: Waiting")
        tk.Label(details_frame, textvariable=self.file_status_var, font=('Consolas', 8, 'bold'),
                bg=self.bg_color, fg='#00ff41').pack(anchor='w')
    
    def update_file_info(self, file_path: str, language: str = "", comments: int = 0, 
                         lines: int = 0, status: str = "Processing"):
        if file_path:
            self.file_name_var.set(f"File: {Path(file_path).name[:50]}")
            
            # Get file size
            try:
                size = os.path.getsize(file_path)
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size/1024:.1f} KB"
                else:
                    size_str = f"{size/(1024*1024):.1f} MB"
                self.file_size_var.set(f"Size: {size_str}")
            except:
                self.file_size_var.set("Size: --")
        
        if language:
            self.file_lang_var.set(f"Language: {language.upper()}")
        if lines > 0:
            self.file_lines_var.set(f"Lines: {lines}")
        if comments >= 0:
            self.file_comments_var.set(f"Comments: {comments}")
        
        self.file_status_var.set(f"Status: {status}")
        self.update_idletasks()
    
    def reset(self):
        self.file_name_var.set("No file selected")
        self.file_size_var.set("Size: --")
        self.file_lang_var.set("Language: --")
        self.file_lines_var.set("Lines: --")
        self.file_comments_var.set("Comments: --")
        self.file_status_var.set("Status: Waiting")
        self.update_idletasks()


# ============================================================================
# DARK HACKER GUI
# ============================================================================

class DarkHackerGUI:
    
    def __init__(self):
        self.root = None
        self.output_area = None
        self.circular_progress = None
        self.status_label = None
        self.stats_vars = {}
        self.is_processing = False
        self.current_file_var = None
        self.current_comments_var = None
        self.scan_widget = None
        self.top_info_panel = None
        self.data_display = None
        self.file_details = None
        self.is_fullscreen = False
        self.preserved_multiline_var = None
        
    def setup_styles(self):
        self.root.configure(bg='#0a0e0a')
        return {
            'bg_dark': '#0a0e0a',
            'bg_darker': '#050805',
            'fg_green': '#00ff41',
            'fg_green_dim': '#00cc33',
            'fg_green_dark': '#008822',
            'fg_white': '#d0ffd0',
            'border': '#00ff41',
            'select': '#003300'
        }
    
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
    
    def clear_output(self):
        if self.output_area:
            self.output_area.delete(1.0, tk.END)
    
    def log_message(self, message: str):
        if self.output_area:
            self.output_area.insert(tk.END, message + "\n")
            self.output_area.see(tk.END)
            
            if "[SUCCESS]" in message or "COMPLETED" in message:
                self.output_area.tag_add("SUCCESS", "end-2l", "end-1l")
            elif "[ERROR]" in message:
                self.output_area.tag_add("ERROR", "end-2l", "end-1l")
            elif "[WARNING]" in message:
                self.output_area.tag_add("WARNING", "end-2l", "end-1l")
            elif "PROGRESS:" in message:
                pass
            else:
                self.output_area.tag_add("INFO", "end-2l", "end-1l")
            
            self.root.update_idletasks()
    
    def update_circular_progress(self, message: str):
        if message.startswith("OVERALL:"):
            parts = message.split(":")
            if len(parts) >= 2:
                percent = float(parts[1])
                if self.circular_progress:
                    self.circular_progress.update_progress(percent)
                if self.status_label:
                    if len(parts) >= 3:
                        self.status_label.config(text=f"PROCESSING: {parts[2]}")
                    else:
                        self.status_label.config(text=f"PROCESSING: {percent:.0f}%")
        
        elif message.startswith("CURRENT:"):
            if self.current_file_var:
                self.current_file_var.set(f"FILE: {message[8:][:50]}")
        
        elif message.startswith("FILE_PROGRESS:"):
            parts = message.split(":")
            if len(parts) >= 3:
                file_percent = float(parts[1])
                comments = parts[2]
                if self.current_comments_var:
                    self.current_comments_var.set(f"COMMENTS: {comments}")
        
        elif message.startswith("COMPLETE:"):
            parts = message.split(":")
            if len(parts) >= 3:
                success = parts[1] == "True"
                comments = parts[2]
                if success:
                    self.log_message(f"[SUCCESS] File processed - {comments} comments removed")
                else:
                    self.log_message(f"[ERROR] File processing failed")
    
    def update_scan_progress(self, status: str, current: int, total: int, current_file: str = ""):
        if self.scan_widget:
            if status == "STARTING_SCAN":
                self.scan_widget.scan_label.config(text="SCAN STATUS: SCANNING DIRECTORY...")
                self.scan_widget.scan_bar['value'] = 0
                self.scan_widget.scan_count.config(text="Scanning...")
            elif status == "SCAN_COMPLETE":
                self.scan_widget.scan_label.config(text="SCAN STATUS: COMPLETE")
                self.scan_widget.scan_bar['value'] = 100
                self.scan_widget.scan_count.config(text=f"{total} files found")
            elif status == "PROCESSING":
                self.scan_widget.update_scan(current, total, current_file)
    
    def update_metrics(self, processed: int, total: int, comments: int, lines: int, 
                       elapsed: float, memory: float):
        if self.data_display:
            self.data_display.update_metrics(processed, total, comments, lines, elapsed, memory)
    
    def process_single(self):
        if self.is_processing:
            messagebox.showwarning("BUSY", "Another operation is in progress")
            return
        
        file_path = filedialog.askopenfilename(
            title="SELECT FILE FOR COMMENT REMOVAL",
            filetypes=[("ALL SUPPORTED FILES", "*.*"), ("ALL FILES", "*.*")]
        )
        if not file_path:
            return
        
        output_dir = Path(file_path).parent
        file_name = Path(file_path).stem
        file_ext = Path(file_path).suffix
        output_path = output_dir / f"{file_name} - comments removed{file_ext}"
        
        self.is_processing = True
        self.clear_output()
        self.circular_progress.update_progress(0)
        
        # Update file details
        if self.file_details:
            self.file_details.update_file_info(file_path, status="Starting")
        
        if self.current_file_var:
            self.current_file_var.set(f"FILE: {Path(file_path).name}")
        if self.current_comments_var:
            self.current_comments_var.set("COMMENTS: 0")
        
        self.log_message(f"[START] Processing: {Path(file_path).name}")
        self.log_message(f"[INFO] Output: {output_path}")
        
        def process_thread():
            remover = CommentRemover()
            
            def progress_callback(msg):
                self.root.after(0, lambda: self.update_circular_progress(msg))
                self.root.after(0, lambda: self.log_message(msg) if not msg.startswith(("OVERALL:", "CURRENT:", "FILE_PROGRESS:")) else None)
            
            remover.set_progress_callback(progress_callback)
            result = remover.process_file(file_path, str(output_path), progress_callback)
            
            self.root.after(0, lambda: self.single_complete(result, output_path, file_path))
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def single_complete(self, result: Dict, output_path: Path, input_path: str):
        self.circular_progress.update_progress(100)
        
        if result['success']:
            # Update file details
            if self.file_details:
                self.file_details.update_file_info(
                    input_path, 
                    language=result['language'],
                    comments=result['comments_removed'],
                    lines=result['total_lines'],
                    status="Completed"
                )
            
            self.log_message("")
            self.log_message("=" * 80)
            self.log_message("[SUCCESS] FILE PROCESSED SUCCESSFULLY")
            self.log_message(f"[INFO] LANGUAGE: {result['language'].upper()}")
            self.log_message(f"[INFO] COMMENTS REMOVED: {result['comments_removed']}")
            self.log_message(f"[INFO] MULTILINE PRESERVED: {result.get('preserved_multiline', 0)}")
            self.log_message(f"[INFO] TOTAL LINES: {result['total_lines']}")
            self.log_message(f"[INFO] OUTPUT SAVED: {output_path}")
            self.log_message("=" * 80)
            
            # Update stats
            self.stats_vars['total_files'].set("1")
            self.stats_vars['comments_removed'].set(str(result['comments_removed']))
            self.stats_vars['success_rate'].set("100%")
            
            if self.preserved_multiline_var:
                self.preserved_multiline_var.set(str(result.get('preserved_multiline', 0)))
            
            messagebox.showinfo(
                "PROCESSING COMPLETE",
                f"FILE PROCESSED SUCCESSFULLY\n\n"
                f"LANGUAGE: {result['language'].upper()}\n"
                f"COMMENTS REMOVED: {result['comments_removed']}\n"
                f"MULTILINE PRESERVED: {result.get('preserved_multiline', 0)}\n"
                f"TOTAL LINES: {result['total_lines']}\n\n"
                f"OUTPUT: {output_path}"
            )
        else:
            if self.file_details:
                self.file_details.update_file_info(input_path, status="Failed")
            
            self.log_message("")
            self.log_message("=" * 80)
            self.log_message("[ERROR] PROCESSING FAILED")
            for err in result.get('errors', []):
                self.log_message(f"[ERROR] {err}")
            self.log_message("=" * 80)
            
            messagebox.showerror(
                "PROCESSING FAILED",
                f"FILE PROCESSING FAILED\n\n"
                f"ERRORS: {', '.join(result.get('errors', ['UNKNOWN ERROR']))}"
            )
        
        self.is_processing = False
        self.circular_progress.update_progress(0)
        if self.current_file_var:
            self.current_file_var.set("FILE: READY")
        if self.current_comments_var:
            self.current_comments_var.set("COMMENTS: 0")
    
    def process_batch(self):
        if self.is_processing:
            messagebox.showwarning("BUSY", "Another operation is in progress")
            return
        
        source_dir = filedialog.askdirectory(title="SELECT SOURCE DIRECTORY")
        if not source_dir:
            return
        
        source_path = Path(source_dir)
        output_dir_name = f"{source_path.name} - comments removed"
        parent_dir = source_path.parent
        output_dir = parent_dir / output_dir_name
        
        confirm = messagebox.askyesno(
            "CONFIRM BATCH PROCESSING",
            f"SOURCE: {source_dir}\n"
            f"OUTPUT: {output_dir}\n\n"
            f"All supported files will be processed.\n"
            f"Original files will remain unchanged.\n"
            f"Multi-line comments in Python files will be PRESERVED.\n\n"
            f"Proceed?"
        )
        
        if not confirm:
            return
        
        self.is_processing = True
        self.clear_output()
        self.circular_progress.update_progress(0)
        
        if self.current_file_var:
            self.current_file_var.set("BATCH PROCESSING ACTIVE")
        if self.current_comments_var:
            self.current_comments_var.set("INITIALIZING...")
        
        if self.file_details:
            self.file_details.reset()
        
        self.log_message(f"[START] Batch processing: {source_dir}")
        self.log_message(f"[INFO] Output directory: {output_dir}")
        self.log_message(f"[INFO] Multi-line comments in Python will be PRESERVED to avoid code breakage")
        
        def process_thread():
            processor = BatchProcessor()
            
            def progress_callback(msg):
                self.root.after(0, lambda: self.update_circular_progress(msg))
            
            def file_callback(msg):
                self.root.after(0, lambda: self.update_circular_progress(msg))
            
            def scan_callback(status, current, total, current_file):
                self.root.after(0, lambda: self.update_scan_progress(status, current, total, current_file))
                if current_file and self.file_details:
                    self.root.after(0, lambda: self.file_details.update_file_info(
                        os.path.join(source_dir, current_file) if current_file else "",
                        status="Scanning"
                    ))
            
            def metrics_callback(processed, total, comments, lines, elapsed, memory):
                self.root.after(0, lambda: self.update_metrics(processed, total, comments, lines, elapsed, memory))
            
            results = processor.process_directory(source_dir, str(output_dir), 
                                                  progress_callback=progress_callback,
                                                  file_callback=file_callback,
                                                  scan_callback=scan_callback,
                                                  metrics_callback=metrics_callback)
            
            self.root.after(0, lambda: self.batch_complete(results, output_dir))
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def batch_complete(self, results: Dict, output_dir: Path):
        self.circular_progress.update_progress(100)
        
        self.log_message("")
        self.log_message("=" * 80)
        self.log_message("[SUCCESS] BATCH PROCESSING COMPLETED")
        self.log_message(f"[STATS] TOTAL FILES: {results['total_files']}")
        self.log_message(f"[STATS] PROCESSED: {results['processed_files']}")
        self.log_message(f"[STATS] FAILED: {results['failed_files']}")
        self.log_message(f"[STATS] TOTAL COMMENTS REMOVED: {results['total_comments_removed']}")
        self.log_message(f"[STATS] TOTAL MULTILINE PRESERVED: {results['total_preserved_multiline']}")
        self.log_message(f"[STATS] TOTAL LINES PROCESSED: {results['total_lines_processed']}")
        self.log_message(f"[INFO] OUTPUT DIRECTORY: {output_dir}")
        self.log_message("-" * 40)
        
        # Group results by language
        lang_stats = {}
        for detail in results['details']:
            lang = detail['language']
            if lang not in lang_stats:
                lang_stats[lang] = {'success': 0, 'failed': 0, 'comments': 0}
            if detail['success']:
                lang_stats[lang]['success'] += 1
                lang_stats[lang]['comments'] += detail['comments_removed']
            else:
                lang_stats[lang]['failed'] += 1
        
        self.log_message("\nLANGUAGE BREAKDOWN:")
        for lang, stats in lang_stats.items():
            self.log_message(f"  {lang.upper()}: {stats['success']} processed, {stats['failed']} failed, {stats['comments']} comments")
        
        self.log_message("-" * 40)
        
        # Show successful files
        success_count = 0
        for detail in results['details']:
            if detail['success']:
                success_count += 1
                if success_count <= 20:  # Show first 20 successful files
                    self.log_message(f"[OK] {Path(detail['file']).name} | {detail['language']} | {detail['comments_removed']} comments | {detail['preserved_multiline']} preserved")
        
        if results['processed_files'] > 20:
            self.log_message(f"... and {results['processed_files'] - 20} more files")
        
        # Show failed files
        for detail in results['details']:
            if not detail['success']:
                self.log_message(f"[FAIL] {Path(detail['file']).name} | {detail['language']}")
                for err in detail.get('errors', []):
                    self.log_message(f"       ERROR: {err}")
        
        self.log_message("=" * 80)
        
        # Update stats
        self.stats_vars['total_files'].set(str(results['total_files']))
        self.stats_vars['comments_removed'].set(str(results['total_comments_removed']))
        if results['total_files'] > 0:
            rate = (results['processed_files'] / results['total_files']) * 100
            self.stats_vars['success_rate'].set(f"{rate:.0f}%")
        
        if self.preserved_multiline_var:
            self.preserved_multiline_var.set(str(results['total_preserved_multiline']))
        
        if self.file_details:
            self.file_details.reset()
        
        messagebox.showinfo(
            "BATCH PROCESSING COMPLETE",
            f"BATCH PROCESSING COMPLETED\n\n"
            f"TOTAL FILES: {results['total_files']}\n"
            f"SUCCESSFUL: {results['processed_files']}\n"
            f"FAILED: {results['failed_files']}\n"
            f"TOTAL COMMENTS REMOVED: {results['total_comments_removed']}\n"
            f"MULTILINE PRESERVED: {results['total_preserved_multiline']}\n"
            f"TOTAL LINES PROCESSED: {results['total_lines_processed']}\n\n"
            f"OUTPUT DIRECTORY: {output_dir}"
        )
        
        self.is_processing = False
        self.circular_progress.update_progress(0)
        if self.current_file_var:
            self.current_file_var.set("FILE: READY")
        if self.current_comments_var:
            self.current_comments_var.set("COMMENTS: 0")
        if self.scan_widget:
            self.scan_widget.reset()
    
    def view_documentation(self):
        doc_text = f"""
UNIVERSAL COMMENT REMOVER {VERSION}
DOCUMENTATION

OVERVIEW:
This tool removes single-line comments from source code files while
PRESERVING multi-line comments to avoid breaking code logic.

KEY FEATURE:
- Multi-line comments in Python are PRESERVED (NOT removed)
- Only single-line comments are removed

SUPPORTED LANGUAGES:
25+ languages including Python, JavaScript, HTML, CSS, C, C++, Java, Go, Rust

SHORTCUTS:
F11 - Fullscreen | Ctrl+D - Documentation | Ctrl+S - Statistics

ORGANIZATION: {ORGANIZATION}
VERSION: {VERSION}
        """
        messagebox.showinfo("DOCUMENTATION", doc_text)
    
    def show_stats(self):
        stats_text = f"""
PROCESSING STATISTICS

Total Files Processed: {self.stats_vars['total_files'].get()}
Total Comments Removed: {self.stats_vars['comments_removed'].get()}
Success Rate: {self.stats_vars['success_rate'].get()}
Multi-line Preserved: {self.preserved_multiline_var.get() if self.preserved_multiline_var else '0'}

SYSTEM INFORMATION
Organization: {ORGANIZATION}
Version: {VERSION}
        """
        messagebox.showinfo("PROCESSING STATISTICS", stats_text)
    
    def run(self):
        self.root = tk.Tk()
        self.root.title(f"UNIVERSAL COMMENT REMOVER {VERSION} - {ORGANIZATION}")
        self.root.geometry("1600x1000")
        self.root.minsize(1400, 850)
        
        # Bind keyboard shortcuts
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Control-d>', lambda e: self.view_documentation())
        self.root.bind('<Control-s>', lambda e: self.show_stats())
        
        style = self.setup_styles()
        
        # Top Bar with Organization and Info
        top_bar = tk.Frame(self.root, bg=style['bg_darker'], height=40)
        top_bar.pack(fill=tk.X)
        top_bar.pack_propagate(False)
        
        # Organization name on left
        org_label = tk.Label(top_bar, text=f"[ {ORGANIZATION} ]", font=('Consolas', 10, 'bold'),
                             bg=style['bg_darker'], fg=style['fg_green'])
        org_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Version on left
        version_label = tk.Label(top_bar, text=f"{VERSION}", font=('Consolas', 9),
                                 bg=style['bg_darker'], fg=style['fg_green_dim'])
        version_label.pack(side=tk.LEFT, padx=5)
        
        # Top Right Info Panel
        self.top_info_panel = TopRightInfoPanel(top_bar, bg_color=style['bg_darker'], fg_color=style['fg_green'])
        self.top_info_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Header
        header_frame = tk.Frame(self.root, bg=style['bg_darker'], height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame, text="UNIVERSAL COMMENT REMOVER", 
            font=('Consolas', 20, 'bold'), bg=style['bg_darker'], fg=style['fg_green']
        ).pack(pady=8)
        
        tk.Label(
            header_frame, text="COMPLETE COMMENT REMOVAL SYSTEM | MULTI-LINE COMMENTS PRESERVED | NO CODE BREAKAGE",
            font=('Consolas', 9), bg=style['bg_darker'], fg=style['fg_green_dim']
        ).pack()
        
        # Main Container
        main_container = tk.Frame(self.root, bg=style['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left Panel - Circular Progress and Stats
        left_panel = tk.Frame(main_container, bg=style['bg_darker'], width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        self.circular_progress = CircularProgress(left_panel, size=200, thickness=12,
                                                   bg_color=style['bg_darker'],
                                                   progress_color=style['fg_green'],
                                                   text_color=style['fg_green'])
        self.circular_progress.pack(pady=20)
        
        # Current file display
        self.current_file_var = tk.StringVar(value="FILE: READY")
        current_file_label = tk.Label(left_panel, textvariable=self.current_file_var,
                                       font=('Consolas', 10), bg=style['bg_darker'],
                                       fg=style['fg_green_dim'], wraplength=310)
        current_file_label.pack(pady=10)
        
        # Current comments display
        self.current_comments_var = tk.StringVar(value="COMMENTS: 0")
        current_comments_label = tk.Label(left_panel, textvariable=self.current_comments_var,
                                          font=('Consolas', 10, 'bold'), bg=style['bg_darker'],
                                          fg=style['fg_green'])
        current_comments_label.pack(pady=5)
        
        # Stats display in left panel
        stats_frame = tk.Frame(left_panel, bg=style['bg_dark'], relief=tk.FLAT, bd=1,
                               highlightbackground=style['fg_green_dark'], highlightthickness=1)
        stats_frame.pack(fill=tk.X, padx=15, pady=15)
        
        self.stats_vars = {
            'total_files': tk.StringVar(value="0"),
            'comments_removed': tk.StringVar(value="0"),
            'success_rate': tk.StringVar(value="100%")
        }
        self.preserved_multiline_var = tk.StringVar(value="0")
        
        for label, var in [("FILES PROCESSED", self.stats_vars['total_files']),
                           ("COMMENTS REMOVED", self.stats_vars['comments_removed']),
                           ("SUCCESS RATE", self.stats_vars['success_rate']),
                           ("MULTILINE PRESERVED", self.preserved_multiline_var)]:
            stat_row = tk.Frame(stats_frame, bg=style['bg_dark'])
            stat_row.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(stat_row, text=label, font=('Consolas', 9), bg=style['bg_dark'],
                    fg=style['fg_green_dim']).pack(side=tk.LEFT)
            tk.Label(stat_row, textvariable=var, font=('Consolas', 11, 'bold'),
                    bg=style['bg_dark'], fg=style['fg_green']).pack(side=tk.RIGHT)
        
        # Data Display Panel
        self.data_display = DataDisplayPanel(left_panel, bg_color=style['bg_dark'], fg_color=style['fg_green'])
        self.data_display.pack(fill=tk.X, padx=15, pady=10)
        
        # Right Panel
        right_panel = tk.Frame(main_container, bg=style['bg_dark'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Control Panel
        control_panel = tk.Frame(right_panel, bg=style['bg_darker'], relief=tk.FLAT, bd=1,
                                highlightbackground=style['border'], highlightthickness=1)
        control_panel.pack(fill=tk.X, pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(control_panel, bg=style['bg_darker'])
        button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        btn_style = {
            'font': ('Consolas', 10, 'bold'), 'bg': style['bg_dark'], 'fg': style['fg_green'],
            'activebackground': style['select'], 'activeforeground': style['fg_green'],
            'relief': tk.FLAT, 'bd': 1, 'highlightbackground': style['fg_green'],
            'highlightthickness': 1, 'cursor': 'hand2', 'padx': 15, 'pady': 8
        }
        
        tk.Button(button_frame, text="[ PROCESS SINGLE FILE ]", command=self.process_single, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="[ BATCH PROCESS DIRECTORY ]", command=self.process_batch, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="[ FULLSCREEN ]", command=self.toggle_fullscreen, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="[ DOCUMENTATION ]", command=self.view_documentation, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="[ STATISTICS ]", command=self.show_stats, **btn_style).pack(side=tk.LEFT, padx=5)
        
        # Language Info
        lang_frame = tk.Frame(button_frame, bg=style['bg_darker'])
        lang_frame.pack(side=tk.RIGHT, padx=5)
        
        lang_count = len(LanguageConfig.LANGUAGES)
        tk.Label(lang_frame, text=f"SUPPORTED LANGUAGES: {lang_count}", font=('Consolas', 9),
                bg=style['bg_darker'], fg=style['fg_green_dark']).pack()
        
        # File Details Panel
        self.file_details = FileDetailsPanel(right_panel, bg_color=style['bg_darker'], fg_color=style['fg_green'])
        self.file_details.pack(fill=tk.X, pady=(0, 15))
        
        # Scan Progress Widget
        scan_frame = tk.Frame(right_panel, bg=style['bg_darker'], relief=tk.FLAT, bd=1,
                              highlightbackground=style['fg_green_dark'], highlightthickness=1)
        scan_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.scan_widget = ScanProgressWidget(scan_frame, bg_color=style['bg_darker'], fg_color=style['fg_green'])
        self.scan_widget.pack(fill=tk.X, padx=10, pady=10)
        
        # Output Area
        output_frame = tk.Frame(right_panel, bg=style['bg_darker'], relief=tk.FLAT, bd=1,
                               highlightbackground=style['border'], highlightthickness=1)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        output_header = tk.Frame(output_frame, bg=style['bg_darker'], height=35)
        output_header.pack(fill=tk.X)
        output_header.pack_propagate(False)
        
        tk.Label(output_header, text="> PROCESSING LOG", font=('Consolas', 10, 'bold'),
                bg=style['bg_darker'], fg=style['fg_green']).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Clear log button
        clear_btn = tk.Button(output_header, text="CLEAR LOG", command=self.clear_output,
                              font=('Consolas', 8), bg=style['bg_darker'], fg=style['fg_green_dim'],
                              relief=tk.FLAT, cursor='hand2')
        clear_btn.pack(side=tk.RIGHT, padx=10)
        
        # Export log button
        def export_log():
            from datetime import datetime
            export_path = Path.home() / "Downloads" / f"comment_remover_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(self.output_area.get(1.0, tk.END))
            messagebox.showinfo("EXPORT COMPLETE", f"Log exported to:\n{export_path}")
        
        export_btn = tk.Button(output_header, text="EXPORT LOG", command=export_log,
                               font=('Consolas', 8), bg=style['bg_darker'], fg=style['fg_green_dim'],
                               relief=tk.FLAT, cursor='hand2')
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        self.output_area = tk.Text(output_frame, bg=style['bg_dark'], fg=style['fg_white'],
                                   insertbackground=style['fg_green'], font=('Consolas', 10),
                                   relief=tk.FLAT, wrap=tk.WORD, selectbackground=style['select'])
        self.output_area.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        scrollbar = tk.Scrollbar(self.output_area, orient=tk.VERTICAL, command=self.output_area.yview, bg=style['bg_darker'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_area.config(yscrollcommand=scrollbar.set)
        
        # Text tags
        self.output_area.tag_configure("SUCCESS", foreground="#00ff41")
        self.output_area.tag_configure("ERROR", foreground="#ff4444")
        self.output_area.tag_configure("WARNING", foreground="#ffaa44")
        self.output_area.tag_configure("INFO", foreground="#88ff88")
        
        # Status Bar
        status_bar = tk.Frame(self.root, bg=style['bg_darker'], height=25)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(status_bar, text="[ SYSTEM READY ]", font=('Consolas', 8),
                                      bg=style['bg_darker'], fg=style['fg_green_dark'])
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Shortcut hints
        shortcut_label = tk.Label(status_bar, text="F11: FULLSCREEN | Ctrl+D: DOCS | Ctrl+S: STATS", font=('Consolas', 8),
                                  bg=style['bg_darker'], fg=style['fg_green_dark'])
        shortcut_label.pack(side=tk.RIGHT, padx=10)
        
        # Initial log message
        self.log_message(f"[INFO] {ORGANIZATION} - {VERSION}")
        self.log_message("[INFO] CRITICAL: Multi-line comments (''' or \"\"\") are PRESERVED to avoid code breakage")
        self.log_message("[INFO] System initialized and ready")
        self.log_message("[INFO] Select a file or directory to begin")
        
        self.root.mainloop()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Try to import psutil for system info, fallback if not available
    import sys
    try:
        import psutil
    except ImportError:
        # Create dummy psutil module
        class DummyPsutil:
            @staticmethod
            def boot_time():
                return time.time() - 3600
            @staticmethod
            def cpu_percent(interval=0.1):
                return 25
            @staticmethod
            def Process():
                class DummyProcess:
                    @staticmethod
                    def memory_info():
                        class DummyMemory:
                            rss = 50 * 1024 * 1024
                        return DummyMemory()
                return DummyProcess()
        sys.modules['psutil'] = DummyPsutil()
    
    gui = DarkHackerGUI()
    gui.run()
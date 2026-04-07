"""
UNIVERSAL COMMENT REMOVER - DARK HACKER EDITION
Complete Multi-Language Comment Removal System with Circular Progress
Creates new files without comments | Preserves originals | Batch processing
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
import math

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
            'string_aware': True
        },
        'javascript': {
            'extensions': ['.js', '.jsx', '.mjs', '.cjs'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'preserve_shebang': True,
            'string_aware': True
        },
        'typescript': {
            'extensions': ['.ts', '.tsx'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'html': {
            'extensions': ['.html', '.htm', '.xhtml'],
            'single_line': None,
            'multi_line_start': ['<!--'],
            'multi_line_end': ['-->'],
            'string_aware': False
        },
        'css': {
            'extensions': ['.css', '.scss', '.sass', '.less'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'cpp': {
            'extensions': ['.cpp', '.cc', '.cxx', '.c++', '.h', '.hpp', '.hxx'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'c': {
            'extensions': ['.c', '.h'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'java': {
            'extensions': ['.java'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'csharp': {
            'extensions': ['.cs'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'ruby': {
            'extensions': ['.rb', '.rbw'],
            'single_line': r'#.*$',
            'multi_line_start': ['=begin'],
            'multi_line_end': ['=end'],
            'preserve_shebang': True,
            'string_aware': True
        },
        'go': {
            'extensions': ['.go'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'rust': {
            'extensions': ['.rs'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'php': {
            'extensions': ['.php'],
            'single_line': r'(//|#).*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'swift': {
            'extensions': ['.swift'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'kotlin': {
            'extensions': ['.kt', '.kts'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'sql': {
            'extensions': ['.sql'],
            'single_line': r'(--|#).*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
        },
        'xml': {
            'extensions': ['.xml', '.xsd', '.xsl', '.xslt'],
            'single_line': None,
            'multi_line_start': ['<!--'],
            'multi_line_end': ['-->'],
            'string_aware': False
        },
        'yaml': {
            'extensions': ['.yaml', '.yml'],
            'single_line': r'#.*$',
            'multi_line_start': [],
            'multi_line_end': [],
            'string_aware': True
        },
        'json': {
            'extensions': ['.json'],
            'single_line': None,
            'multi_line_start': [],
            'multi_line_end': [],
            'string_aware': True,
            'no_comments': True
        },
        'shell': {
            'extensions': ['.sh', '.bash', '.zsh', '.fish'],
            'single_line': r'#.*$',
            'multi_line_start': [": '"],
            'multi_line_end': ["'"],
            'preserve_shebang': True,
            'string_aware': True
        },
        'perl': {
            'extensions': ['.pl', '.pm'],
            'single_line': r'#.*$',
            'multi_line_start': ['=pod', '=cut'],
            'multi_line_end': ['=cut', '=pod'],
            'preserve_shebang': True,
            'string_aware': True
        },
        'lua': {
            'extensions': ['.lua'],
            'single_line': r'--.*$',
            'multi_line_start': ['--[['],
            'multi_line_end': [']]'],
            'string_aware': True
        },
        'r': {
            'extensions': ['.r', '.R'],
            'single_line': r'#.*$',
            'multi_line_start': [],
            'multi_line_end': [],
            'string_aware': True
        },
        'dart': {
            'extensions': ['.dart'],
            'single_line': r'//.*$',
            'multi_line_start': ['/*'],
            'multi_line_end': ['*/'],
            'string_aware': True
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
            'string_aware': False
        })


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
# COMMENT REMOVER ENGINE
# ============================================================================

class CommentRemover:
    
    def __init__(self):
        self.log_messages = []
        self.progress_callback = None
        self.comments_removed = 0
        self.total_lines = 0
        
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
    
    def remove_all_comments(self, content: str, language: str, config: Dict, file_progress_callback=None) -> Tuple[str, int, int]:
        lines = content.splitlines(True)
        self.total_lines = len(lines)
        result_lines = []
        
        in_string = False
        string_char = None
        in_multiline_comment = False
        multiline_end_pattern = None
        comments_removed = 0
        
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
                        
                        # Preserve Python docstrings
                        if language == 'python' and start_pattern in ['"""', "'''"]:
                            prev_line = lines[i-1] if i > 0 else ""
                            if i == 0 or prev_line.strip().startswith(('class ', 'def ')) or prev_line.strip() == '':
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
                                break
                        
                        in_multiline_comment = True
                        multiline_end_pattern = end_pattern
                        
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
        
        return cleaned_content, comments_removed, self.total_lines
    
    def process_file(self, file_path: str, output_path: str, progress_callback=None) -> Dict[str, Any]:
        result = {
            'success': False,
            'language': 'unknown',
            'comments_removed': 0,
            'total_lines': 0,
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
            
            cleaned_content, comments_count, total_lines = self.remove_all_comments(
                original_content, language, config, file_progress_cb
            )
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            result['comments_removed'] = comments_count
            result['total_lines'] = total_lines
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
    
    def process_directory(self, source_dir: str, output_dir: str, extensions: List[str] = None, 
                          progress_callback=None, file_callback=None) -> Dict[str, Any]:
        
        results = {
            'total_files': 0,
            'processed_files': 0,
            'failed_files': 0,
            'skipped_files': 0,
            'total_comments_removed': 0,
            'total_lines_processed': 0,
            'details': []
        }
        
        source_path = Path(source_dir)
        output_path = Path(output_dir)
        
        # Collect files
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
        
        results['total_files'] = len(files)
        
        for idx, file_path in enumerate(files):
            rel_path = file_path.relative_to(source_path)
            output_file = output_path / rel_path
            
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
                'language': result.get('language', 'unknown'),
                'errors': result.get('errors', [])
            })
            
            if result['success']:
                results['processed_files'] += 1
                results['total_comments_removed'] += result.get('comments_removed', 0)
                results['total_lines_processed'] += result.get('total_lines', 0)
            else:
                results['failed_files'] += 1
            
            if file_callback:
                file_callback(f"COMPLETE:{result['success']}:{result.get('comments_removed', 0)}")
        
        if progress_callback:
            progress_callback(f"OVERALL:100:{results['total_files']}/{results['total_files']}")
        
        return results


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
            
            self.root.after(0, lambda: self.single_complete(result, output_path))
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def single_complete(self, result: Dict, output_path: Path):
        self.circular_progress.update_progress(100)
        
        if result['success']:
            self.log_message("")
            self.log_message("=" * 80)
            self.log_message("[SUCCESS] FILE PROCESSED SUCCESSFULLY")
            self.log_message(f"[INFO] LANGUAGE: {result['language'].upper()}")
            self.log_message(f"[INFO] COMMENTS REMOVED: {result['comments_removed']}")
            self.log_message(f"[INFO] OUTPUT SAVED: {output_path}")
            self.log_message("=" * 80)
            
            messagebox.showinfo(
                "PROCESSING COMPLETE",
                f"FILE PROCESSED SUCCESSFULLY\n\n"
                f"LANGUAGE: {result['language'].upper()}\n"
                f"COMMENTS REMOVED: {result['comments_removed']}\n\n"
                f"OUTPUT: {output_path}"
            )
        else:
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
            f"Original files will remain unchanged.\n\n"
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
        
        self.log_message(f"[START] Batch processing: {source_dir}")
        self.log_message(f"[INFO] Output directory: {output_dir}")
        
        def process_thread():
            processor = BatchProcessor()
            
            def progress_callback(msg):
                self.root.after(0, lambda: self.update_circular_progress(msg))
            
            def file_callback(msg):
                self.root.after(0, lambda: self.update_circular_progress(msg))
            
            results = processor.process_directory(source_dir, str(output_dir), 
                                                  progress_callback=progress_callback,
                                                  file_callback=file_callback)
            
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
        self.log_message(f"[STATS] TOTAL LINES PROCESSED: {results['total_lines_processed']}")
        self.log_message(f"[INFO] OUTPUT DIRECTORY: {output_dir}")
        self.log_message("-" * 40)
        
        # Show summary of processed files
        success_count = 0
        for detail in results['details']:
            if detail['success']:
                success_count += 1
                self.log_message(f"[OK] {Path(detail['file']).name} | {detail['language']} | {detail['comments_removed']} comments")
            else:
                self.log_message(f"[FAIL] {Path(detail['file']).name} | {detail['language']}")
                for err in detail.get('errors', []):
                    self.log_message(f"       ERROR: {err}")
        
        self.log_message("=" * 80)
        
        messagebox.showinfo(
            "BATCH PROCESSING COMPLETE",
            f"BATCH PROCESSING COMPLETED\n\n"
            f"TOTAL FILES: {results['total_files']}\n"
            f"SUCCESSFUL: {results['processed_files']}\n"
            f"FAILED: {results['failed_files']}\n"
            f"TOTAL COMMENTS REMOVED: {results['total_comments_removed']}\n"
            f"TOTAL LINES PROCESSED: {results['total_lines_processed']}\n\n"
            f"OUTPUT DIRECTORY: {output_dir}"
        )
        
        self.is_processing = False
        self.circular_progress.update_progress(0)
        if self.current_file_var:
            self.current_file_var.set("FILE: READY")
        if self.current_comments_var:
            self.current_comments_var.set("COMMENTS: 0")
    
    def run(self):
        self.root = tk.Tk()
        self.root.title("UNIVERSAL COMMENT REMOVER v4.0")
        self.root.geometry("1300x850")
        self.root.minsize(1100, 700)
        
        style = self.setup_styles()
        
        # Header
        header_frame = tk.Frame(self.root, bg=style['bg_darker'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame, text="UNIVERSAL COMMENT REMOVER", 
            font=('Consolas', 22, 'bold'), bg=style['bg_darker'], fg=style['fg_green']
        ).pack(pady=10)
        
        tk.Label(
            header_frame, text="COMPLETE COMMENT REMOVAL SYSTEM | PRESERVES ORIGINAL FILES",
            font=('Consolas', 10), bg=style['bg_darker'], fg=style['fg_green_dim']
        ).pack()
        
        # Main Container
        main_container = tk.Frame(self.root, bg=style['bg_dark'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left Panel - Circular Progress
        left_panel = tk.Frame(main_container, bg=style['bg_darker'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        self.circular_progress = CircularProgress(left_panel, size=200, thickness=12,
                                                   bg_color=style['bg_darker'],
                                                   progress_color=style['fg_green'],
                                                   text_color=style['fg_green'])
        self.circular_progress.pack(pady=40)
        
        # Current file display
        self.current_file_var = tk.StringVar(value="FILE: READY")
        current_file_label = tk.Label(left_panel, textvariable=self.current_file_var,
                                       font=('Consolas', 10), bg=style['bg_darker'],
                                       fg=style['fg_green_dim'], wraplength=280)
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
        stats_frame.pack(fill=tk.X, padx=20, pady=30)
        
        self.stats_vars = {
            'total_files': tk.StringVar(value="0"),
            'comments_removed': tk.StringVar(value="0"),
            'success_rate': tk.StringVar(value="100%")
        }
        
        for label, var in [("FILES", self.stats_vars['total_files']),
                           ("COMMENTS", self.stats_vars['comments_removed']),
                           ("RATE", self.stats_vars['success_rate'])]:
            stat_row = tk.Frame(stats_frame, bg=style['bg_dark'])
            stat_row.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(stat_row, text=label, font=('Consolas', 9), bg=style['bg_dark'],
                    fg=style['fg_green_dim']).pack(side=tk.LEFT)
            tk.Label(stat_row, textvariable=var, font=('Consolas', 12, 'bold'),
                    bg=style['bg_dark'], fg=style['fg_green']).pack(side=tk.RIGHT)
        
        # Right Panel
        right_panel = tk.Frame(main_container, bg=style['bg_dark'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Control Panel
        control_panel = tk.Frame(right_panel, bg=style['bg_darker'], relief=tk.FLAT, bd=1,
                                highlightbackground=style['border'], highlightthickness=1)
        control_panel.pack(fill=tk.X, pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(control_panel, bg=style['bg_darker'])
        button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        btn_style = {
            'font': ('Consolas', 11, 'bold'), 'bg': style['bg_dark'], 'fg': style['fg_green'],
            'activebackground': style['select'], 'activeforeground': style['fg_green'],
            'relief': tk.FLAT, 'bd': 1, 'highlightbackground': style['fg_green'],
            'highlightthickness': 1, 'cursor': 'hand2', 'padx': 20, 'pady': 8
        }
        
        tk.Button(button_frame, text="[ PROCESS SINGLE FILE ]", command=self.process_single, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="[ BATCH PROCESS DIRECTORY ]", command=self.process_batch, **btn_style).pack(side=tk.LEFT, padx=5)
        
        # Language Info
        lang_frame = tk.Frame(button_frame, bg=style['bg_darker'])
        lang_frame.pack(side=tk.RIGHT, padx=5)
        
        lang_count = len(LanguageConfig.LANGUAGES)
        tk.Label(lang_frame, text=f"SUPPORTED LANGUAGES: {lang_count}", font=('Consolas', 9),
                bg=style['bg_darker'], fg=style['fg_green_dark']).pack()
        
        # Output Area
        output_frame = tk.Frame(right_panel, bg=style['bg_darker'], relief=tk.FLAT, bd=1,
                               highlightbackground=style['border'], highlightthickness=1)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        output_header = tk.Frame(output_frame, bg=style['bg_darker'], height=30)
        output_header.pack(fill=tk.X)
        output_header.pack_propagate(False)
        
        tk.Label(output_header, text="> PROCESSING LOG", font=('Consolas', 10, 'bold'),
                bg=style['bg_darker'], fg=style['fg_green']).pack(side=tk.LEFT, padx=10, pady=5)
        
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
        
        tk.Label(status_bar, text=f"v4.0 | {datetime.now().strftime('%Y-%m-%d')}", font=('Consolas', 8),
                bg=style['bg_darker'], fg=style['fg_green_dark']).pack(side=tk.RIGHT, padx=10)
        
        self.root.mainloop()


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    gui = DarkHackerGUI()
    gui.run()
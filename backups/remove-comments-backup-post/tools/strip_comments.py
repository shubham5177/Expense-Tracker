#!/usr/bin/env python3
import os
import re
import sys
import shutil
from pathlib import Path
import tokenize
import io

ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / 'backups' / 'remove-comments-backup-post'
EXCLUDE_DIRS = {'backups', '.git', '__pycache__'}

EXT_PATTERNS = ['*.py', '*.js', '*.html', '*.css']

changed = []
errors = []

def is_excluded(path: Path):
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False

def backup_file(src: Path, dst_base: Path):
    dst = dst_base / src.relative_to(ROOT)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

def strip_python(path: Path):
    try:
        with tokenize.open(path) as f:
            src = f.read()
        tokens = tokenize.generate_tokens(io.StringIO(src).readline)
        new_tokens = []
        for toknum, tokval, start, end, line in tokens:
            if toknum == tokenize.COMMENT:
                # skip comment tokens entirely
                continue
            new_tokens.append((toknum, tokval))
        new_src = tokenize.untokenize(new_tokens)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_src)
        return True
    except Exception as e:
        errors.append((str(path), str(e)))
        return False

JS_LINE_COMMENT_RE = re.compile(r'//.*')
JS_BLOCK_COMMENT_RE = re.compile(r'/\*.*?\*/', re.DOTALL)
HTML_COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)

def strip_js_css(path: Path):
    try:
        text = path.read_text(encoding='utf-8')
        # remove block comments first
        text2 = JS_BLOCK_COMMENT_RE.sub('', text)
        # remove line comments but avoid lines with http:// or https://
        lines = text2.splitlines()
        out_lines = []
        for ln in lines:
            if 'http://' in ln or 'https://' in ln:
                out_lines.append(ln)
                continue
            # naive removal of // comments
            if '//' in ln:
                i = ln.find('//')
                out_lines.append(ln[:i].rstrip())
            else:
                out_lines.append(ln)
        new_text = '\n'.join(out_lines).rstrip() + '\n'
        path.write_text(new_text, encoding='utf-8')
        return True
    except Exception as e:
        errors.append((str(path), str(e)))
        return False

def strip_html(path: Path):
    try:
        text = path.read_text(encoding='utf-8')
        new_text = HTML_COMMENT_RE.sub('', text)
        path.write_text(new_text, encoding='utf-8')
        return True
    except Exception as e:
        errors.append((str(path), str(e)))
        return False


def main():
    print('Root:', ROOT)
    # create backup dir
    if BACKUP_DIR.exists():
        print('Backup dir already exists:', BACKUP_DIR)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # collect files
    files = []
    for ext in ['py', 'js', 'html', 'css']:
        for p in ROOT.rglob(f'*.{ext}'):
            if is_excluded(p):
                continue
            files.append(p)

    print(f'Found {len(files)} files to process')

    for p in files:
        try:
            backup_file(p, BACKUP_DIR)
        except Exception as e:
            errors.append((str(p), 'backup failed: ' + str(e)))

    for p in files:
        suffix = p.suffix.lower()
        ok = False
        if suffix == '.py':
            ok = strip_python(p)
        elif suffix in ('.js', '.css'):
            ok = strip_js_css(p)
        elif suffix == '.html':
            ok = strip_html(p)
        if ok:
            changed.append(str(p))

    print('\nProcessing complete.')
    print(f'Files changed: {len(changed)}')
    for c in changed:
        print(' -', c)
    if errors:
        print('\nErrors:')
        for e in errors:
            print(' -', e[0], e[1])
    # exit code
    if errors:
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()

import re
import argparse
import os
from typing import Set, Dict, List, Tuple

def find_citation_keys(tex_content: str) -> Tuple[Set[str], Set[str]]:
    """
    Finds all active and commented-out citation keys in the .tex file content.
    It splits each line by the comment character '%' to differentiate.
    Returns a tuple of two sets: (active_keys, commented_keys).
    """
    citation_pattern = re.compile(r'\\cite[a-zA-Z]*?(?:\[[^\]]*\])*\{([^}]+)\}')
    active_keys = set()
    commented_keys = set()

    for line in tex_content.splitlines():
        # Split line at the first unescaped '%' to separate active content from comments.
        # This handles cases like '... some text % \cite{key}'
        parts = re.split(r'(?<!\\)%', line, 1)
        active_part = parts[0]
        comment_part = parts[1] if len(parts) > 1 else ''

        # Find keys in the active part of the line
        active_matches = citation_pattern.findall(active_part)
        for key_group in active_matches:
            keys = [key.strip() for key in key_group.split(',')]
            active_keys.update(keys)

        # Find keys in the commented part of the line
        commented_matches = citation_pattern.findall(comment_part)
        for key_group in commented_matches:
            keys = [key.strip() for key in key_group.split(',')]
            commented_keys.update(keys)

    return active_keys, commented_keys

def parse_bib_file(bib_content: str) -> Dict[str, str]:
    """
    Parses the .bib file and extracts all entries into a dictionary.
    The keys are the citation keys, and the values are the full BibTeX entries.
    """
    bib_entries = {}
    # This regex looks for entries starting with @type{key, ... }
    # It uses a non-greedy match to find the closing brace of each entry.
    entry_pattern = re.compile(r'(@[a-zA-Z]+\{[^,]+,.*?\n\})', re.DOTALL)
    
    # Find all top-level BibTeX entries
    entries = entry_pattern.findall(bib_content)
    
    for entry in entries:
        # The key is the part between the first '{' and the first ','
        key_match = re.search(r'@[a-zA-Z]+\{([^,]+),', entry)
        if key_match:
            key = key_match.group(1).strip()
            bib_entries[key] = entry
            
    return bib_entries

def extract_used_entries(tex_file_path: str, bib_file_path: str) -> str:
    """
    Reads the .tex and .bib files, finds used citations, and returns a new .bib file content.
    """
    try:
        with open(tex_file_path, 'r', encoding='utf-8') as f:
            tex_content = f.read()
    except FileNotFoundError:
        return f"Error: The file '{tex_file_path}' was not found."
    except Exception as e:
        return f"Error reading '{tex_file_path}': {e}"

    try:
        with open(bib_file_path, 'r', encoding='utf-8') as f:
            bib_content = f.read()
    except FileNotFoundError:
        return f"Error: The file '{bib_file_path}' was not found."
    except Exception as e:
        return f"Error reading '{bib_file_path}': {e}"
        
    # Step 1: Find all active and commented citation keys in the .tex file
    active_keys, commented_keys = find_citation_keys(tex_content)
    
    # Warn about commented keys that are not also used actively
    unique_commented = commented_keys - active_keys
    if unique_commented:
        print("\nWarning: The following citation keys were found in comments and will be ignored:")
        for key in sorted(list(unique_commented)):
            print(f"  - {key}")

    if not active_keys:
        print("\nNo active citation keys found in the .tex file.")
        return ""
        
    print(f"\nFound {len(active_keys)} unique active citation keys in '{os.path.basename(tex_file_path)}'.")

    # Step 2: Parse the .bib file to get all available entries
    all_bib_entries = parse_bib_file(bib_content)
    if not all_bib_entries:
        print(f"No BibTeX entries found in '{os.path.basename(bib_file_path)}'.")
        return ""
        
    print(f"Found {len(all_bib_entries)} entries in '{os.path.basename(bib_file_path)}'.")

    # Step 3: Filter the BibTeX entries based on the active keys
    new_bib_content_list = []
    for key in sorted(list(active_keys)): # Sort for consistent output
        if key in all_bib_entries:
            new_bib_content_list.append(all_bib_entries[key])
        else:
            print(f"Warning: Citation key '{key}' found in .tex file but not in .bib file.")

    return "\n".join(new_bib_content_list)

def main():
    """
    Main function to handle command-line arguments and run the extraction process.
    """
    parser = argparse.ArgumentParser(
        description='Extract used BibTeX entries from a .bib file based on citations in a .tex file.'
    )
    parser.add_argument('tex_file', help='The path to the input .tex file.')
    parser.add_argument('bib_file', help='The path to the input .bib file.')
    parser.add_argument(
        '-o', '--output', 
        help='The path for the output .bib file. Defaults to "minibib_output.bib".',
        default='minibib_output.bib'
    )

    args = parser.parse_args()

    # Get the content for the new .bib file
    new_bib_content = extract_used_entries(args.tex_file, args.bib_file)
    
    if new_bib_content and not new_bib_content.startswith("Error"):
        # Write the new content to the output file
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(new_bib_content)
            print(f"\nSuccessfully created new .bib file: '{args.output}'")
        except Exception as e:
            print(f"\nError writing to output file '{args.output}': {e}")

if __name__ == '__main__':
    main()

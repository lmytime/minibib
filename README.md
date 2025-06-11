# BibTeX Entry Extractor for LaTeX
A simple yet powerful Python script to create a clean `.bib` file containing only the references cited in your `.tex` document. This is perfect for cleaning up your bibliography before sharing your project or submitting it to a journal.

# Features
- Extracts Only Used References: Scans your .tex file and pulls only the cited entries from your master .bib file.

- Handles Various Cite Commands: Correctly identifies keys from a wide range of citation commands, including \cite, \citep, \citet, \citealt, etc.

- Parses Complex Citations: Intelligently handles citations with pre-notes and post-notes, like \citep[see][p. 5]{key}.

- Ignores Commented Citations: The script detects citations in commented-out lines (e.g., % \cite{key}) and excludes them from the final bibliography.

- User-Friendly Warnings:

    - Notifies you if a cited key is present in the .tex file but missing from the .bib file.

    - Lists all the citation keys that were found in comments and therefore ignored.

# Prerequisites
- Python 3

No external libraries are needed.

# Install
```sh
pip install minibib
```

# Usage
Run the script from your terminal using the following command structure:

```sh
minibib <path_to_tex_file> <path_to_bib_file> [options]
```

# Arguments
- `tex_file`: The path to your main `.tex` file.

- `bib_file`: The path to your master `.bib` file.

- `-o, --output`: (Optional) The name of the new, cleaned `.bib` file. Defaults to `minibib_output.bib`.

# Example
Imagine you have the following files:

`my_paper.tex`:

```tex
\documentclass{article}

\begin{document}

This paper references the work of \citet{Doe2021}.
We also build on previous results \citep[see Chapter 3]{Smith2019}.


\bibliography{references}
\bibliographystyle{plain}

\end{document}
```

`references.bib`:

```bib
@article{Doe2021,
    author  = {Doe, John},
    title   = {A Groundbreaking Study},
    journal = {Journal of Important Research},
    year    = {2021},
    volume  = {10},
    pages   = {1-20}
}

@book{Smith2019,
    author    = {Smith, Jane},
    title     = {Foundations of Modern Science},
    publisher = {Academic Press},
    year      = {2019}
}

@misc{Jones2022,
    author = {Jones, Sam},
    title  = {Preliminary Thoughts},
    year   = {2022},
    note   = {Unpublished}
}
```

To generate your clean bibliography, run:

```sh
minibib my_paper.tex references.bib -o final_references.bib
```

Console Output:

```
Warning: The following citation keys were found in comments and will be ignored:
  - Jones2022

Found 2 unique active citation keys in 'my_paper.tex'.
Found 3 entries in 'references.bib'.

Successfully created new .bib file: 'final_references.bib'
```

The resulting `final_references.bib` will contain:

```bib
@article{Doe2021,
    author  = {Doe, John},
    title   = {A Groundbreaking Study},
    journal = {Journal of Important Research},
    year    = {2021},
    volume  = {10},
    pages   = {1-20}
}

@book{Smith2019,
    author    = {Smith, Jane},
    title     = {Foundations of Modern Science},
    publisher = {Academic Press},
    year      = {2019}
}
```

# License
This project is open-source under the MIT License.
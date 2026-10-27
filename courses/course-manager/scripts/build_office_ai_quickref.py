#!/usr/bin/env python3
"""Build the office-ai quick reference with its approved 12px (9pt) footer.

Use instead of the generic build/sync --create-pdf entry for this artifact.
All source, fidelity, visual review and promotion gates remain in pdf_build.
The adapter is a declared recipe dependency; changing it marks this PDF stale.
"""
import argparse
import json
import sys
from pathlib import Path
from unittest.mock import patch

MANAGER = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MANAGER))

from src.pdf_sources import PipelineError, load_recipe
from src.pdf_build import build

FOOTER = '<div style="font-size:12px;width:100%;text-align:center">Page <span class="pageNumber"></span> / <span class="totalPages"></span></div>'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--create-pdf', action='store_true')
    args = parser.parse_args()
    if not args.create_pdf:
        parser.error('PDF authoring requires explicit --create-pdf')
    from playwright.sync_api import Page
    native_pdf = Page.pdf

    def pdf_with_approved_footer(page, *positional, **options):
        expected = FOOTER.replace('font-size:12px', 'font-size:8px')
        if options.get('footer_template') != expected:
            raise PipelineError('Renderer footer changed; inspect the adapter before rebuilding')
        options['footer_template'] = FOOTER
        return native_pdf(page, *positional, **options)

    root = MANAGER.parent
    recipe = load_recipe(root, MANAGER / 'registry/pdf/recipes/office-ai-quickref.json')
    assert recipe['artifact_id'] == 'office-ai-quickref'
    with patch.object(Page, 'pdf', pdf_with_approved_footer):
        result = build(root, recipe, create_pdf=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

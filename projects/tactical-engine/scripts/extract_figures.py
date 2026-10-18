#!/usr/bin/env python3
"""Extract Docling-detected figures from their original PDF with PyMuPDF.

Usage:
 python extract_figures.py /path/to/source.pdf /path/to/docling.json
"""
import argparse
import json
from pathlib import Path
import pymupdf


def main():
    parser = argparse.ArgumentParser(description='Extract figures detected by Docling')
    parser.add_argument('pdf', type=Path)
    parser.add_argument('docling_json', type=Path)
    parser.add_argument('--scale', type=float, default=2.0)
    args = parser.parse_args()
    if args.scale <= 0:
        parser.error('--scale must be positive')
    with args.docling_json.open(encoding='utf-8') as stream:
        data = json.load(stream)
    figures = data.get('pictures', [])
    output_dir = args.docling_json.parent / (args.docling_json.stem + '_images')
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    with pymupdf.open(args.pdf) as doc:
        for index, picture in enumerate(figures, start=1):
            provenances = picture.get('prov') or []
            if not provenances:
                print(f'[SKIP] Figure {index}: no coordinates')
                continue
            prov = provenances[0]
            page_no = prov['page_no']
            if not 1 <= page_no <= len(doc):
                print(f'[SKIP] Figure {index}: invalid page {page_no}')
                continue
            page = doc[page_no - 1]
            bbox = prov['bbox']
            origin = bbox.get('coord_origin', 'BOTTOMLEFT')
            if origin == 'BOTTOMLEFT':
                rect = pymupdf.Rect(bbox['l'], page.rect.height - bbox['t'], bbox['r'], page.rect.height - bbox['b'])
            elif origin == 'TOPLEFT':
                rect = pymupdf.Rect(bbox['l'], bbox['t'], bbox['r'], bbox['b'])
            else:
                print(f'[SKIP] Figure {index}: unsupported origin {origin}')
                continue
            rect = rect.normalize() & page.rect
            if rect.is_empty or rect.is_infinite:
                print(f'[SKIP] Figure {index}: empty crop')
                continue
            filename = f'figure_{index:03d}_page_{page_no:02d}.png'
            page.get_pixmap(matrix=pymupdf.Matrix(args.scale, args.scale), clip=rect, alpha=False).save(str(output_dir / filename))
            manifest.append({
                'figure_index': index,
                'self_ref': picture.get('self_ref'),
                'page': page_no,
                'file': filename,
                'bbox': bbox,
                'captions': [c.get('$ref') for c in picture.get('captions', [])],
            })
            print(f'[OK] {filename}')
    manifest_path = output_dir / 'images.json'
    with manifest_path.open('w', encoding='utf-8') as stream:
        json.dump(manifest, stream, indent=2, ensure_ascii=False)
    print(f'Completed: {len(manifest)}/{len(figures)} images in {output_dir}')


if __name__ == '__main__':
    main()

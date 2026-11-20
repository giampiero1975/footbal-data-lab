"""Run the authorized V10-02 with the digest-pinned linked v2 catalog."""
import sys

from qwen27_mmap_attempt_01 import PROJECT, main


if __name__ == '__main__':
    sys.exit(main('qwen27-mmap-on-26112006',
                  PROJECT / 'evaluation/quality_first_qwen27_mmap_on_03',
                  provision_catalog_v2=True))

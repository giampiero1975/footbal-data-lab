"""Continue V10-02 after the zero-POST catalog rejection, with a new attempt."""
import sys

from qwen27_mmap_attempt_01 import PROJECT, main


if __name__ == '__main__':
    sys.exit(main('qwen27-mmap-on-26112005',
                  PROJECT / 'evaluation/quality_first_qwen27_mmap_on_02',
                  provision_catalog_v2=True))

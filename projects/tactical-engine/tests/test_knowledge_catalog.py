import importlib.util
from pathlib import Path
import unittest

PATH=Path(__file__).parents[1]/"api/knowledge_catalog.py"
spec=importlib.util.spec_from_file_location("knowledge_catalog",PATH)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)


class KnowledgeCatalogTests(unittest.TestCase):
    def setUp(self):
        self.rows={
            "ids":["a","b","c"],
            "documents":["Pressing alto coordinato","Costruzione dal basso","Transizione e pressing"],
            "metadatas":[
                {"source":"Manuale A","source_pdf":"/a.pdf","source_relative":"a.json","source_json":"/a.json","page_numbers":"[1]","chunk_index":0,"headings":"[]","raw_text":"x"},
                {"source":"Manuale A","source_pdf":"/a.pdf","source_relative":"a.json","source_json":"/a.json","page_numbers":"[2]","chunk_index":1,"headings":"[]","raw_text":"x"},
                {"source":"Manuale B","source_pdf":"/b.pdf","source_relative":"b.json","source_json":"/b.json","page_numbers":"[4, 5]","chunk_index":0,"headings":"[]","raw_text":""},
            ],
        }

    def test_aggregate_exact_counts_and_provenance(self):
        out=m.aggregate_rows("test",{"hnsw:space":"cosine"},self.rows)
        self.assertEqual((out["chunk_count"],out["document_count"]),(3,2))
        self.assertEqual(out["documents"][0]["pages"],[1,2])
        self.assertTrue(out["documents"][0]["origin_complete"])
        self.assertEqual(out["empty_raw_text_count"],1)

    def test_lexical_search_preserves_source_and_page(self):
        out=m.aggregate_rows("test",{},self.rows)
        found=m.search_catalog(out,"pressing",10)
        self.assertEqual([x["id"] for x in found],["a","c"])
        self.assertEqual(found[0]["pages"],[1])

    def test_short_or_empty_query_returns_no_results(self):
        out=m.aggregate_rows("test",{},self.rows)
        self.assertEqual(m.search_catalog(out,"a",10),[])


if __name__ == "__main__": unittest.main()

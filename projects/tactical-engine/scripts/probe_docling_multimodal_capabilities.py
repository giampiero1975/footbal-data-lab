"""Inspect installed Docling picture options without converting documents."""
import json
from importlib.metadata import version

def main():
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    opts = PdfPipelineOptions()
    fields = ["generate_picture_images", "generate_page_images", "do_picture_description", "do_picture_classification", "picture_description_options", "images_scale", "enable_remote_services"]
    data = {"docling_version": version("docling"), "fields": {}}
    for name in fields:
        value = getattr(opts, name, None)
        data["fields"][name] = {"available": name in type(opts).model_fields, "default": str(value)[:120]}
    print(json.dumps(data, indent=2))
if __name__ == "__main__":
    main()

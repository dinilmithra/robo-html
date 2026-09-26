# robo-html

Reusable HTML report rendering for automation projects.

The library is application-neutral: the application supplies its own HTML template and report data. The renderer safely embeds canonical JSON into a self-contained HTML report.

```python
from pathlib import Path
from robo_html import HtmlReportGenerator

html = HtmlReportGenerator.generate_from_json(
    Path("report.json"),
    template_path=Path("templates/report.html"),
    data_placeholder="__MY_REPORT_DATA__",
)
```


## Publishing

Run `python .\tools\publish_robo_html.py` from the library directory. The publisher auto-uses the library `.venv`, increments the patch version by default, deletes any existing `dist/` directory before building, stages fresh wheel/sdist artifacts, and publishes by default. Use `--build-only` to build without uploading; the incremented version is retained after a successful build.

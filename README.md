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

From the workspace root, preview with `python publishing/publish_robo_html.py --dry-run`, then publish with `python publishing/publish_robo_html.py --publish`. The shared publisher uses the library environment and updates dependent metadata after a successful release. Failed unpublished version changes are rolled back; successful release metadata is committed and pushed. Each project uses its own virtual environment. See [workspace publishing instructions](../PUBLISHING.md).

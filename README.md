# AI PMM Workflows

A collection of AI-powered workflows by **I-Wen (Elaine) Lee** — each one takes a piece of
product-marketing judgment and turns it into a repeatable, runnable system. The throughline:
*the judgment drives the automation, not the other way around.*

Each workflow is a self-contained folder that works two ways — as a **Claude skill**
(`SKILL.md`, invoked in chat) and as a **runnable program** (`python main.py`), sharing the
same code.

## Workflows

| Workflow | What it does | Status |
|---|---|---|
| [**ai-content-pipeline**](./ai-content-pipeline) | Give it a company or an ICP → it proposes buyer personas (you confirm them) → generates a blog + a newsletter tailored to each persona → simulates engagement → recommends what to publish next. Demonstrated on Zip & Shopify. | ✅ Live |

*New workflows are added here only once they run end-to-end and produce real output.*

## Running any workflow

```bash
cd ai-content-pipeline
pip install -r requirements.txt
python main.py run --company zip      # built-in example, no API keys needed
```

See each workflow's own README for details.

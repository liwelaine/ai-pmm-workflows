# AI PMM Workflows

A portfolio of AI-native product marketing workflows that show how product marketers can use LLMs, automation, and lightweight systems to improve audience research, content generation, campaign execution, and performance optimization.

This repository is designed as a product marketing portfolio project, not just a code demo. It shows how AI can help structure repeatable GTM workflows from company context to persona-based messaging, CRM-style distribution, measurement, and next-step recommendations.

---

## Workflow at a Glance

```mermaid
flowchart LR
    A[Company Profile] --> B[Audience Personas]
    B --> C[Persona-Based Content]
    C --> D[CRM-Style Distribution]
    D --> E[Engagement Analytics]
    E --> F[Optimization Recommendations]
    F --> C
```

---

## Featured Workflow: AI Content Pipeline

AI Content Pipeline is a runnable workflow that takes a company profile as input and turns it into segmented marketing content and performance recommendations.

The workflow moves from:

```text
company profile
→ audience personas
→ blog and newsletter content
→ CRM-style distribution
→ engagement analytics
→ optimization recommendations
```

---

## Why I Built This

I built this to demonstrate how I think about AI-native product marketing: not just using AI to generate copy, but designing a repeatable system that connects segmentation, messaging, content creation, distribution, measurement, and optimization.

The goal is to show PMM judgment, GTM thinking, and AI workflow design in one practical project.

---

## What This Demonstrates

- Audience segmentation
- Messaging and positioning
- Content strategy
- CRM-style campaign execution
- Performance analysis
- AI workflow design
- GTM system thinking
- Turning repeatable marketing processes into scalable systems

---

## Repository Structure

```text
ai-pmm-workflows/
├── ai-content-pipeline/      # Main runnable AI PMM workflow
├── assets/                   # Screenshots and diagrams
├── docs/                     # Portfolio demo page
├── main.py                   # Legacy root runner
├── smoke_test.py             # Legacy root test
└── setup-content-engine.sh   # Setup helper
```

---

## Run Locally

```bash
cd ai-content-pipeline
python main.py run --profile examples/zip.json
```

You can also run another company profile:

```bash
python main.py run --profile examples/shopify.json
python main.py run --profile examples/datadog.json
```

---

## Dashboard

```bash
cd ai-content-pipeline
python dashboard/app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## Detailed Documentation

For the full technical workflow, see:

```text
ai-content-pipeline/README.md
```

For the Claude Skill version, see:

```text
ai-content-pipeline/SKILL.md
```

---

## Future Workflow Ideas

- Competitive positioning analyzer
- ICP research generator
- Sales enablement brief builder
- Customer interview synthesis workflow
- Launch messaging and GTM planning assistant
  

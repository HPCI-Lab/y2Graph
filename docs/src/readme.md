# y2Graph

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

y2Graph (yaml to graph)  is a simple Python tool to build W3C-PROV provenance graphs from workflow descriptions written in YAML.
It uses the prov library to create entities, activities, and their relationships, and can export the results to PROV-JSON and a graph visualization (PNG).

This is useful when having to create large provenance graphs without needing to re-run the entire workflow. 

### Features

- Define workflows in a simple YAML file
- Each task specifies:
    - inputs (UUIDs representing files or data items)
    - outputs (UUIDs for generated results)
- Automatically constructs a PROV document linking tasks and data
- Export to:
    - prov.json (standard W3C PROV format)
    - PNG graph (requires Graphviz)

### Example YAML Workflow

```
tasks:
  - id: task1
    label: "Load Data"
    attributes: 
      - timestamp: 12345
      - context: "training"
    inputs: []
    outputs:
      - "uuid-1234"

  - id: task2
    label: "Process Data"
    attributes: 
      - timestamp: 456677
    inputs:
      - "uuid-1234"
    outputs:
      - "uuid-5678"

  - id: task3
    label: "Analyze Results"
    inputs:
      - "uuid-5678"
    outputs:
      - "uuid-9999"
```

To create the corresponding graph: 

```
y2graph test.yaml
```

### 📂 Output

- output_prov.json: PROV-JSON representation of the workflow
- output_graph.png: Graph visualization of tasks and data flow

![output_graph](./docs/src/assets/images.png)

<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">← Prev</a>
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">🏠 Home</a>
    <a href="installation.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">Next →</a>
</div>

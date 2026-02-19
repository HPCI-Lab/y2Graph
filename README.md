
<div align="center">
  <a href="https://github.com/HPCI-Lab">
    <img src="./assets/HPCI-Lab-t.png" alt="HPCI Lab Logo" width="100" height="100">
  </a>

  <h3 align="center">y2Graph</h3>

  <p align="center">
    A simple Python tool to build W3C-PROV provenance graphs from workflow descriptions written in YAML.
    <br />
    <a href="https://hpci-lab.github.io/y2Graph/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/HPCI-Lab/y2Graph/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/HPCI-Lab/y2Graph/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<br />

<div align="center">
  
[![Contributors](https://img.shields.io/github/contributors/HPCI-Lab/y2Graph?style=for-the-badge)](https://github.com/HPCI-Lab/y2Graph/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/HPCI-Lab/y2Graph?style=for-the-badge)](https://github.com/HPCI-Lab/y2Graph/network/members)
[![Stars](https://img.shields.io/github/stars/HPCI-Lab/y2Graph?style=for-the-badge)](https://github.com/HPCI-Lab/y2Graph/stargazers)
[![Issues](https://img.shields.io/github/issues/HPCI-Lab/y2Graph?style=for-the-badge)](https://github.com/HPCI-Lab/y2Graph/issues)
[![GPLv3 License](https://img.shields.io/badge/LICENCE-GPL3.0-green?style=for-the-badge)](https://opensource.org/licenses/)

</div>

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

### Installation

Check out the [yProv4ML documentation](https://hpci-lab.github.io/yProv4ML/installation.html) page to install graphviz.

Then: 

```
pip install y2graph
```

Or: 

```
git clone https://github.com/HPCI-Lab/y2Graph.git
cd y2Graph
pip install -r requirements.txt
```

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

To create the graph corresponding to the previous code (file named `tmp.yaml`): 

```bash
y2graph tmp.yaml
```

To create an example graph: 

```bash
cd example_images
y2graph example.yaml
```

### 📂 Output

- output_prov.json: PROV-JSON representation of the workflow
- output_graph.pdf: Graph visualization of tasks and data flow

![output_graph](example/output_graph.png)

### Documentation

For detailed information, please refer to the [Documentation](https://hpci-lab.github.io/y2Graph/)

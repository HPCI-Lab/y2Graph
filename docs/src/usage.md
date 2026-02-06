
### Usage

Currently, two usage modalities are available: 

The former simply allows to convert from a yaml to W3C ProvJSON and the respective graph form: 

```bash
y2graph example_join/test1.yaml example_join/test2.yaml --join -j combined.json -o combined.pdf
```

The latter allows to specify multiple yaml files, and to connect the jsons into a single file, as well as creating a common graph representation. This feature uses UIDs to identify shared elements which can be connected.  

```bash
y2graph example_simple/test.yaml -j simple.json -o simple.pdf
```

<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
    <a href=".installation.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">← Prev</a>
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">🏠 Home</a>
    <a href="examples.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">Next →</a>
</div>


### Joined Example

This example allows to specify multiple yaml files, and to connect the jsons into a single file, as well as creating a common graph representation. This feature uses UIDs to identify shared elements which can be connected.  

All data files are present in the `example_join` subdirectory. 

The files `example1.yaml` and `example2.yaml` are used as source, and the program looks for ids the inputs and outputs fields to connect as common elements. 

```bash
cd example_join

y2g example1.yaml example2.yaml --join -j combined.json -o combined.pdf
```

Or: 

```bash
cd example_join

y2graph example1.yaml example2.yaml --join -j combined.json -o combined.pdf
```


![ExampleJoined](./assets/joined.png)

<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
    <a href=".readme.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">← Prev</a>
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">🏠 Home</a>
    <a href="installation.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">Next →</a>
</div>

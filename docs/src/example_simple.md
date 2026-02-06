
### Simple Example

This example allows to convert from a yaml to W3C ProvJSON and the respective graph form. 

All data files are present in the `example_simple` subdirectory. 

The file `example.yaml` is used as source, and the program generates fist a W3C Prov JSON file, and then converts it to pdf, svg or png visualization. 

```bash
cd example_simple

y2g example.yaml -j example.json -o example.pdf
```

Or: 

```bash
cd example_simple

y2graph example.yaml -j example.json -o example.pdf
```

![ExampleSimple](./assets/simple.png)

<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
    <a href=".examples.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">← Prev</a>
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">🏠 Home</a>
    <a href="example_join.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">Next →</a>
</div>

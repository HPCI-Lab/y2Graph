
### Example with Images

This example allows to convert from a yaml to W3C ProvJSON and the respective graph form. In addition, when the path to an image is specified in an entity, the program is able to fetch it and visualize it in the graph. 

All data files are present in the `example_images` subdirectory, with all images in the `imgs` folder. 

The file `example.yaml` is used as source, and the program generates fist a W3C Prov JSON file, and then converts it to pdf, svg or png visualization. 

```bash
cd example_images

y2g example.yaml -j example_with_images.json -o example_with_images.pdf
```

Or: 

```bash
cd example_images

y2graph example.yaml -j example_with_images.json -o example_with_images.pdf
```


![ExampleWithImages](./assets/images.png)

<div style="display: flex; justify-content: center; gap: 10px; margin-top: 20px;">
    <a href=".readme.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">← Prev</a>
    <a href="." style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">🏠 Home</a>
    <a href="installation.md" style="text-decoration: none; background-color: #006269; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; transition: 0.3s;">Next →</a>
</div>

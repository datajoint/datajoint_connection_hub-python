# DataJoint Hub Plugin

This is an official DataJoint Python plugin for connection to DataJoint Hub's hosted instances.

Note: This plugin adds features to the `datajoint` package and thus requires it. Users should not import directly from the plugin but instead simply `import datajoint` to access plugin features.

## Run tests locally

```
$  ./serve.sh up LOCAL
$$ docker exec -it datajoint_connection_hub-python_app_1 sh
$$ nosetests -v --tests=/home/dja/datajoint-python/tests
$$ nosetests -vw tests
$$ exit
$  ./serve.sh down LOCAL
```

Note: Make sure to have a valid Git SSH key to access necessary private repos.
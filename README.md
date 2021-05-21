# DataJoint Hub Plugin

This is an official DataJoint Python plugin for connection to DJNeuro's hosted instances. [https://djneuro.io/services](https://djneuro.io/services)

Note: This plugin adds features to the `datajoint` package and thus requires it. Users should not import directly from the plugin but instead simply `import datajoint` to access plugin features.

## Client Usage

The plugin enables connections to hosted instances by adding support
for a 'hub:' URL scheme to look up database hosts. To configure, simply
install datajoint, the plugin, and set the host URL accordingly. From
here, the plugin will intercept hosts specified using the 'hub://'
URL scheme and connect to the corresponding database.

```
$ pip install datajoint
$ pip install datajoint-connection-hub
$ export DJ_HOST=hub://djhub.io/<orgname>/<pipeline-name>
```


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

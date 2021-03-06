## C++/Qt5 client

This console client uses C++/Qt to interact with the RESTful `progressApi` service of **gae-progress**.

 - To build you need to install [Qt5](http://www.qt.io) and [CMake](https://cmake.org).
 - Point CMake to `clients/cpp-qt5` and select a build directory.
 - Click configure.
 - When asked point `PROGRESS_QT_INSTALL_PATH` to the install directory of Qt5.
 - Click generate.

Open the resulting solution in your C++ IDE and build the solution. This should build an application named `progress`. To query your progresses you simply run

```
> progress list --key YOUR-API-KEY
```

from command line. When all goes well you should see the first batch of your progresses printed to console. Output should look similar to

```
Received 2 items
----------
id: "4639526752354304"
created: "2016-01-13T09:16:06.775000Z"
title: "Cleaning Up"
progress: 10
----------
id: "6117270380085248"
created: "2016-01-13T09:11:30.773000Z"
title: "Training classifier"
progress: 0
----------
```

To create a new progress run
```
> progress create --key YOUR-API-KEY --title "My first progress" --desc "Informative description" --progress 10.0
```

Type

```
> progress --help
```

to see available options.

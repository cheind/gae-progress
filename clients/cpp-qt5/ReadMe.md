## C++/Qt5 client

This client uses [Qt](http://www.qt.io/) to communicate with `progressApi`.
 - To build it you need to install Qt5 and [CMake](https://cmake.org).
 - Point CMake to `clients/cpp-qt5` and select a build directory.
 - Click configure
 - When asked point `PROGRESS_QT_INSTALL_PATH` to the install directory of Qt5.
 - Click generate

Open the resulting solution in your C++ IDE and update `apikey` field to match your API key.
Verify that the URL is pointing to the correct server address. Build the solution.
This should build an application named `progress`. To run it, simply invoke

```
> progress
```

You should receive the first batch of your progresses. Output should look similar to

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

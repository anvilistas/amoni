# Amoni
A command line utility for local development of [Anvil](https://anvil.works) apps.

Amoni gives you:

* A simple command to start a new project and create all the necessary files and folders:

    ```amoni init```

* Pre-configured docker containers for the anvil app server and postgresql database
server to run your app
* Simple commands to start and stop those servers:

    ```
    amoni start

    amoni stop
    ```

* Your app available in your browser at port 3030 on your local machine
* Your database server available on port 5432 on your local machine

* A pre-configured docker container and a simple command to run your test suite:

    ```amoni test```

* Commands to fetch anvil apps and add them to your project as the main app or as
dependencies:

    ```
    amoni install app

    amoni install dependency
    ```

* [Stub files](https://mypy.readthedocs.io/en/stable/stubs.html) that allow your
autocompleter to see what tables are included in your app


[Read the Documentation](https://amoni.readthedocs.io/en/latest/)

[Ask a Question](https://github.com/anvilistas/amoni/discussions)

[Chat with the team](https://matrix.to/#/#anvilistas_community:gitter.im?via=gitter.im&via=matrix.org)

# Transcript robot


## Configurations

you can consult the documentation for configurations [here](docs/2.AppConfigurations.md).


## Supported content

### Input movie types

- `*.mp4`
- `*.ts`

### Output transcript languages

- [Here](docs/2.AppConfigurations.md#supported-languages)


## How to run the project

### Build the image:

```bash
docker build -t transcript-robot .
```

#### Run the container:

```sh
docker run -v
        ./data/in-data/:/data/in-data/:ro \
        ./data/out-data/:/data/out-data/:rw \
        ./data/tmp-data/:/data/tmp-data/:rw \
    transcript-robot
```

#### Run docker-compose:

```bash
docker-compose up --build
```



## Contributing

If you want to contribute to this project, please check how you can configure your development environment [here](docs/1.DevEnvironment.md).

## Introduction

Folder to work with the Airadne framework.

## Endpoints

```bash
{
  people(input: {maxAge: 20, minAge:15}) {
    name,
    age
  }
}
```

```bash
{
  numericAggregatePeople(function:max, field: "age")
}
```

```bash
{
  dateTimeAggregatePeople(function:max, field: "dateTimeInsertion")
}
```


## Resources

[Another project about Airadne](https://github.com/CarlosAMolina/microservice-apis-python)

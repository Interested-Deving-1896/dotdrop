# Variables entry

The optional **variables** entry contains a variables mapping (See [variables](config-file.md#variables)).

```yaml
variables:
  <variable-name>: <variable-content>
```

Variables defined in the `variables` entry are made available
within the config file and to the [templates](../template/templating.md).

For example
```yaml
variables:
  myvar: "some value"
  home: "{{@@ env['HOME'] @@}}"
  email: "user@domain.com"
```

Config variables are recursively evaluated, which means that
a config like the below:
```yaml
variables:
  var1: "var1"
  var2: "{{@@ var1 @@}} var2"
  var3: "{{@@ var2 @@}} var3"
  var4: "{{@@ dvar4 @@}}"
dynvariables:
  dvar1: "echo dvar1"
  dvar2: "{{@@ dvar1 @@}} dvar2"
  dvar3: "{{@@ dvar2 @@}} dvar3"
  dvar4: "echo {{@@ var3 @@}}"
```

will result in the following available variables:

* var1: `var1`
* var2: `var1 var2`
* var3: `var1 var2 var3`
* var4: `echo var1 var2 var3`
* dvar1: `dvar1`
* dvar2: `dvar1 dvar2`
* dvar3: `dvar1 dvar2 dvar3`
* dvar4: `var1 var2 var3`

Config variables can be nested as shown below:
```yaml
variables:
  rofi:
    background_color: "rgba ( 33, 33, 33, 100 % );"
  polybar:
    background_color: "#cc222222"
```

Where the above would be referenced using `{{@@ rofi.background_color @@}}`
and `{{@@ polybar.background_color @@}}`.

## Variables precedence

* `dynvariables` > `variables`
* Profile `(dyn)variables` > any other `(dyn)variables`
* Profile `(dyn)variables` > profile's included `(dyn)variables`
* Imported `(dyn)variables` > `(dyn)variables` (except for `import_configs`)

When including profiles with `include`, the value of a variable present in multiple
included profiles will come from the last profile graph in the order of the include list.

In the below example, the variable value is `1`:
```yaml
  top:
    variables:
      foo: 1
    include:
      - left
      - right
  left:
    variables:
      foo: 2
  right:
    variables:
      foo: 3
    include:
      - bottom
  bottom:
    variables:
      foo: 4
```

In this example, its value is `4`
```yaml
  top:
    include:
      - left
      - right
  left:
    variables:
      foo: 2
  right:
    include:
      - bottom
  bottom:
    variables:
      foo: 4
```

See also [CONTRIBUTING doc](/CONTRIBUTING.md)

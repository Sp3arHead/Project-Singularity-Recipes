# Recipe schema

A recipe is a YAML document that describes safe, declarative setup tasks for a Project Singularity server. Each recipe must contain the following top-level fields:

- `name` (required): The display name of the recipe.
- `version` (required): The recipe format version selected by its author.
- `author`: The person or organization that maintains the recipe.
- `description`: A short description of what the recipe provides.
- `requiresLicense`: Whether a valid Project Singularity license is required. The default is `true`.
- `optionalPackages`: An optional list of packages that can be enabled by the server owner.
- `tasks` (required): The ordered list of actions performed by the recipe.

Each entry in `optionalPackages` may contain:

- `id`: The stable identifier of the optional package.
- `name`: The display name of the optional package.
- `description`: A description of the optional package.
- `defaultEnabled`: Whether the package is enabled by default.
- `tasks`: The ordered list of actions for the optional package.

## Allowed actions

A recipe may use only these action types and fields:

- `download_github` with `repo`, `ref`, `subpath`, and `dest`.
- `download_file` with `url` and `dest`.
- `unzip` with `src` and `dest`.
- `move_path` with `src` and `dest`.
- `remove_path` with `path`.
- `write_file` with `path` and `content`.
- `append_to_cfg` with `content`.
- `connect_database` with no parameters.
- `query_database` with either `file` or `sql`.
- `waste_time` with `seconds`, which may be at most 30.

There is no action that runs shell commands, by design.

## Limits and safety requirements

- A recipe file is at most 256 KB.
- There are at most 100 steps including optional packages.
- Each downloaded file is at most 1 GB.
- Each SQL file is at most 50 MB.
- A run takes at most 1800 seconds.
- All URLs must use HTTPS.
- All target paths must stay inside the server data folder.

## Complete example recipe

The following is an example only. It does not install a real package or reference a real external project.

```yaml
name: Example Recipe
version: 1
author: Example Author
description: A three-step example recipe for documentation.
requiresLicense: false
optionalPackages: []
tasks:
  - action: download_file
    url: https://example.com/example-package.zip
    dest: downloads/example-package.zip
  - action: unzip
    src: downloads/example-package.zip
    dest: resources/example-package
  - action: write_file
    path: resources/example-package/example.cfg
    content: "# Example configuration\n"
```

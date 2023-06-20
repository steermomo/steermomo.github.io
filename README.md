# i.steer.space

![GitHub Action Automatic Build](https://github.com/steermomo/steermomo.github.io/workflows/Python%20application/badge.svg?branch=origin)

| desc | command |
| --- | --- |
| install poetry up| poetry self add poetry-plugin-up |
| update each package to latest version |poetry show -o \| awk '{print $1}' \| xargs poetry update |



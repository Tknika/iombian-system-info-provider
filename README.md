# IoMBian Display Handler

This service publishes the following system information through a ZeroMQ socket (port 5557 by default):

- Hostname
- Time and uptime
- Storage (used, total and percent)
- Local network connection status (ip address for each interface)
- Internet connection status


## Installation

- Clone the repo into a temp folder:

> ```git clone https://github.com/Tknika/iombian-system-info-provider.git /tmp/iombian-system-info-provider && cd /tmp/iombian-system-info-provider```

- Create the installation folder and move the appropiate files (edit the user):

> ```sudo mkdir /opt/iombian-system-info-provider```

> ```sudo cp requirements.txt /opt/iombian-system-info-provider```

> ```sudo cp -r src/* /opt/iombian-system-info-provider```

> ```sudo cp systemd/iombian-system-info-provider.service /etc/systemd/system/```

> ```sudo chown -R iompi:iompi /opt/iombian-system-info-provider```

- Create the virtual environment and install the dependencies:

> ```cd /opt/iombian-system-info-provider```

> ```python3 -m venv venv```

> ```source venv/bin/activate```

> ```pip install --upgrade pip```

> ```pip install -r requirements.txt```

- Start the script

> ```sudo systemctl enable iombian-system-info-provider.service && sudo systemctl start iombian-system-info-provider.service```

## Author

(c) 2021 [Aitor Iturrioz Rodríguez](https://github.com/bodiroga)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
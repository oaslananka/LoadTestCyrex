# LoadTestCyrex Documentation

Welcome to the LoadTestCyrex project documentation. This documentation provides information on how to set up, use, and contribute to the project.

## Table of Contents

1. [Overview](#overview)
2. [Setup](#setup)
3. [Running Tests](#running-tests)
4. [Docker Setup](#docker-setup)
5. [Playground Scripts](#playground-scripts)
6. [Contributing](#contributing)
7. [License](#license)

## Overview

LoadTestCyrex is a performance testing tool for gRPC services using Locust. It provides various client scripts and configurations for testing authentication, vacancy creation, and other operations through gRPC.

## Setup

### Cloning the Repository

```sh {"id":"01J0BBEEYTXCNTAEDT4S6CXYCQ"}
git clone https://github.com/oaslananka/LoadTestCyrex.git
cd LoadTestCyrex
```

### Creating and Activating a Virtual Environment

```sh {"id":"01J0BBEEYTXCNTAEDT4TG4KHXB"}
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Installing the Required Packages

```sh {"id":"01J0BBEEYTXCNTAEDT4WJ4FF84"}
pip install -r requirements.txt
```

### Setting Up Environment Variables

Create a `.env` file in the root directory and add the following:

```ini {"id":"01J0BBEEYTXCNTAEDT4YNVX2XX"}
TestUser_1_Email=user1@example.com
TestUser_1_Password=pass1
TestUser_2_Email=user2@example.com
TestUser_2_Password=pass2
TestUser_3_Email=user3@example.com
TestUser_3_Password=pass3
```

### Compiling the `.proto` Files

```sh {"id":"01J0BBEEYTXCNTAEDT520Q2NTN"}
python generate_protos.py
```

## Running Tests

To run the performance tests using Locust, use the following command:

```sh {"id":"01J0BBEEYTXCNTAEDT53SYSJWR"}
locust -f src/main.py --config config/task.config
```

## Docker Setup

### Building and Running the Docker Container

Ensure Docker is installed on your system. Then, build the Docker image and start the container:

```sh {"id":"01J0BBEEYTXCNTAEDT53V6E6MD"}
docker-compose build
docker-compose up
```

### Accessing the Locust Web Interface

Open your browser and navigate to [http://localhost:8089](http://localhost:8089).

## Playground Scripts

The `playgrounds` directory contains various scripts for testing and experimenting with the LoadTestCyrex project. Each script is well-documented and can be run individually to test different functionalities of the project.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

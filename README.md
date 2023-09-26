# BenefitCostRatioCalc
 Benefit Cost Ratio Calculator App
 [![Build and Archive Workflow](https://github.com/AvinashMahala/BenefitCostRatioCalc/actions/workflows/build.yml/badge.svg)](https://github.com/AvinashMahala/BenefitCostRatioCalc/actions/workflows/build.yml)

🛠 Backend: Python, Tkinter, SQLite, Git, Pip

🎨 Frontend: Tkinter (GUI Library)

🧰 Dev & Deploy: Python 3.x, Git, Pip

💌 Database: SQLite

📦 Dependency Management: Pip

Certainly, here's a more comprehensive README for your Benefit Cost Ratio (BCR) Calculator application:

# Benefit Cost Ratio (BCR) Calculator Application

The Benefit Cost Ratio (BCR) Calculator Application is a user-friendly tool for estimating the benefit-to-cost ratio of bridge construction and maintenance projects. This README provides an overview of the application, its features, and how to use it effectively.

## Table of Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
- [Using the Application](#using-the-application)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The BCR Calculator Application is designed to assist engineers and project managers in evaluating the economic feasibility of bridge-related projects. It provides a user-friendly graphical interface for entering project data, calculating maintenance costs, and estimating the BCR, a critical metric for decision-making in infrastructure projects.

## Key Features

### 1. Tab-Based User Interface

The application features a tab-based user interface that organizes information and calculations into distinct sections, making it easy to navigate and manage project data.

- **Homepage**: Provides an overview and serves as the main entry point.
- **Deck, Steel, SubStructure, and SuperStructure Tabs**: Allows for detailed data entry and cost calculations for different project components.
- **Final Result**: Displays the final project cost and BCR calculation results.

### 2. Database Integration

The application integrates with a database for storing and retrieving project-specific data. This ensures data consistency and facilitates historical data analysis.

### 3. Comprehensive Data Entry

- Enter bridge-specific data, such as bridge ID, UUID, ADT (Average Daily Traffic), Detour Length (mi), and ADT_TRk.
- Input costs for various project elements, including deck, steel, substructure, and superstructure.
- Calculate maintenance costs and BCR based on user inputs.

### 4. Error Handling

The application includes error-handling mechanisms to ensure that mandatory data fields are provided before performing calculations. Users receive informative error messages when essential data is missing.

## Getting Started

Follow these steps to get started with the BCR Calculator Application:

1. **Clone the Repository**: Begin by cloning this repository to your local machine:

   ```shell
   https://github.com/AvinashMahala/BenefitCostRatioCalc.git
   ```

2. **Install Dependencies**: Install the required dependencies by running the following command:

   ```shell
   pip install -r requirements.txt
   ```

3. **Database Configuration**: Ensure that your database configuration is set correctly. Modify the database connection details as needed in the application.

4. **Run the Application**: Start the application by running the `main.py` script:

   ```shell
   python main.py
   ```

   This will launch the BCR Calculator Application.

## Using the Application

### Data Entry

1. **Homepage**: Enter the bridge ID and UUID to access project-specific data.

2. **Deck, Steel, SubStructure, and SuperStructure Tabs**: Input costs and project data for different bridge elements.

3. **Final Result**: View the final project cost and BCR calculation results.

### Error Handling

- The application will display error messages if mandatory data fields are missing or if there are issues with data input.

### Database Integration

- The application integrates with a database for data storage and retrieval. Ensure that your database is correctly configured and accessible.

## Technical Details

The BCR Calculator Application is built using the following technologies:

- **Python**: The core programming language used for development.
- **Tkinter**: A Python library for building graphical user interfaces (GUI).
- **SQLite**: A lightweight, built-in database used for data storage and retrieval.

## Contributing

Contributions to this project are welcome. If you would like to contribute to the development or improvement of the BCR Calculator Application, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Add feature'`.
4. Push to your forked repository: `git push origin feature-name`.
5. Create a pull request describing your changes.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use and modify the code for your own purposes.

# Rainfall & Water Resource Monitoring System

A Python-based desktop application for monitoring and managing rainfall and water resource data with separate interfaces for administrators and clients.

## Features

- **User Authentication System**
  - Separate login portals for administrators and clients
  - Secure password handling with visibility toggle
  - Role-based access control

- **Administrator Dashboard**
  - Manage user accounts
  - Access and modify rainfall data
  - Monitor water resources
  - Administrative controls and data management

- **Client Portal**
  - View rainfall statistics
  - Access water resource information
  - User-friendly interface

## Project Structure

```
├── admin_page.py         # Administrator dashboard implementation
├── client_page.py        # Client portal implementation
├── fetch_json_data.py    # Data retrieval utilities
├── home_page.py         # Home page implementation
├── main.py              # Main application entry point
├── rain_data_page.py    # Rainfall data management
├── search_query.py      # Search functionality
├── water_data_page.py   # Water resource data management
└── server/              # Data storage directory
    ├── groundwater.json    # Groundwater data
    ├── rain_test.json     # Test rainfall data
    ├── rainfall_data.json # Main rainfall data
    ├── users.json         # User authentication data
    └── water_data.json    # Water resource data
```

## Requirements

- Python 3.x
- Tkinter (included in standard Python installation)
- JSON (included in standard Python installation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AshmitSenapati/python-project.git
```

2. Navigate to the project directory:
```bash
cd python-project
```

## Usage

1. Run the main application:
```bash
python main.py
```

2. Select your role (Administrator or Client)
3. Log in with your credentials
4. Navigate through the interface to access the desired functionality

## System Features

### Administrator Features
- User account management
- Data manipulation and updates
- System monitoring and control
- Access to all data repositories

### Client Features
- View rainfall statistics
- Access water resource data
- Search functionality
- User-friendly data visualization

## Data Storage

The application uses JSON files for data storage:
- `users.json`: User authentication and role information
- `rainfall_data.json`: Comprehensive rainfall statistics
- `water_data.json`: Water resource information
- `groundwater.json`: Groundwater level data
- `rain_test.json`: Test data for rainfall measurements

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Author

Ashmit Senapati - 25BCE2451
Manit Bisht - 25BCE2441
Pranay.R Jangra - 25BCE2433
Anushka Gupta - 25BCE2434
Nikhil Sagar - 25BCE2446

---
For more information or support, please open an issue in the repository.
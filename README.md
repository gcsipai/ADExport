ADExport - Active Directory Export Tool
https://img.shields.io/badge/Python-3.8+-blue.svg
https://img.shields.io/badge/License-MIT-green.svg
https://img.shields.io/badge/Version-Beta%25201.1-orange.svg

A modern, user-friendly graphical application for exporting Active Directory data to CSV files with multi-language support and dark/light themes.

🌟 Features
🔌 Connection Management
Automatic DC Detection - Local Domain Controller auto-discovery

Flexible Connectivity - Remote and local AD connections

SSL/TLS Support - Secure encrypted connections

Multiple Port Support - Standard (389) and SSL (636) ports

📊 Data Export Capabilities
Users & Organizational Units - Complete user and OU structure export

Groups & Members - Group information with member lists

User Status Filtering - Filter by enabled/disabled/all users

Comprehensive Attributes - Export all essential AD attributes

🎨 User Experience
Multi-language Support - Hungarian and English interfaces

Dark/Light Themes - System-aware theme switching

Modern GUI - Built with CustomTkinter for sleek appearance

Real-time Status - Live progress and status updates

💾 Output Features
CSV Format - Standardized semicolon-delimited files

UTF-8 Encoding - Full international character support

Custom Filenames - User-defined export file names

Structured Data - Well-organized, readable output

📥 Installation
Prerequisites
Python 3.8 or higher

Active Directory environment access

Read permissions in AD

Dependencies
bash
pip install customtkinter ldap3
Quick Start

DC IP/Hostname

Port (389 for standard, 636 for SSL)

Base DN (automatically detected for local DC)

Bind DN with read permissions

Password

Select Export Options:

☑️ Users/OUs - Export users and organizational units

☑️ Groups/Members - Export groups with their members

🔽 User Status Filter - Choose between All, Enabled, or Disabled users

Start Export:

Click "Start Export"

Choose save location for CSV files

Review exported data

Advanced Features
SSL/TLS Encryption: Enable for secure connections

Automatic Detection: Local DC and Base DN auto-discovery

Language Switching: Toggle between Hungarian and English

Theme Selection: Switch between dark and light modes

🗂️ Export Structure
Users and OUs CSV
Column	Description	Example
ObjektumTípus	Object type (User/OU)	Felhasználó
Állapot	Account status	Engedélyezett
Név	Full name	John Smith
Felhasználónév	sAMAccountName	jsmith
Keresztnév	Given name	John
Vezetéknév	Surname	Smith
Email	Email address	jsmith@company.com
Mobil	Mobile number	+123456789
Leírás	Description	IT Department
DN	Distinguished Name	CN=John Smith,OU=Users,DC=company,DC=com
Groups CSV
Column	Description	Example
Név	Group display name	Administrators
Csoportnév	sAMAccountName	Domain Admins
Leírás	Group description	Full administrative access
DN	Distinguished Name	CN=Domain Admins,OU=Groups,DC=company,DC=com
Tagok DN-jei	Member DNs	CN=John Smith,OU=Users,DC=company,DC=com; CN=Jane Doe,OU=Users,DC=company,DC=com
🔧 Configuration
Supported LDAP Attributes
Users: sAMAccountName, cn, givenName, sn, mail, distinguishedName, description, mobile, userAccountControl

Groups: cn, sAMAccountName, description, distinguishedName, member

OUs: distinguishedName, ou

Filter Options
All Users: Export all user accounts

Enabled Only: Active user accounts

Disabled Only: Inactive user accounts

🎯 Use Cases
🏢 System Administration
User inventory management

Account status auditing

Organizational structure documentation

🔒 Security & Compliance
Access right reviews

Security group analysis

Compliance reporting

Audit preparation

📈 HR & Management
Employee directory generation

Department structure analysis

Onboarding/offboarding tracking

🔄 Migration & Integration
System migration preparation

Data synchronization

External system integration

🌍 Multi-language Support
Hungarian (Magyar)
Complete Hungarian interface

Localized status messages

Hungarian CSV headers

English
Full English localization

International standards

English CSV headers

🛠️ Technical Details
Built With
Python 3 - Core programming language

CustomTkinter - Modern GUI framework

LDAP3 - Active Directory communication

SSL/TLS - Secure connection handling

LDAP Queries
python
# User filter
BASE_USER_FILTER = '(&(objectClass=user)(!(objectClass=computer)))'

# OU filter  
OU_FILTER = '(objectClass=organizationalUnit)'

# Group filter
GROUP_FILTER = '(objectClass=group)'
📋 System Requirements
Operating System: Windows 10/11, Windows Server 2012+

Python: Version 3.8 or higher

Permissions: Read access to Active Directory

Network: Connectivity to Domain Controller

🤝 Contributing
We welcome contributions! Please feel free to submit pull requests, report bugs, or suggest new features.

Development Setup
Fork the repository

Create a feature branch

Make your changes

Test thoroughly

Submit a pull request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

⚠️ Disclaimer
This tool is designed for authorized administrative use only. Ensure you have proper permissions before exporting Active Directory data. The developers are not responsible for any misuse or damage caused by this application.

🆘 Support
For issues and questions:

Check the existing GitHub issues

Create a new issue with detailed description

Include error messages and steps to reproduce

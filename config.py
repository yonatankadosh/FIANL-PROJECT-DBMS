"""
Database configuration file.

IMPORTANT: To connect to mysqlsrv1.cs.tau.ac.il, you need to:
1. Set up an SSH tunnel, OR
2. Connect via the university VPN

If using SSH tunnel, run this command first:
ssh -L 3305:mysqlsrv1.cs.tau.ac.il:3306 namirbarr@nova.cs.tau.ac.il

Then use 'localhost' as the host below.
"""

# MySQL Database Configuration
# If using SSH tunnel, use 'localhost' as host, otherwise use 'mysqlsrv1.cs.tau.ac.il'
DB_CONFIG = {
    'host': 'localhost',  # Use 'localhost' if using SSH tunnel, 'mysqlsrv1.cs.tau.ac.il' otherwise
    'port': '3305',  # Local port if using SSH tunnel, or 3306 for direct connection
    'user': 'namirbarr',  # MySQL username
    'database': 'namirbarr',  # MySQL database name
    'password': 'namirbarr'  # MySQL password
}


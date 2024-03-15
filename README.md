# sql_server_test
## SSRS (Reporting Services)

### Installation
- Install visual studio
- Install microsft SQL server
- Install SQL server management studioa
- Install SSRS
- Install power BI
- Install SQL server data tools (SSDT): https://learn.microsoft.com/en-us/sql/ssdt/download-sql-server-data-tools-ssdt?view=sql-server-ver16
- You need to go into visual studio code, manage extensions, search SSDT and download the 3 from microsoft.

### Setting up a report

on the SSRS website hosted locally at http://ivan-dtsquad/Reports/browse/, the connection string will be something like this: Data Source=localhost\SQLEXPRESS; Initial Catalog=test_db
When I connect, I can create a report by pressing new -> report, which opens the report builder.
After finishing a report, you can view it on the report server at http://ivan-dtsquad/ReportServer
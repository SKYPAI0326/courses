/*
  SQL Server training lab: read-only instance inventory
  Run only after connecting to the intended training instance.
  This script does not create, update, or delete database objects or rows.
*/

SELECT
    SERVERPROPERTY('ProductVersion') AS ProductVersion,
    SERVERPROPERTY('ProductLevel') AS ProductLevel,
    SERVERPROPERTY('Edition') AS Edition,
    SERVERPROPERTY('EngineEdition') AS EngineEdition;
GO

SELECT
    DB_NAME() AS CurrentDatabase;
GO

SELECT
    state_desc AS DatabaseState,
    COUNT_BIG(*) AS VisibleDatabaseCount
FROM sys.databases
GROUP BY state_desc
ORDER BY state_desc;
GO

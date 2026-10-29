/*
  SQL Server training lab: inspect key constraints in Microsoft's AdventureWorks sample.
  Prerequisite: connect to the instance and select the matching AdventureWorks sample database.
  Read-only: these statements do not create, update, or delete data or objects.
*/

SELECT
    DB_NAME() AS CurrentDatabase,
    OBJECT_ID(N'Purchasing.ProductVendor', N'U') AS ProductVendorObjectId;
GO

SELECT
    tc.CONSTRAINT_NAME,
    tc.CONSTRAINT_TYPE,
    kcu.COLUMN_NAME,
    kcu.ORDINAL_POSITION
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
LEFT JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS kcu
    ON  tc.CONSTRAINT_CATALOG = kcu.CONSTRAINT_CATALOG
    AND tc.CONSTRAINT_SCHEMA = kcu.CONSTRAINT_SCHEMA
    AND tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
    AND tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
    AND tc.TABLE_NAME = kcu.TABLE_NAME
WHERE tc.TABLE_SCHEMA = N'Purchasing'
  AND tc.TABLE_NAME = N'ProductVendor'
  AND tc.CONSTRAINT_TYPE IN (N'PRIMARY KEY', N'FOREIGN KEY')
ORDER BY
    tc.CONSTRAINT_TYPE,
    tc.CONSTRAINT_NAME,
    kcu.ORDINAL_POSITION;
GO

SELECT
    ProductID,
    VendorID,
    COUNT_BIG(*) AS PairCount
FROM Purchasing.ProductVendor
GROUP BY ProductID, VendorID
HAVING COUNT_BIG(*) > 1;
GO

# SQL Server Instructor Resources

## Knowledge

- [Database Engine instances](https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/database-engine-instances-sql-server?view=sql-server-ver16) — 說明執行個體如何接收連線與管理資料庫；第一課使用。
- [SERVERPROPERTY](https://learn.microsoft.com/en-us/sql/t-sql/functions/serverproperty-transact-sql) — 讀取當前實例的版本、Edition 與引擎類型；環境盤點 Lab 使用。
- [sys.databases](https://learn.microsoft.com/en-us/sql/relational-databases/system-catalog-views/sys-databases-transact-sql?view=sql-server-ver17) — 查閱可見資料庫的狀態與設定；用於辨認目前伺服器狀態，並注意 metadata visibility 權限限制。
- [Databases](https://learn.microsoft.com/en-us/sql/relational-databases/databases/databases?view=sql-server-ver16) — 說明資料庫、結構描述與資料表的層級；用於架構名詞教學。
- [Tables](https://learn.microsoft.com/en-us/sql/relational-databases/tables/tables) — 說明資料列、欄及資料完整性；用於資料表設計。
- [Primary and foreign key constraints](https://learn.microsoft.com/en-us/sql/relational-databases/tables/primary-and-foreign-key-constraints?view=sql-server-ver16) — 主鍵、外鍵及參照完整性；用於關聯模型實作。
- [System information schema views](https://learn.microsoft.com/en-us/sql/relational-databases/system-information-schema-views/system-information-schema-views-transact-sql?view=sql-server-ver17) — 說明 `INFORMATION_SCHEMA` 中繼資料查詢與可見性限制；AdventureWorks 鍵值盤點 Lab 使用。
- [KEY_COLUMN_USAGE](https://learn.microsoft.com/en-us/sql/relational-databases/system-information-schema-views/key-column-usage-transact-sql?view=sql-server-ver17) — 查詢目前資料庫中可見的鍵約束欄位及順序；用於確認複合鍵。
- [CREATE DATABASE](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-database-transact-sql?view=sql-server-ver16) — 建立資料庫的語法、檔案及限制；用於 DDL 實作。
- [SQL Server 2025 hardware and software requirements](https://learn.microsoft.com/en-us/sql/sql-server/install/hardware-and-software-requirements-for-installing-sql-server-2025?view=sql-server-ver17) — 核對 Windows 安裝需求與處理器架構。
- [SQL Server on Linux installation guidance](https://learn.microsoft.com/en-us/sql/linux/install-upgrade/setup) — 核對支援平台、x64 限制及容器支援條件。
- [SQL Server editions and features](https://learn.microsoft.com/en-us/sql/sql-server/editions-and-components-of-sql-server-2025?view=sql-server-ver17) — 比較版本與可用功能，避免混淆版本差異。
- [AdventureWorks sample databases](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver17) — 取得 Microsoft 官方 OLTP／DW 範例資料庫；它是範例資料，不是生產事故證據。
- [SQL Server Agent overview](https://learn.microsoft.com/en-us/ssms/agent/sql-server-agent?view=sql-server-ver17) — 工作、排程、警示及權限；用於作業自動化單元。
- [Azure SQL feature comparison](https://learn.microsoft.com/en-us/azure/azure-sql/database/features-comparison?view=azuresql) — 核對 SQL Server、Azure SQL Database 與 Managed Instance 的功能差異。
- [Automate management tasks in Azure SQL](https://learn.microsoft.com/en-us/azure/azure-sql/database/job-automation-overview?view=azuresql) — 核對不同 Azure SQL 產品的排程與 SQL Agent 能力。
- [BigQuery overview](https://docs.cloud.google.com/bigquery/docs/introduction) — 說明 BigQuery 的託管分析服務、儲存與運算分層；用於雲端倉儲定位。
- [Load data into BigQuery](https://docs.cloud.google.com/bigquery/docs/loading-data) — 比較批次載入、串流、CDC 與外部資料查詢；用於 ETL／ELT 單元。
- [Snowflake architecture](https://docs.snowflake.com/en/user-guide/intro-key-concepts) — 說明儲存、運算、雲端服務層及資料載入選項；用於跨平台比較。
- [Snowflake data loading overview](https://docs.snowflake.com/en/user-guide/data-load-overview) — 說明 COPY 批次載入與 Snowpipe 持續載入；用於管線模式比較。
- [Azure SQL Database overview](https://learn.microsoft.com/en-us/azure/azure-sql/database/sql-database-paas-overview?view=azuresql) — 說明它是受管理的關聯式 PaaS 資料庫及平台代管維護邊界。
- [Microsoft Fabric Data Warehouse](https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing) — Azure 生態系中的雲端倉儲範例；用於和 Azure SQL Database 區分。

## Wisdom

尚未安排真人 DBA／講師社群或真人學員回饋。真人試教對象待確認；AI 角色扮演不會代替此項驗收。

## Gaps

- 尚未確認有可用的 x64 SQL Server 實驗主機。使用者回報另有 ASUS G14、AMD CPU 與 NVIDIA 獨立顯卡；Windows／Linux 版本、CPU 型號、記憶體、磁碟空間及 SQL Server 安裝狀態待查。
- 尚無本人可合法使用的真實事故紀錄。可用官方範例資料及明確標示的受控實驗；不可據此宣稱有生產事故經驗。
- Cloud Data 實作平台、帳號權限及可能費用未決；確認後再選 BigQuery、Snowflake 或 Azure 方案。
- 使用者提供的 Azure SQL 例子需在課程中精確分類：Azure SQL Database 是雲端關聯式資料庫服務；講雲端資料倉儲時另以 Fabric Warehouse 或 Synapse 等適當產品說明，不混為同一類。

## Environment check (2026-10-02)

- 本機 `uname -m` 回報 `arm64`；本次 PATH 檢查未找到 `docker`、`sqlcmd` 或 `sqlservr`。這不代表電腦上完全沒有其他未加入 PATH 的圖形工具。
- 使用者回報另持有 AMD CPU、NVIDIA 獨顯的 ASUS G14 筆電；此為使用者陳述，尚未檢查該筆電的作業系統與 SQL Server 可用狀態。
- Microsoft 文件指出 SQL Server Linux 容器僅支援 x86-64 主機；ARM 翻譯／模擬未經支援。實機操作需另確認 x64 主機或伺服器。
- Microsoft 文件指出 Azure SQL Database 不提供 SQL Server Agent；Azure SQL Managed Instance 支援大部分但非全部 Agent 功能。

# Task 2: Exploratory Data Analysis (EDA) and Business Intelligence

For this task I used the **classicmodels** sample database from mysqltutorial.org. It is the data of a company that sells scale model cars and it has 8 related tables (customers, orders, orderdetails, products, productlines, payments, employees, offices). I picked it because Step 2 asks for multi-table joins, and this database is already split into proper tables. ApexPlanet did not give a list of business questions, so I wrote 7 of my own.

**Tools used:** MySQL Workbench, Python (pandas, matplotlib, seaborn), PowerPoint

## What is in this folder

| File / folder | What it is |
|---|---|
| `task2_sql_queries.sql` | the 7 SQL queries for Step 2 |
| `sql_results/` | one screenshot of the output for each query (Q1 to Q7). Q2 has 27 rows so it is split into two images |
| `task2_eda.py` | Python script for Step 1 and Step 3 (reads the tables straight from MySQL) |
| `charts/` | the 10 charts that the script saves |
| `Dashboard_Mockup.pptx` | the dashboard mock-up for Step 4 |

---

## Step 1: Descriptive statistics and univariate analysis

I loaded the tables from MySQL into pandas and used `describe()` and `value_counts()` to get the summary numbers.

**Numerical columns**

| Column | Mean | Median | Min | Max |
|---|---|---|---|---|
| priceEach | 90.77 | 85.81 | 26.55 | 214.30 |
| quantityOrdered | 35.22 | 35 | 6 | 97 |
| buyPrice | 54.40 | 53.92 | 15.91 | 103.42 |
| MSRP | 100.44 | 98.30 | 33.19 | 214.30 |
| quantityInStock | 5,046.65 | 5,437.50 | 15 | 9,997 |
| payment amount | 32,431.65 | 32,077.44 | 615.45 | 120,166.58 |
| creditLimit | 67,659.02 | 76,700 | 0 | 227,600 |

What I noticed:
- The average price per item (90.77) is a little higher than the median (85.81), so a few expensive models pull the average up.
- Quantity per order line is quite steady. The mean and the median are both about 35 and most lines are between 27 and 43 units.
- The biggest payment (about 120,167) is far above the typical payment (about 32,000), so there are a few very large payments.
- Some customers have a credit limit of 0, which is why the mean credit limit (67,659) is lower than the median (76,700).
- MSRP is about double the buy price on average (100.44 against 54.40).

**Categorical columns**

- **Order status** (326 orders): Shipped 303, Cancelled 6, In Process 6, Resolved 4, On Hold 4, Disputed 3. About 93% of the orders are shipped.
- **Product line** (110 products): Classic Cars 38, Vintage Cars 24, Motorcycles 13, Planes 12, Trucks and Buses 11, Ships 9, Trains 3.
- **Customer country** (122 customers): USA 36, Germany 13, France 12, Spain 7, Australia 5, UK 5, then Italy, New Zealand, Singapore and Finland with 3 or 4 each.

**Charts for this step** (in `charts/`): `01_priceEach_histogram.png`, `02_quantityOrdered_histogram.png`, `03_payment_amount_histogram.png` (histograms) and `04_order_status_bar.png`, `05_product_line_bar.png`, `06_top_countries_bar.png` (bar charts).

---

## Step 2: SQL for business questions

Revenue in all these queries is `quantityOrdered x priceEach`, and cancelled orders are left out. The queries use filtering (`WHERE`), aggregation (`SUM`, `COUNT`, `GROUP BY`) and joins of 2 to 4 tables.

| # | Business question | What I found |
|---|---|---|
| 1 | What are the top 5 products by revenue? | The 1992 Ferrari 360 Spider red is first with about 271,015 revenue (1,768 units). Next are the 1952 Alpine Renault 1300 (190,018), the 2001 Ferrari Enzo (182,440), the 2003 Harley-Davidson Eagle Drag Bike (170,686) and the 1968 Ford Mustang (157,749). Four of the five are cars. |
| 2 | What is the monthly trend of orders and revenue? | November is the biggest month in both years: 965,062 from 29 orders in 2003-11 and 979,292 from 33 orders in 2004-11. October is also high. Other months are mostly between 120,000 and 440,000. Revenue is growing: 2003 was about 3.25M and 2004 about 4.34M (up about 34%). The data stops at 2005-05, and January to May 2005 (about 1.77M) is about 48% higher than January to May 2004 (about 1.19M). |
| 3 | Which product lines bring the most revenue? | Classic Cars is first with about 3.77M (34,923 units), about 40% of all revenue. Vintage Cars is second with about 1.76M. Together they are about 59% of revenue. Trains is the smallest with about 179,000. Trucks and Buses (1.02M) earn more than Planes (0.90M) from slightly fewer units, so trucks sell at a higher price per unit. |
| 4 | Who are the top 10 customers by total payments? | Euro+ Shopping Channel (Spain) paid the most, about 715,739, followed by Mini Gifts Distributors Ltd. (USA) with about 584,188. The third customer, Australian Collectors, Co., is far behind at about 180,585. The 10th customer paid about 130,305. |
| 5 | Which 5 countries bring the most revenue? | The USA is far ahead with about 3.23M from 111 orders, which is about 35% of all revenue. Then Spain (1.05M), France (1.01M), Australia (0.56M) and New Zealand (0.42M). |
| 6 | Which 5 sales reps bring the most revenue? | Gerard Hernandez is first with about 1.21M from 7 customers, then Leslie Jennings with about 1.08M. Pamela Castillo handles the most customers (10) but is third with about 868,000. |
| 7 | How many orders were shipped late each year? | Very few. Only 1 order out of 312 shipped orders was late, in 2003 (0.9% of that year). 2004 and 2005 had none. |

The screenshots of all the outputs are in `sql_results/`.

---

## Step 3: Multivariate analysis and correlation

For this step I joined `orderdetails` with `products`, so every row is one item in an order. I made two scatter plots, a correlation heatmap and a pair plot (`07_scatter_buyPrice_MSRP.png`, `08_scatter_priceEach_quantity.png`, `09_heatmap.png`, `10_pairplot.png`).

Correlation values from the heatmap:

| Pair | Correlation |
|---|---|
| priceEach and MSRP | 0.98 |
| buyPrice and MSRP | 0.92 |
| priceEach and buyPrice | 0.90 |
| quantityOrdered and the other columns | 0.02 to 0.03 |
| quantityInStock and the other columns | 0.02 to 0.06 |

What I understood from this:
- Price, buy price and MSRP move together very strongly. This makes sense because the price on an order is close to the MSRP, and the MSRP is set as a markup on the buy price.
- Quantity ordered has almost no relation with anything else. Customers do not order smaller or larger quantities because an item is cheaper or more expensive.
- Stock quantity also has no real relation with price or quantity ordered.

---

## Step 4: Dashboard mock-up

The mock-up is in `Dashboard_Mockup.pptx`. It has 6 KPI tiles, a monthly revenue line chart (from Q2) and a revenue by product line bar chart (from Q3).

| KPI | Value | Why I picked it |
|---|---|---|
| Total revenue | about $9.37M | shows how big the business is |
| Total orders | 320 | order volume (cancelled orders left out) |
| Average order value | about $29,267 | how much one order is worth |
| Total customers | 122 | size of the customer base |
| Late shipments | 0.3% | shows whether delivery promises are kept |
| Units sold | 102,882 | sales volume |

---

## Notes

- Total revenue is 9,365,336.43. I got the same number by adding the monthly revenue in Q2 and by adding the product lines in Q3.
- The orders in the database run from January 2003 to May 2005, so 2005 is only a partial year.
- Q4 uses the `payments` table, so it shows what customers actually paid and it will not match the revenue numbers exactly.

## How to run

1. Load `mysqlsampledatabase.sql` (from mysqltutorial.org) into MySQL. It creates the `classicmodels` database.
2. Run the queries in `task2_sql_queries.sql` one by one in MySQL Workbench.
3. Install the packages with `pip install pandas matplotlib seaborn sqlalchemy pymysql cryptography`.
4. Run `python task2_eda.py`. It asks for the MySQL password and saves the charts in a `charts` folder.

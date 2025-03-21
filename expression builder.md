# Azure Data Factory (ADF) Expression Builder - Employee Table Examples

## Employee Table Schema
| EmployeeID | Name    | Age | Department | Salary  | JoiningDate  |
|-----------|--------|----|------------|--------|-------------|
| 101       | Alice  | 30 | HR         | 50000  | 2020-01-15  |
| 102       | Bob    | 40 | IT         | 70000  | 2018-06-23  |
| 103       | Charlie| 28 | Finance    | 60000  | 2021-09-30  |
| 104       | David  | 35 | IT         | 75000  | 2017-11-12  |
| 105       | Eve    | 27 | HR         | 55000  | 2022-02-01  |

---

## 1. String Functions (Employee Name & Department)

```adf
toUpper(Name)                          -- Convert employee name to uppercase
toLower(Department)                    -- Convert department name to lowercase
length(Name)                            -- Get length of employee name
concat(Name, ' - ', Department)         -- Concatenate name and department
replace(Department, 'HR', 'Human Resources') -- Replace 'HR' with full form
substring(Name, 0, 3)                   -- Extract first 3 letters of name
startsWith(Name, 'A')                   -- Check if name starts with 'A'
endsWith(Name, 'e')                     -- Check if name ends with 'e'
indexOf(Name, 'a')                      -- Find position of letter 'a' in name
trim(Name)                              -- Trim spaces from employee name
contains(Name, 'Bob')                   -- Check if name contains 'Bob'


add(Salary, 5000)                       -- Increase salary by 5000
sub(Salary, 3000)                        -- Decrease salary by 3000
mul(Salary, 1.10)                        -- Increase salary by 10%
div(Salary, 2)                           -- Divide salary into two parts
mod(EmployeeID, 2)                        -- Check if EmployeeID is even or odd
round(Salary, -3)                        -- Round salary to nearest thousand
abs(Salary - 60000)                      -- Get absolute difference in salary
max(Salary)                              -- Get maximum salary
min(Salary)                              -- Get minimum salary
avg(Salary)                              -- Calculate average salary



year(JoiningDate)                        -- Extract year from JoiningDate
month(JoiningDate)                       -- Extract month from JoiningDate
day(JoiningDate)                         -- Extract day from JoiningDate
dateDiff(JoiningDate, utcNow(), 'YYYY')  -- Find years since joining
addYears(JoiningDate, 5)                 -- Add 5 years to JoiningDate
addMonths(JoiningDate, -2)               -- Subtract 2 months from JoiningDate
formatDateTime(JoiningDate, 'yyyy/MM/dd') -- Convert JoiningDate format
dayOfWeek(JoiningDate)                   -- Get day of the week (0=Sunday, 6=Saturday)
ticks(JoiningDate)                       -- Convert JoiningDate to ticks



iif(Age > 30, 'Senior', 'Junior')        -- Categorize employees based on age
iif(Salary > 60000, 'High Earner', 'Low Earner') -- Categorize based on salary
EmployeeID in (101, 103, 105)            -- Check if EmployeeID exists in list
not(Age > 30)                            -- Negate condition
and(Age > 30, Salary > 50000)            -- Employees older than 30 earning above 50k
or(Age < 25, Salary > 70000)             -- Employees younger than 25 or earning above 70k
equals(Department, 'IT')                 -- Check if department is IT
coalesce(null, 'No Data Available')      -- Return default value if null



array(EmployeeID, Name, Department)      -- Create an array with employee data
length(array(EmployeeID, Name))          -- Get array length
join(array('HR', 'IT', 'Finance'), '-')  -- Join departments into string
first(array('Alice', 'Bob', 'Charlie'))  -- Get first employee name in array
last(array('Alice', 'Bob', 'Charlie'))   -- Get last employee name in array
indexOf(array('HR', 'IT', 'Finance'), 'IT') -- Get index of 'IT' in department array
union(array('HR', 'IT'), array('Finance', 'IT')) -- Merge arrays
intersect(array('HR', 'IT'), array('IT', 'Finance')) -- Get common departments
except(array('HR', 'IT', 'Finance'), array('IT')) -- Remove 'IT' from department list
contains(array('HR', 'IT', 'Finance'), 'IT') -- Check if 'IT' exists in array




toInteger('123')                         -- Convert string to integer
toFloat('12.34')                         -- Convert string to float
toBoolean('true')                        -- Convert string to boolean
toDate('2022-10-12')                     -- Convert string to date
string(Salary)                           -- Convert Salary to string
json('{ "EmployeeID": 101, "Name": "Alice" }') -- Parse JSON string
base64(Name)                             -- Encode employee name to Base64
decodeBase64(base64(Name))               -- Decode Base64 to original name



fileName('/data/employees.csv')         -- Extract file name
fileExtension('/data/employees.csv')    -- Extract file extension
filePath('/data/employees.csv')         -- Get file path without extension
exists('/data/employees.csv')           -- Check if file exists
size('/data/employees.csv')             -- Get file size



iif(dateDiff(OrderDate, ShipDate, 'Day') > 5, 'Delayed', 'On Time')

iif(Quantity == 0, 'Out of Stock', 'Available')





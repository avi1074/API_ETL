employees_quarter = """
WITH quarter_hired AS (
    SELECT 
        EXTRACT(QUARTER FROM employees.datetime::date) AS quarter,
        employees.id AS employees_id,
        departments.departments AS department_name,
        jobs.job AS job_name,
        EXTRACT(year FROM employees.datetime::date) AS year_e
    FROM 
        employees 
    JOIN 
        departments ON employees.department_id = departments.id
    JOIN 
        jobs ON jobs.id = employees.job_id
    WHERE
    	EXTRACT(year FROM employees.datetime::date) = '2021'
)

SELECT 
    department_name, 
    job_name, 
    COUNT(DISTINCT CASE WHEN quarter = 1 THEN employees_id END) AS Q1,
    COUNT(DISTINCT CASE WHEN quarter = 2 THEN employees_id END) AS Q2,
    COUNT(DISTINCT CASE WHEN quarter = 3 THEN employees_id END) AS Q3,
    COUNT(DISTINCT CASE WHEN quarter = 4 THEN employees_id END) AS Q4
FROM 
    quarter_hired
GROUP BY 
    department_name, 
    job_name
ORDER BY 
    department_name, 
    job_name;
"""


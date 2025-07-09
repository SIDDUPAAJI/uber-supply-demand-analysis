
-- Create the Uber data table
CREATE TABLE uber_data (
    Request_id INTEGER,
    Pickup_point TEXT,
    Driver_id INTEGER,
    Status TEXT,
    Request_timestamp TEXT,
    Drop_timestamp TEXT,
    Request_hour INTEGER,
    Time_slot TEXT
);

-- Sample Queries

-- 1. Total requests by status
SELECT Status, COUNT(*) as total_requests
FROM uber_data
GROUP BY Status;

-- 2. Total requests by time slot
SELECT [Time slot], COUNT(*) as total_requests
FROM uber_data
GROUP BY [Time slot]
ORDER BY total_requests DESC;

-- 3. Cancelled rides by pickup point
SELECT [Pickup point], COUNT(*) as cancellations
FROM uber_data
WHERE Status = 'Cancelled'
GROUP BY [Pickup point];

-- 4. Completion rate by time slot
SELECT [Time slot],
    ROUND(SUM(CASE WHEN Status = 'Trip Completed' THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 2) as completion_rate
FROM uber_data
GROUP BY [Time slot];

-- 5. Completed trips per time slot and pickup point
SELECT [Pickup point], [Time slot], COUNT(*) as completed
FROM uber_data
WHERE Status = 'Trip Completed'
GROUP BY [Pickup point], [Time slot]
ORDER BY completed DESC;

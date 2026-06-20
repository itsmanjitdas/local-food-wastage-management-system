-- Q1: Total food providers and receivers in each city
SELECT City, COUNT(DISTINCT Provider_ID) AS Total_Providers, COUNT(DISTINCT Receiver_ID) AS Total_Receivers 
FROM (SELECT City, Provider_ID, NULL AS Receiver_ID FROM Providers 
      UNION ALL SELECT City, NULL AS Provider_ID, Receiver_ID FROM Receivers) as Combined GROUP BY City;

-- Q2: Type of food provider that contributes the most food
SELECT Provider_Type, SUM(Quantity) AS Total_Food_Donated FROM Food_Listings GROUP BY Provider_Type ORDER BY Total_Food_Donated DESC;

-- Q3: Contact information of food providers in Bangalore
SELECT Name, Type, Contact, Address, City FROM Providers WHERE City = 'Bangalore';

-- Q4: Receivers who have claimed the most food listings
SELECT r.Name, r.Type, COUNT(c.Claim_ID) AS Total_Claims FROM Receivers r JOIN Claims c ON r.Receiver_ID = c.Receiver_ID GROUP BY r.Receiver_ID, r.Name, r.Type ORDER BY Total_Claims DESC;

-- Q5: Total quantity of food available from all providers combined
SELECT SUM(Quantity) AS Total_Available_Food FROM Food_Listings;

-- Q6: City with the highest number of food listings
SELECT Location AS City, COUNT(Food_ID) AS Total_Listings FROM Food_Listings GROUP BY Location ORDER BY Total_Listings DESC LIMIT 1;

-- Q7: Most commonly available food types
SELECT Food_Type, COUNT(*) AS Listing_Count, SUM(Quantity) AS Total_Quantity FROM Food_Listings GROUP BY Food_Type ORDER BY Total_Quantity DESC;

-- Q8: Number of food claims made for each food item
SELECT fl.Food_Name, COUNT(c.Claim_ID) AS Total_Claims_Made FROM Food_Listings fl LEFT JOIN Claims c ON fl.Food_ID = c.Food_ID GROUP BY fl.Food_Name ORDER BY Total_Claims_Made DESC;

-- Q9: Provider with the highest number of successful food claims
SELECT p.Name, COUNT(c.Claim_ID) AS Successful_Claims FROM Providers p JOIN Food_Listings fl ON p.Provider_ID = fl.Provider_ID JOIN Claims c ON fl.Food_ID = c.Food_ID WHERE c.Status = 'Completed' GROUP BY p.Provider_ID, p.Name ORDER BY Successful_Claims DESC LIMIT 1;

-- Q10: Percentage breakdown of food claims status
SELECT Status, COUNT(*) AS Count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Claims), 2) AS Percentage FROM Claims GROUP BY Status;

-- Q11: Average quantity of food claimed per receiver
SELECT r.Name, ROUND(AVG(fl.Quantity), 2) AS Avg_Quantity_Claimed FROM Receivers r JOIN Claims c ON r.Receiver_ID = c.Receiver_ID JOIN Food_Listings fl ON c.Food_ID = fl.Food_ID GROUP BY r.Receiver_ID, r.Name;

-- Q12: Meal type claimed the most
SELECT fl.Meal_Type, COUNT(c.Claim_ID) AS Claims_Count FROM Food_Listings fl JOIN Claims c ON fl.Food_ID = c.Food_ID GROUP BY fl.Meal_Type ORDER BY Claims_Count DESC;

-- Q13: Total quantity of food donated by each provider
SELECT p.Name, p.Type, SUM(fl.Quantity) AS Total_Donated FROM Providers p JOIN Food_Listings fl ON p.Provider_ID = fl.Provider_ID GROUP BY p.Provider_ID, p.Name, p.Type ORDER BY Total_Donated DESC;

-- Q14: Food listings that expired before being claimed
SELECT fl.Food_Name, fl.Expiry_Date, fl.Location FROM Food_Listings fl LEFT JOIN Claims c ON fl.Food_ID = c.Food_ID WHERE fl.Expiry_Date < CURDATE() AND (c.Claim_ID IS NULL OR c.Status = 'Cancelled');

-- Q15: Monthly trend of food claims made
SELECT DATE_FORMAT(Timestamp, '%Y-%m') AS Month, COUNT(Claim_ID) AS Total_Claims FROM Claims GROUP BY Month ORDER BY Month ASC;
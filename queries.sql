/* List all instructors who has given more than a specific number of lessons during the current month. Sum all lessons, independent of type, and sort the result by the number of given lessons. This query will be used to find instructors risking to work too much, and will be executed daily. */

SELECT fullName, personNumber, lessonsInMonth
FROM Teacher
INNER JOIN (
	SELECT teacherID, COUNT(teacherID) AS lessonsInMonth
	FROM TimeSlot
	WHERE
		TimeSlot.month = (SELECT EXTRACT(MONTH FROM (SELECT CURRENT_DATE))) AND
		TimeSlot.year = (SELECT EXTRACT(YEAR FROM (SELECT CURRENT_DATE)))
	GROUP BY teacherID
) AS teachersInMonth
ON Teacher.teacherID = teachersInMonth.teacherID
INNER JOIN Person
ON Person.personID = Teacher.personID
ORDER BY lessonsInMonth
;



/* Show how many students there are with no sibling, with one sibling, with two siblings, etc. This query is expected to be performed a few times per week. */

WITH a AS (
SELECT siblingCount, COUNT(siblingCount) AS studentAmount
	FROM
	(
		SELECT student.studentID, COUNT(student.studentID) AS siblingCount
		FROM student, siblings
		WHERE student.studentID = siblings.studentID OR student.studentID = siblings.siblingID
		GROUP BY student.studentID
	) AS xyz
	GROUP BY siblingCount
),
b AS (SELECT COUNT(studentID) AS studentAmount FROM Student)
SELECT * FROM a
UNION ALL
SELECT 0 AS siblingCount, studentAmount - (SELECT SUM(studentAmount) FROM a) AS studentAmount FROM b
ORDER BY siblingCount
;



/* List all ensembles held during the next week, sorted by music genre and weekday. For each ensemble tell whether it's full booked, has 1-2 seats left or has more seats left. Hint: you might want to use a CASE statement in your query to produce the desired output. */

WITH infoNextWeek AS (
	SELECT Ensamble.lessonID, timeSlotID, day, month, year, genre, maxStudents
	FROM Ensamble
	INNER JOIN (
		WITH timeSlotsNextWeek AS (
			WITH UPPER_DATE AS (SELECT CURRENT_DATE + INTERVAL '7 days' AS u_date)
			SELECT TimeSlot.timeSlotID, TimeSlot.day, TimeSlot.month, TimeSlot.year
			FROM TimeSlot, UPPER_DATE
			GROUP BY TimeSlot.timeSlotID, UPPER_DATE.u_date
			HAVING
				(TimeSlot.year BETWEEN EXTRACT(YEAR FROM CURRENT_DATE) AND EXTRACT(YEAR FROM UPPER_DATE.u_date))
				AND
				(TimeSlot.month BETWEEN EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(MONTH FROM UPPER_DATE.u_date))
				AND
				(TimeSlot.day BETWEEN EXTRACT(DAY FROM CURRENT_DATE) AND EXTRACT(DAY FROM UPPER_DATE.u_date))
		)
		SELECT LessonTimeSlot.lessonID, timeSlotsNextWeek.timeSlotID, day, month, year
		FROM timeSlotsNextWeek
		INNER JOIN LessonTimeSlot
		ON timeSlotsNextWeek.timeSlotID = LessonTimeSlot.timeSlotID
	) AS lessonsNextWeek
	ON Ensamble.lessonID = lessonsNextWeek.lessonID
)

SELECT genre,
CASE /* this probably isn't the best way of doing this, but this operation is also a relatively simple one on what will mostly be small sets, so I'll allow it */
	WHEN EXTRACT(DOW FROM MAKE_DATE(year, month, day)) = 0 THEN 'Sunday'
	WHEN EXTRACT(DOW FROM MAKE_DATE(year, month, day)) = 1 THEN 'Monday'
	WHEN EXTRACT(DOW FROM MAKE_DATE(year, month, day)) = 2 THEN 'Tuesday'
	WHEN EXTRACT(DOW FROM MAKE_DATE(year, month, day)) = 3 THEN 'Wednesday'
	WHEN EXTRACT(DOW FROM MAKE_DATE(year, month, day)) = 4 THEN 'Thursday'
	WHEN EXTRACT(DOW FROM MAKE_DATE(year, month, day)) = 5 THEN 'Friday'
	WHEN EXTRACT(DOW FROM MAKE_DATE(year, month, day)) = 6 THEN 'Saturday'
END AS weekDay,
CASE
	WHEN maxstudents - count > 0 AND maxstudents - count < 3 THEN '1-2 seats left'
	WHEN maxstudents - count > 2 THEN 'Many seats left'
	WHEN maxstudents - count < 1 THEN 'Fully booked'
END AS seatStatus
FROM infoNextWeek
INNER JOIN (
	SELECT lessonID, COUNT(studentID)
	FROM StudentLesson
	WHERE StudentLesson.lessonID IN (SELECT lessonID FROM infoNextWeek)
	GROUP BY lessonID
) AS registeredStudents
ON registeredStudents.lessonID = infoNextWeek.lessonID
ORDER BY genre, weekDay
;



/* Show the number of lessons given per month during a specified year. t shall be possible to retrieve the total number of lessons per month (just one number per month) and the specific number of individual lessons, group lessons and ensembles (three numbers per month) */

WITH lessonsInYear AS (
	SELECT lessonID, day, month, year
	FROM LessonTimeSlot
	INNER JOIN
	(SELECT timeSlotID, day, month, year FROM TimeSlot WHERE year = 2022) AS timeSlotsInYear
	ON timeSlotsInYear.timeSlotID = LessonTimeSlot.timeSlotID
)
SELECT groupLes.month, totalLessons, groupLessons, individualLessons, ensambleLessons
FROM (
	SELECT month, COUNT(*) AS groupLessons
	FROM GroupLesson
	INNER JOIN lessonsInYear
	ON GroupLesson.lessonID = lessonsInYear.lessonID
	GROUP BY month
) AS groupLes
FULL OUTER JOIN (
	SELECT month, COUNT(*) AS individualLessons
	FROM IndividualLesson
	INNER JOIN lessonsInYear
	ON IndividualLesson.lessonID = lessonsInYear.lessonID
	GROUP BY month
) AS indivLes
ON groupLes.month = indivLes.month
FULL OUTER JOIN (
	SELECT month, COUNT(*) AS ensambleLessons
	FROM Ensamble
	INNER JOIN lessonsInYear
	ON Ensamble.lessonID = lessonsInYear.lessonID
	GROUP BY month
) AS ensamLes
ON groupLes.month = ensamLes.month
FULL OUTER JOIN (
	SELECT month, COUNT(lessonID) AS totalLessons
	FROM lessonsInYear
	GROUP BY month
	ORDER BY month
) AS totalLes
ON groupLes.month = totalLes.month
ORDER BY groupLes.month
;
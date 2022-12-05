
### Students without siblings
SELECT COUNT(studentid)
FROM student
WHERE studentid not in (SELECT studentid FROM siblings);

### Average lessons per month
# find timeslots that are in lessontimeslot and are of the given year
# group by month
# select count(timeslotid) as lessonsinmonth
# select avg(lessonsinmonth)

SELECT AVG(lessons_in_month) FROM (
	SELECT COUNT(timeslotid) as lessons_in_month
	FROM timeslot
	WHERE timeslotid in (SELECT timeslotid FROM lessontimeslot)
		and year = 2022
	GROUP BY month
) as FOO;

### Amount of lessons in given month
# select timeslots in lessontimeslot and has the given month and year
# select COUNT

SELECT COUNT(timeslotid)
FROM timeslot
WHERE timeslotid in (SELECT timeslotid FROM lessontimeslot)
	and month = 6 and year = 2022
;

### Amount of lessons of given type in given month
# timeslots in month > lessonids in month > lessons in month > specific type of lesson in month
# select timeslots in lessontimeslots and with the right year and month
# select corresponding lessonids
# select corresponding lessons of the given type
# count them

SELECT COUNT(lessonid) FROM lesson WHERE lessontype = 2 and lessonid in (
	SELECT lessonid FROM lessontimeslot WHERE timeslotid in (
		SELECT timeslotid
		FROM timeslot
		WHERE timeslotid in (SELECT timeslotid FROM lessontimeslot)
			and month = 6 and year = 2022
	)
);

### Teachers who have given more than a specified amount of lessons in the current month
# timeslots in month > lessonids in month > lessons in month > teachers in month
# group by teacherid

SELECT teacherid, lessons_held FROM (
	SELECT teacherid, COUNT(teacherid) as lessons_held FROM lesson WHERE lessonid in (
		SELECT lessonid FROM lessontimeslot WHERE timeslotid in (
			SELECT timeslotid
			FROM timeslot
			WHERE (
				timeslotid in (SELECT timeslotid FROM lessontimeslot)
				and month = (SELECT EXTRACT(MONTH FROM CURRENT_DATE) AS mon)
				and year = (SELECT EXTRACT(YEAR FROM CURRENT_DATE) AS yer)
			)
		)
	)
	GROUP BY teacherid
) as FOO
WHERE lessons_held > 0;

### Teachers and amount of lessons they have given this month, in sorted order
# timeslots in month > lessonids in month > lessons in month > teachers in month
# group by teacher id
# count teacher id
# sort by count

SELECT teacherid, lessons_held FROM (
	SELECT teacherid, COUNT(teacherid) as lessons_held FROM lesson WHERE lessonid in (
		SELECT lessonid FROM lessontimeslot WHERE timeslotid in (
			SELECT timeslotid
			FROM timeslot
			WHERE (
				timeslotid in (SELECT timeslotid FROM lessontimeslot)
				and month = (SELECT EXTRACT(MONTH FROM CURRENT_DATE) AS mon)
				and year = (SELECT EXTRACT(YEAR FROM CURRENT_DATE) AS yer)
			)
		)
	)
	GROUP BY teacherid
) as FOO
ORDER BY lessons_held;

### Amount of students that have a specified amount of siblings
SELECT COUNT(sibling_amount)
FROM (
	SELECT COUNT(studentid) as sibling_amount
	FROM siblings
	GROUP BY studentid
) as FOO
WHERE (sibling_amount = 1);















from faker import Faker
from random import randint

print("Building data:")

# Amount of tuples in respective relations
person_amount = 10000
knownInstruments_amount = int(1.5 * person_amount)
student_amount = int(0.6 * person_amount)
teacher_amount = int(person_amount - student_amount)
studentInstrument_amount = int(0.6 * student_amount)
personContact_amount = int(student_amount)
instrument_amount = int(1.1 * student_amount)
siblings_amount = int(0.2 * student_amount)
double_sibling_amount = int(0.1 * siblings_amount)
address_amount = int(student_amount - siblings_amount)
contact_amount = int(student_amount - siblings_amount)
timeSlot_amount = int(1.2 * teacher_amount)
lesson_amount = int(0.8 * timeSlot_amount)
ensamble_amount = int(lesson_amount / 3)
groupLesson_amount = int(lesson_amount / 3)
individualLesson_amount = int(lesson_amount / 3)
studentLesson_amount = int(lesson_amount)
lessonTimeSlot_amount = int(lesson_amount)

# Resources
fake = Faker()

def randomPhone():
	number = "+467"
	for i in range(0, 8):
		number = number + str(randint(0, 9))
	return number

def randomPersonalNumber():
	return str(randint(1960, 2016)) + str(randint(1, 12)) + str(randint(1, 30)) + str(randint(1000, 9999))

def randomBool(percent):
	num = randint(0, 101)
	if num <= percent:
		return True
	else:
		return False

def randomFromList(entries):
	return entries[randint(0, len(entries) - 1)]

# Pre-defined tuples
print("Price...", end = " ")
price = [
	{"lessonType" : 0, "cost" : 49},
	{"lessonType" : 1, "cost" : 39},
	{"lessonType" : 2, "cost" : 29}
]
print("Done.")

print("Skill...", end = " ")
skill = [
	{"skill" : 0, "title" : "beginner"},
	{"skill" : 1, "title" : "intermediate"},
	{"skill" : 2, "title" : "advanced"}
]
print("Done.")

print("LessonType...", end = " ")
lessonType = [
	{"type" : 0, "title" : "individual"},
	{"type" : 1, "title" : "group"},
	{"type" : 2, "title" : "ensamble"}
]
print("Done.")

# Randomized tuples
print("Address...", end = " ")
address = []
for i in range(0, address_amount):
	address.append({
		"addressID" : i,
		"street" : fake.name() + " " + randomFromList(["Street", "Road", "Avenue", "Park", "Drive"]),
		"zipCode" : randint(10000, 99999),
		"city" : fake.city()
	})
print("Done.")

print("Contact...", end = " ")
contact = []
for i in range(0, contact_amount):
	contact.append({
		"contactID" : i,
		"contactTitle" : fake.name(),
		"phoneNumber" : randomPhone(),
		"emailAddress" : fake.email()
	})
print("Done.")

print("Instrument...", end = " ")
instrument = []
for i in range(0, instrument_amount):
	instrument.append({
		"instrumentID" : i,
		"type" : randomFromList(["guitar", "piano", "saw", "harmonica", "theremin", "spoon", "flute", "bass", "drums"]),
		"brand" : randomFromList(["home made", "IKEA", "Flying Tiger", "Stradivarius"]),
		"price" : randint(5, 500),
		"monthRented" : "NULL",
		"yearRented" : "NULL"
	})
print("Done.")

print("Teacher...", end = " ")
person = []
teacher = []
student = []
siblings = []
knownInstruments = []
personContact = []
for i in range(0, teacher_amount):
	person.append({
		"personID" : i,
		"teacherID" : i,
		"addressID" : i,
		"personNumber" : randomPersonalNumber(),
		"fullName" : fake.name()
	})
	tEnsamble = randomBool(90);
	if tEnsamble:
		tEnsamble = 1
	else:
		tEnsamble = 0
	teacher.append({
		"teacherID" : i,
		"personID" : i,
		"teachesEnsambles" : tEnsamble
	})
	knownInstruments.append({
		"personID" : i,
		"instrument" : randomFromList(["guitar", "piano", "saw", "harmonica", "theremin", "singing", "spoon", "flute", "bass", "drums"])
	})
print("Done.")
print("TimeSlot...", end = " ")
timeSlot = []
for i in range(0, timeSlot_amount):
	datee = fake.date().split("-")
	timeSlot.append({
		"timeSlotID" : i,
		"teacherID" : randint(0, teacher_amount - 1),
		"day" : datee[2],
		"month" : datee[1],
		"year" : randint(2018, 2022),
		"time" : fake.time()
	})
print("Done.")

print("Student...", end = " ")
for i in range(teacher_amount, person_amount - siblings_amount):
	person.append({
		"personID" : i,
		"studentID" : i - teacher_amount,
		"addressID" : i,
		"personNumber" : randomPersonalNumber(),
		"fullName" : fake.name()
	})
	admit = randomBool(90)
	if admit:
		admit = 1
	else:
		admit = 0
	student.append({
		"studentID" : i - teacher_amount,
		"personID" : i,
		"admitted" : admit
	})
	knownInstruments.append({
		"personID" : i,
		"instrument" : randomFromList(["guitar", "piano", "saw", "harmonica", "theremin", "singing", "spoon", "flute", "bass", "drums"])
	})
	personContact.append({
		"personID" : i,
		"contactID" : i - teacher_amount
	})

for i in range(person_amount - siblings_amount, person_amount):
	person.append({
		"personID" : i,
		"studentID" : i - teacher_amount,
		"addressID" : i - person_amount + siblings_amount,
		"personNumber" : randomPersonalNumber(),
		"fullName" : fake.name()
	})
	admit = randomBool(90)
	if admit:
		admit = 1
	else:
		admit = 0
	student.append({
		"studentID" : i - teacher_amount,
		"personID" : i,
		"admitted" : admit
	})
	siblings.append({
		"studentID" : i - teacher_amount,
		"siblingID" : (i - person_amount + siblings_amount) % (siblings_amount - double_sibling_amount)
	})
	siblings.append({
		"studentID" : (i - person_amount + siblings_amount) % (siblings_amount - double_sibling_amount),
		"siblingID" : i - teacher_amount
	})
	knownInstruments.append({
		"personID" : i,
		"instrument" : randomFromList(["guitar", "piano", "saw", "harmonica", "theremin", "singing", "spoon", "flute", "bass", "drums"])
	})
	personContact.append({
		"personID" : i,
		"contactID" : i - person_amount + siblings_amount
	})

print("Done.")
print("Siblings... Done.")
print("PersonContact... Done.")

print("KnownInstrument...", end = " ")
for i in range(0, knownInstruments_amount - person_amount):
	insts = ["guitar", "piano", "saw", "harmonica", "theremin", "singing", "spoon", "flute", "bass", "drums"]
	insts.remove(knownInstruments[i]["instrument"])
	knownInstruments.append({
		"personID" : i,
		"instrument" : randomFromList(insts)
	})
print("Done.")

print("StudentInstrument...", end = " ")
studentInstrument = []
rentedInstruments = []
for i in range(0, studentInstrument_amount):
	inst = knownInstruments[i + teacher_amount]["instrument"]
	instID = 0
	found = False
	for s in range(0, len(instrument) - 1):
		if instrument[s]["type"] == inst and (not instrument[s]["instrumentID"] in rentedInstruments):
			rentedInstruments.append(instrument[s]["instrumentID"])
			instID = instrument[s]["instrumentID"]
			found = True
			break

	if found:
		instrument[instID]["monthRented"] = randint(1, 12)
		instrument[instID]["yearRented"] = randint(2019, 2022)
		studentInstrument.append({
			"studentID" : i,
			"instrumentID" : instID
		})
print("Done.")

print("Lesson...", end = " ")
lesson = []
lessonTimeSlot = []
individualLesson = []
groupLesson = []
ensamble = []
studentLesson = []
for i in range(0, lesson_amount):
	lesson_tuple = {
		"lessonID" : i,
		"skill" : randint(0, 2),
		"lessonType" : randint(0, 2)
	}
	if lesson_tuple["lessonType"] == 0:
		lesson_tuple["teacherID"] = randint(0, teacher_amount - 1)
		inst = randomFromList(["guitar", "piano", "saw", "harmonica", "theremin", "singing", "spoon", "flute", "bass", "drums"])
		individualLesson.append({
			"lessonID" : i,
			"instrument" : inst
		})
		studentLesson.append({
			"studentID" : randint(0, student_amount - 1),
			"lessonID" : i
		})
	elif lesson_tuple["lessonType"] == 1:
		lesson_tuple["teacherID"] = randint(0, teacher_amount - 1)
		minStudents = randint(2, 4)
		maxStudents = randint(minStudents, 10)
		groupLesson.append({
			"lessonID" : i,
			"maxStudents" : maxStudents,
			"minStudents" : minStudents,
			"instrument" : randomFromList(["guitar", "piano", "saw", "harmonica", "theremin", "singing", "spoon", "flute", "bass", "drums"])
		})
		added_students = []
		for k in range(0, randint(minStudents, maxStudents)):
			studentID = randint(0, student_amount - 1)
			while studentID in added_students: 
				studentID = randint(0, student_amount - 1)
			added_students.append(studentID)
			studentLesson.append({
				"studentID" : studentID,
				"lessonID" : i
			})
	elif lesson_tuple["lessonType"] == 2:
		teacherID = randint(0, teacher_amount - 1)
		while not teacher[teacherID]["teachesEnsambles"]:
			teacherID = randint(0, teacher_amount - 1)
		lesson_tuple["teacherID"] = teacherID
		minStudents = randint(2, 4)
		maxStudents = randint(minStudents, 10)
		ensamble.append({
			"lessonID" : i,
			"minStudents" : minStudents,
			"maxStudents" : maxStudents,
			"genre" : randomFromList(["rock", "pop", "folk", "electronica", "punk", "silence", "classical", "gregorian chants", "idm", "raggae", "jazz"])
		})
		added_students = []
		for k in range(0, randint(minStudents, maxStudents)):
			studentID = randint(0, student_amount - 1)
			while studentID in added_students: 
				studentID = randint(0, student_amount - 1)
			added_students.append(studentID)
			studentLesson.append({
				"studentID" : studentID,
				"lessonID" : i
			})
	else:
		print("Error: Invalid lesson type.")
	lesson.append(lesson_tuple)
	takenSlots = []
	lessonTimeSlot.append({
		"lessonID" : i,
		"timeSlotID" : i
	})
print("Done.")
print("IndividualLesson... Done.")
print("GroupLesson... Done.")
print("Ensamble... Done.")
print("LessonTimeSlot... Done.")
print("StudentLesson... Done.")

print("Building Complete.")
ans = input("Review the data? Y/n (Y) ")

if ans.lower() != "n":
	print("Reviewing data. Type 'exit' to proceed to export.")
	while True:
		inp = input("> ")
		data = []
		if inp == "exit":
			break
		elif inp == "address":
			data = address
		elif inp == "contact":
			data = contact
		elif inp == "ensamble":
			data = ensamble
		elif inp == "group":
			data = groupLesson
		elif inp == "individual":
			data = individualLesson
		elif inp == "instrument":
			data = instrument
		elif inp == "known":
			data = knownInstruments
		elif inp == "lesson":
			data = lesson
		elif inp == "lessontime":
			data = lessonTimeSlot
		elif inp == "person":
			data = person
		elif inp == "personcontact":
			data = personContact
		elif inp == "price":
			data = price
		elif inp == "siblings":
			data = siblings
		elif inp == "student":
			data = student
		elif inp == "studentinstrument":
			data = studentInstrument
		elif inp == "studentlesson":
			data = studentLesson
		elif inp == "teacher":
			data = teacher
		elif inp == "timeslot":
			data = timeSlot
		elif inp == "skill":
			data = skill
		elif inp == "lessontype":
			data = lessonType
		else:
			print("Invalid command.")
			print("Valid commands are: exit, address, contact, ensamble, group, individual, individualLesson, instrument, known, lessontime, person, personcontact, price, siblings, student, studentinstrument, studentlesson, teacher, timeslot, skill, lessontype")

		for i in data:
			print(i)
ans = input("Export to SQL file? Y/n (Y) ")
if ans.lower() != "n":
	print("Exporting to file...")
	file_name = str(input("Enter export file name: "))
	file = open(file_name, "w")

	relations = {
		"Address" : address,
		"Contact" : contact,
		"Instrument" : instrument,
		"Price" : price,
		"Skill" : skill,
		"LessonType" : lessonType,
		"Person" : person,
		"KnownInstruments" : knownInstruments,
		"PersonContact" : personContact,
		"Teacher" : teacher,
		"Student" : student,
		"Lesson" : lesson,
		"Siblings" : siblings,
		"StudentInstrument" : studentInstrument,
		"GroupLesson" : groupLesson,
		"Ensamble" : ensamble,
		"IndividualLesson" : individualLesson,
		"StudentLesson" : studentLesson,
		"TimeSlot" : timeSlot,
		"LessonTimeSlot" : lessonTimeSlot
	}

	for b in relations:
		name = b
		dat = relations[b]
		line = "\nINSERT INTO " + name + " ("
		for a in dat[0]:
			line = line + a + ", "
		line = line[:-2] + ") VALUES"
		for t in dat:
			file.write(line + "\n")
			line = "	("
			for a in t:
				formatting = ""
				if type(t[a]) is str and t[a] != "NULL":
					formatting = "'"
				line = line + formatting + str(t[a]) + formatting + ", "
			line = line[:-2] + "),"
		file.write(line[:-1] + ";\n")

	file.close()

print("Done. Exiting...")
<!DOCTYPE html>
<html>
<head>
<title>Student Dashboard</title>
</head>

<body>
	<h1>Welcome to your dashboard...</h1>
	<h2><?php echo @$error; ?></h2>

	<form method="post" >
                <input type="email" name="to" placeholder="Enter Receiver Email">
                <br><br>
                <input type="text" name="subject" placeholder="Enter Subject">
                <br><br>
                <textarea rows="6" name="message" placeholder="Enter your message here"></textarea>
                <br><br>
                <input type="submit" value="Send Email" />
            </form>
</body>
</html>
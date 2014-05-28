<?php
/*
Triangle de Sierpinski
par  killruana <killruana@gmail.com>
*/


if (isset($_GET['x'])) { // Est-ce que la taille de l'image est sp�cifi�e ?
	$size_x = $_GET['x'];
} else { // Si non, on impose une taille
	$size_x = 640;
}

/*
if ($size_x > 1024) { // On impose une taille maximun, pour �viter de voler trop de ressources...
	$size_x = 1024;
}
*/

$size_y = $size_x*3/4; // L'image est au format 4/3

$img = imagecreate($size_x,$size_y); // Cr�ation d'une image

// On d�finit ici les couleurs qui seront utilis�s
$yellow = imagecolorallocate($img, 0xff, 0xff, 0x00); // Jaune 
$black = imagecolorallocate($img, 0x00, 0x00, 0x00);  // Noir

imagefill($img, 0, 0, $black); // On remplit le fond de l'image


// Initialisation de l'algorithme
$X = mt_rand(0,100);
$Y = mt_rand(0,100);

// Algorithme du triangle de Sierpinski
for($k=0; $k<=(.5*$size_x*$size_y); $k++) {
	$N= mt_rand(1000000, 9999999)/10000000;

	if ($N<=1/3) {
		$X = $X*0.5;
		$Y = $Y*0.5;
	}

	if (1/3<$N and $N<=2/3) {
		$X = ($X+($size_x/2))*0.5;
		$Y = ($Y+$size_y)*0.5;
	}

	if (2/3<$N) {
		$X = ($X+$size_x)*0.5;
		$Y = $Y*0.5;
	}
	
	imagerectangle($img, $X, $Y, $X, $Y, $yellow); // Ajout du pixel � sa place
}


header("Content-Type: image/png"); // Envoie du header
imagepng($img); // Affichage de l'image
imagedestroy($img); // Destruction de l'image
?>

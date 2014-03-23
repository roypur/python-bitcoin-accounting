<?php
$btc=$_GET["address"];
$address = ereg_replace("[^A-Za-z0-9]", "", $btc );
echo exec("/srv/python/bitcoin/pay.py --address $address");
?>

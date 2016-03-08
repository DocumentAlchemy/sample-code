<?php

# This script will download a PNG image file containing a QR code that encodes
# an aribtrary string.

# See the README or visit:
# https://documentalchemy.com/api-doc#!/DocumentAlchemy/get_data_rendition_qr_png
# for more information.

# First let's set some variables we'll use below.

$api_key = 'CHANGE ME';        # PLEASE BE SURE TO CHANGE THE VALUE OF $api_key
$data = 'http://example.com/'; # This is the data we'll encode.
$size = 200;                   # The size of the image (in pixels).
$out_file = 'qr-code.png';     # The file to save the image to.

# Next we construct the URL we'll request.
$base_url = 'https://documentalchemy.com/api/v1/data/-/rendition/qr.png';
$uri = $base_url . '?data=' . urlencode($data) . "&size=" . $size;

# Open a file for writing.
$fp = fopen($out_file, 'wb');

# Initialize the curl request.
$ch = curl_init($uri);

# Configure the request.  Note that we add an `Authorization` header
# containing the API key.
curl_setopt_array($ch, array(
  CURLOPT_HTTPHEADER      => array('Authorization: da.key=' . $api_key),
  CURLOPT_RETURNTRANSFER  => true,
  CURLOPT_VERBOSE         => 1,
  CURLOPT_FILE            => $fp,
  CURLOPT_HEADER          => 0
));

# Execute the request.
curl_exec($ch);

# Finally close the request.
curl_close($ch);

?>

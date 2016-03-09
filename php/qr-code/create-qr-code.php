<?php

# This script will download a PNG image file containing a QR code that encodes
# an aribtrary string.

# See the README or visit:
# https://documentalchemy.com/api-doc#!/DocumentAlchemy/get_data_rendition_qr_png
# for more information.

# SANTITY CHECK
# If we're missing the API-KEY or TEXT-TO-ENCODE parameters,
# print usage instructions and exit.
if(count($argv) < 3) {
  echo "USE: <API-KEY> <TEXT-TO-ENCODE> [<OUTPUT-FILE-NAME>]\n";
  exit(1);
} else {

# Otherwise continue with the real work of the script.

  # Read parameters from the command line and set up other variables.

  $api_key  = $argv[1];
  $data     = $argv[2];
  $size    = 200;                # The size of the image (in pixels).
  $out_file = 'qr-code.png';     # The file to save the image to.
  if(count($argv) >= 4) {
    $out_file = $argv[3];
  }

  # Construct the URL we'll request.
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

  # And echo our results to the terminal.
  echo "QR code image saved at \"" . $out_file . "\".";
}

?>

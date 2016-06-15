<?php

# This script will return a count of the number of words in an MS Office
# or PDF file.
#
# You can run this program with the command:
#
#   php count-words.php <API-KEY> <FILE-TO-COUNT>
#
# where:
#
#  <API-KEY> is your DocumentAlchemy API key, which you
#    can obtain by registering for DocumentAlchemy at
#    https://documentalchemy.com/
#
# and
#
#  <FILE-TO-COUNT> is the PDF or Word document you want
#    to count the number of words in.
#
#
# This program works by submitting the file to the DocumentAlchemy
# API with an HTTP POST and then parsing the server's response.
#
# See the README or visit https://documentalchemy.com/api-doc
# for more information.


# SANITY CHECK: If we're missing the API-KEY or TEXT-TO-ENCODE parameters,
# print usage instructions and exit.
if(count($argv) < 3) {
  echo "USE: php word-count.php <API-KEY> <FILE-TO-COUNT>\n";
  exit(1);
} else {

  # Otherwise continue with the real work of the script.

  # Read parameters from the command line
  $api_key  = $argv[1];
  $document = $argv[2];

  # ANOTHER SANITY CHECK: confirm that the document actually exists before continuing.
  if(!file_exists($document)) {
    echo "ERROR: The file \"" . $document . "\" was not found.\n";
    exit(2);
  } else {

    # Since we have an API Key and a file, let's submit the request to the API>

    # `endpoint` is the API endpoint we'll be invoking.
    # See https://documentalchemy.com/api-doc#get_ofcpdf_document_rendition_wordcount
    # for more information about that method.
    $endpoint = 'https://documentalchemy.com/api/v1/document/-/rendition/wordcount.json';

    # Set `verbose` to 1 if you want detailed information about the HTTP transaction.
    $verbose = 0;

    # Initialize the curl request.
    $ch = curl_init($endpoint);

    # Create a "payload" containing the document to submit with the request.
    # `document` is the name of the form field that DocumentAlchemy is expecting.
    # Note that curl will treat `@foo` as a reference to the file `foo`.
    $payload = array( "document"=>"@".$document );

    # Configure the request.
    # Note that we add an `Authorization` header containing the API key.
    # and add our payload as `CUROPT_POSTFIELDS`.
    curl_setopt_array($ch, array(
      CURLOPT_HTTPHEADER      => array('Authorization: da.key=' . $api_key),
      CURLOPT_RETURNTRANSFER  => true,
      CURLOPT_VERBOSE         => $verbose,
      CURLOPT_POST            => true,
      CURLOPT_POSTFIELDS      => $payload
    ));

    # Execute the request.
    $response = curl_exec($ch);

    # Grab the HTTP status code
    $httpstatus = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    # Close the request.
    curl_close($ch);

    # Test the status code
    if($httpstatus != 200) {
      echo "\nOops. We expected a 200 response but found " . $httpstatus . " instead.\n";
      if($httpstatus === 401) {
        echo "\nNOTE: An HTTP 401 response suggests that that your API Key value is incorrect.\n";
        echo "Please visit https://documentalchemy.com/my-keys to confirm your API key.\n";
      } else if($httpstatus === 400) {
        echo "\nNOTE: An HTTP 400 response MIGHT indicate that your file wasn't a MS Word or PDF file.\n";
        echo "The server's reponse might contain a more precise description of the problem.\n";
      }
      echo "\nThe server returned:\n" .  $response . "\n\n";
      exit(3);
    } else {

      # Parse and test the response.
      $json = json_decode($response);
      if($json === NULL) {
        echo "\nOops. We had a problem trying to parse the server's response as JSON.\n";
        echo "\nThe server returned: " .  $response . "\n\n";
        exit(4);
      } else if($json->wordcount === NULL) {
        echo "\nOops. The server returned a JSON response but it doesn't contain the expected 'wordcount' attribute.\n";
        echo "\nThe server returned: " .  $response . "\n\n";
        exit(5);
      } else {

        # Echo our results to the console.
        echo "The file \"" . basename($document) . "\" contains " . $json->wordcount . " words.\n";

      } # (end of testing the $json response)

    } # (end of testing the $httpstatus)

  } # (end of second sanity check, testing that $document is a real file)

} # (end of first sanity check, testing that the command line arguments are valid)

?>

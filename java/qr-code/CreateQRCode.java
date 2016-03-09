// We'll need a few URL and file related classes below.
import java.net.URLEncoder;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.FileSystems;
import java.io.InputStream;
import java.nio.file.StandardCopyOption;

public class CreateQRCode {
  public static void main(String[] args) throws Exception {


    // SANITY CHECK

    // If we don't have all of the command line parameters, print a usage
    // message and exit...

    if(args.length < 2) {
      System.err.println("USE: <API-KEY> <TEXT-TO-ENCODE> [<OUTPUT-FILE-NAME>]");
      System.exit(1);

    // ...otherwise we perform the real work of the script.

    } else {

      // "CONSTANTS"
      // First let's define some "constants" that we may want to change from time to
      // time, but that we won't expose as command line paramters. See
      // https://documentalchemy.com/api-doc#!/DocumentAlchemy/get_data_rendition_qr_png
      // for detailed documenation of the "GET QR Code" method we're using here.

      String URL_BASE = "https://documentalchemy.com";
      String PATH     = "/api/v1/data/-/rendition/qr.png";
      int    SIZE     = 100; // Image size in pixels - note that `400` is the default.
      String ECL      = "L"; // Error correction level (the amount of redundancy in
                             //   the encoded image), one of `L`, `M`, `Q`, `H`.
                             //   The default is `H`.

      // COMMAND-LINE PARAMETERS

      String apiKey   = args[0];
      String data     = args[1];
      String fileName = null;
      if (args.length > 2) {
        fileName      = args[2];
      } else {
        fileName      = "qr-code.png";
      }

      // CONSTRUCT THE URL

      String u = URL_BASE + PATH;
      u += "?data=" + URLEncoder.encode(data,"utf-8");
      u += "&size=" + SIZE;
      u += "&ecl=" + ECL;
      URL url = new URL(u);

      // OPEN THE CONNECTION

      HttpURLConnection connection = (HttpURLConnection)(url.openConnection());

      try {

        // ADD THE AUTHORIZATION HEADER

        connection.setRequestMethod("GET");
        connection.setRequestProperty("Authorization", "da.key=" + apiKey);

        // DOWNLOAD THE FILE

        InputStream input = connection.getInputStream();
        Path outputPath = FileSystems.getDefault().getPath(fileName);
        Files.copy(input,outputPath,StandardCopyOption.REPLACE_EXISTING);

        // REPORT SUCCESS

        System.out.println("QR code image saved at \""+outputPath.toString()+"\".");

      } catch(Exception e) {

        // REPORT ERRORS IF NEEDED

        System.err.println("An error occured:" + e);
        throw e;

      } finally {

        // CLOSE THE CONNECTION

        if(connection != null) { connection.disconnect(); }

      }
    }
  }

}
